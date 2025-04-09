# Data Quality Monitoring Tool
Description: An AWS based tool that automatically monitors the quality of data flowing through ELT pipelines. It would check for missing values, inconsistencies, duplicates, or outliers and provide reports on data quality issues.

Target Market: Data-driven organizations that rely heavily on accurate, clean data (e.g., marketing agencies, data scientists, business intelligence teams).

Key Features:
Reports for data quality issues and monitoring improvements/declines over time.
Integration with AWS services for easy monitoring of ELT pipeline health.
Pre-configured rules for common data quality issues.


Step-by-Step Implementation:
1. Data Collection and Storage (S3 and RDS)
S3:

Store raw incoming data (e.g., CSVs, JSON files) in an S3 bucket.
S3 triggers Lambda functions when new files are uploaded, enabling real-time data quality checks.
RDS:

Set up an RDS instance (e.g., PostgreSQL or MySQL) to store structured data related to monitoring results and the status of the data pipeline.
You can also store metadata for data tracking and logging purposes.

2. Data Quality Checks Using Lambda
Lambda Function:

Lambda is best suited for lightweight, event-driven computing. Set up an event trigger so that when new data files are uploaded to S3, a Lambda function is invoked to run a data quality check on the file.
The Lambda function can:
Extract the file metadata (e.g., file name, size).
Perform checks like missing values, duplicates, or invalid data formats (using libraries like Pandas for Python).
Log the results of these checks (e.g., via Amazon CloudWatch logs or writing to an RDS database).
Lambda Workflow:

Trigger: An S3 event triggers the Lambda function whenever a new object is uploaded.
Process: The Lambda function loads the data (from S3), performs the quality checks, and stores the results in RDS or another data store.
Alerting: Lambda can trigger notifications via SNS (Simple Notification Service) or log data quality issues in CloudWatch.

3. EC2 for Heavy Data Processing
While Lambda is good for lightweight, event-driven tasks, EC2 will be used for heavy, long-running data processing tasks. For example, if data validation or cleansing tasks require more computational resources or run periodically (e.g., nightly batch jobs), EC2 can be used.

EC2 can be configured to run complex data quality checks (such as cross-referencing large data sets, running machine learning models for anomaly detection, etc.).
You can create a scheduled task (e.g., using cron jobs) to periodically query RDS for records that need additional processing and perform data quality checks on that data.
After processing, EC2 can push the results back to RDS or notify stakeholders if a critical issue is found.

4. Storing Results and Alerts (RDS and CloudWatch)
RDS:

Store the results of your data quality checks in the RDS database. Each record could contain information like:
File/Record ID: A unique identifier for each file/record processed.
Quality Check Type: The specific check (e.g., "Missing Values," "Duplicate Entries").
Status: Pass/Fail result for each check.
Timestamp: When the check was performed.
Error Details: Any issues found during the check.
CloudWatch:

CloudWatch Logs: Use CloudWatch Logs to capture Lambda logs, such as error messages or any critical issues found during data quality checks.
CloudWatch Alarms: Create CloudWatch Alarms to notify you when certain thresholds are breached (e.g., when a file fails a specific data quality check).
You can integrate with SNS to send alerts (email, SMS, etc.) when an alarm is triggered.

5. Data Quality Reporting
You may want to provide a user interface or dashboard for stakeholders to view the results of data quality checks. You can do this using AWS QuickSight or by building a custom reporting system.

AWS QuickSight:

QuickSight can connect to your RDS database, allowing you to visualize the results of your data quality checks in near real-time. You could create dashboards that show the status of data quality checks across multiple data sources.


6. Example Data Quality Checks
Your Lambda function or EC2 instance will perform various data quality checks, such as:

Missing Values:
Check if any critical fields (e.g., customer ID, date, or product code) have missing values.
If missing values are detected, log them to CloudWatch and store the details in RDS.
Duplicate Records:
Check for duplicate records based on a unique identifier (e.g., customer ID).
Notify users if duplicates are found and store the information in RDS.
Outlier Detection:
Use statistical methods to identify outliers (e.g., sales data that is far higher or lower than expected).
Alert the team or flag the records as suspicious in RDS.
Data Type Validation:
Ensure that the data types match expectations (e.g., a "Date" column contains only date-formatted values).
Notify users of invalid data entries and log the details in RDS.



# S3 JSON Uploader

A Python CLI application that randomly selects and uploads JSON files from a specified folder to an AWS S3 bucket at regular intervals.

## Requirements

- Python 3.11
- AWS account with S3 access
- Required Python packages (see requirements.txt)

## AWS Setup Instructions

### 1. Create S3 Bucket

1. Log into AWS Management Console
2. Navigate to S3 service
3. Make sure you're in the correct AWS Region
4. Click "Create bucket"
5. Configure bucket settings:
   - Choose `General purpose` bucket type
   - Choose a globally unique bucket name (this will be your `S3_BUCKET_NAME` in .env)
   - Leave most settings as default
   - Click "Create bucket"

### 2. Create IAM User and Policy

1. Go to IAM service in AWS Console
2. Click "Users" → "Create user"
3. Give your user a name (e.g., "s3-uploader")
4. Do NOT check the box next to "Provide user access to the AWS Management Console"
5. Click "Next: Permissions"
6. Click "Attach policies directly"
7. Create a new policy (Button in Policy section)
8. On the next page, choose JSON in the Policy Editor
9. Copy and paste the following
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
         "Resource": [
           "arn:aws:s3:::YOUR-BUCKET-NAME",
           "arn:aws:s3:::YOUR-BUCKET-NAME/*"
         ]
       }
     ]
   }
   ```
   (Replace `YOUR-BUCKET-NAME` with your actual bucket name)
10. Give the policy a name (e.g., "S3UploadAccess")
11. Attach this policy to your user
12. Complete the user creation
13. **IMPORTANT**: Save the Access Key ID and Secret Access Key - these are your credentials for the .env file

## Project Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your AWS credentials:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file with your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_REGION=your_aws_region
   S3_BUCKET_NAME=your_bucket_name
   ```
5. Update the configuration variables in `src/s3_uploader.py`:
   - `DATA_FOLDER`: Path to your JSON files
   - `UPLOAD_INTERVAL`: Time between uploads in seconds

## Usage

Run the script:

```bash
python src/s3_uploader.py
```

The script will:

1. Load AWS credentials from the .env file
2. Connect to your S3 bucket
3. Randomly select a JSON file from the specified folder
4. Upload it to the S3 bucket
5. Wait for the specified interval
6. Repeat the process

## Project Structure

```
.
├── data-news-articles/     # Folder containing JSON files to upload
├── src/
│   └── s3_uploader.py     # Main script
├── .env                   # AWS credentials (not in version control)
├── .env.example          # Template for .env file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your AWS credentials secure
- Use appropriate IAM roles and permissions for S3 access
