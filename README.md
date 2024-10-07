
# Project Title

Sentiment Analysis using AWS

This project is useful in analyzing text data like reviews, social media posts, or customer feedback to classify it as Positive, Negative, or Neutral.




## Packages

Python

streamlit

transformers

torch

mysql.connector

scipy
## Intro

This Sentiment Analysis Project is prepared by using RoBERTA model Transformers and deployed in the Streamlit web app utilizing AWS S3, RDS and EC2.
## Scope of Work

1. Preperation and Preprocessing:

Utilized a appropriate pretrained model from huggingface models. here it is ROBERTA .

2. Infrastructure Setup:

Launched an Amazon EC2 instance with appropriate IAM roles and security groups.Ensured that EC2 instance has internet access via an Internet Gateway.Created an S3 storage bucket to store app.py file.

3. Environment Configurations:

Installed required packages on EC2 instance like mysqlconnector,transformers,torch,streamlit,python,pip,scipy.Coded to download app.py file from S3 bucket.

4. Database Setup:

Setted up an Amazon RDS database instance to store user information (username and login time).A requirement of this project. Gave connection with mysql.connector with relevent host,user,password and port.

5. Security Configurations:

Configured a security group to allow inbound traffic on the port used by the web application (default: 8501 for Streamlit),(3306 for AWS RDS).

6. Application Deployment:

Run the Streamlit application on the EC2 instance which is stored in S3.

7. Internet access

By putting the external link which is given in the ec2 terminal or open address link in the ec2 instance we can view the streamlit app.


## Note

As this ROBERTA model used here is a LLM so to run this in the AWS EC2 it requires a paid version of large package which will include atleast 8gb of ROM and 12 gb ROM. SAme if it is a local system.