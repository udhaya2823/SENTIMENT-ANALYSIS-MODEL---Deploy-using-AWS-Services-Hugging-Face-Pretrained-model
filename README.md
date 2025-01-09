# 🚀Sentiment Analysis Model Deployment using AWS and Streamlit/Gradio

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Data](#data)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Deployment](#deployment)
- [Evaluation Metrics](#evaluation-metrics)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Introduction
This project focuses on deploying a **Sentiment Analysis Model** using AWS services and making it accessible through a web application built with **Streamlit** or **Gradio**. It utilizes a fine-tuned or pre-trained sentiment analysis model to classify tweets into three categories: **Positive**, **Negative**, and **Neutral**.

The deployment includes setting up AWS infrastructure, ensuring security, and enabling scalability for multiple users.

---

## Features
- Entity-level sentiment analysis for tweets.
- Web interface for user interaction (Streamlit or Gradio).
- AWS-based deployment for scalability and robustness.
- Storage of user login data using Amazon RDS.
- Secure and optimized environment configuration.

---

## Tech Stack
- **Machine Learning**: Transformers, Hugging Face models
- **Web Framework**: Streamlit or Gradio
- **AWS Services**: S3, EC2, RDS, IAM
- **Database**: Amazon RDS (PostgreSQL)
- **Programming Language**: Python
- **Version Control**: Git

---

## Data
Dataset: [Twitter Training Dataset](https://raw.githubusercontent.com/GuviMentor88/Training-Datasets/refs/heads/main/twitter_training.csv)

### Dataset Fields
1. **Tweet ID**: Unique identifier for each tweet.
2. **Entity**: The topic or entity associated with the tweet.
3. **Sentiment**: Sentiment classification (Positive, Negative, Neutral).
4. **Tweet Content**: The actual text of the tweet.

---

## Setup Instructions
### Prerequisites
1. Python 3.8+ installed.
2. AWS Account with access to S3, EC2, and RDS.
3. AWS CLI configured on your local system.
4. Git installed.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sentiment-analysis-aws.git
   cd sentiment-analysis-aws
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up AWS infrastructure:
   - Launch an **EC2 instance** with appropriate IAM roles and security groups.
   - Create an **S3 bucket** and upload the fine-tuned model.
   - Configure an **RDS instance** for storing user login data.
4. Configure environment variables:
   - Add AWS credentials and database configurations in a `.env` file.
5. Deploy the web app:
   ```bash
   streamlit run app.py
   ```
   or
   ```bash
   python -m gradio app.py
   ```

---

## Project Structure
```
sentiment-analysis-aws/
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── model/                # Fine-tuned model files
├── scripts/              # Scripts for data processing and setup
├── data/                 # Sample dataset
├── README.md             # Project documentation
└── .env                  # Environment variables (not included in repo)
```

---

## Usage
1. Open the deployed web application in a browser.
2. Enter a tweet and select an entity.
3. View the sentiment classification results.

---

## Deployment
### AWS Steps
1. Upload the fine-tuned model and `app.py` to an **S3 bucket**.
2. Launch an **EC2 instance** and configure it to access the S3 bucket.
3. Install required dependencies on the EC2 instance:
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip install -r requirements.txt
   ```
4. Set up the **Streamlit/Gradio app** to run on a public-facing port.
5. Configure a **security group** to allow inbound traffic on the application port (default: 8501).

---

## Evaluation Metrics
- **Accuracy**: Measure of correct predictions.
- **Precision**: Proportion of relevant instances among retrieved instances.
- **Recall**: Proportion of relevant instances retrieved.
- **F1-Score**: Harmonic mean of precision and recall.
- **Response Time**: Time taken to process a user query.

---

## Future Enhancements
- Integrate more AWS services like Lambda for serverless computing.
- Expand the dataset for multi-language sentiment analysis.
- Enable real-time sentiment tracking using a live Twitter API.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
