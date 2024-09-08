# Reddit-Data-Pipeline
This project implements a complete ETL (Extract, Transform, Load) pipeline using a variety of technologies to process and analyze Reddit data.
## Features
<b>Data Extraction</b>: Utilizes the Reddit API to extract posts and comments. \
<b>Data Loading</b>: Stores the extracted data in an AWS S3 bucket. \
<b>Data Warehousing</b>: Copies the data from S3 into an AWS Redshift cluster for further analysis. \
<b>Data Transformation</b>: Uses dbt (Data Build Tool) to transform and model the data in Redshift. \
<b>Data Visualization</b>: Creates a dashboard in Google Data Studio to visualize insights from the data. \
<b>Orchestration</b>: Orchestrates the entire workflow using Apache Airflow, running in a Docker container. \
<b>Infrastructure as Code</b>: Automates the creation and management of AWS resources (S3 bucket, Redshift cluster, IAM roles, security groups) using Terraform.
## Architecture
<img width="574" alt="workflow" src="https://github.com/user-attachments/assets/4812bce9-d757-41a9-b5b6-71733d229cea">

## Prerequisites
• AWS account with S3, Redshift, and IAM permissions \
• Docker \
• Terraform \
• Python with necessary libraries \
• Google Data Studio account

## Output
This pipeline provides an end-to-end solution for extracting, transforming, and visualizing Reddit data, offering valuable insights through a dashboard.
![RedditApiPipeline_Dashboard (1)-1](https://github.com/user-attachments/assets/2df170c3-dcf1-4f60-92a2-e0cbfdfcad6f)
I initiated the pipeline on August 17, 2024. It would be more insightful to run it over a longer period, such as an entire week, to capture more data and provide a richer view on the dashboard. Feel free to explore and adjust the timing as you see fit.
