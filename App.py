# Importing required libraries
import boto3  # AWS SDK for Python to interact with AWS services
import os  # For file and directory handling
import pymysql  # For interacting with MySQL databases
import torch  # PyTorch for machine learning
import torch.nn.functional as F  # For softmax function
from transformers import AutoTokenizer, AutoModelForSequenceClassification  # For NLP models
import gradio as gr  # For creating a user interface
from datetime import datetime  # For working with timestamps (not directly used here)

# AWS S3 Configuration
BUCKET_NAME = "finalprojectuk"  # Name of the S3 bucket
MODEL_S3_FOLDER = "fine_tuned_distilbert/"  # Folder in the bucket containing the model files
LOCAL_MODEL_DIR = "fine_tuned_distilbert"  # Local directory to store downloaded model files

# RDS Configuration
RDS_HOST = "finalprojectdb.cv8o0cuu06nc.ap-south-1.rds.amazonaws.com"  # RDS endpoint
RDS_USER = "admin"  # Database username
RDS_PASSWORD = "Iamudhaya23"  # Database password
RDS_DB = "user_logs"  # Database name

# Function to download all files in a folder from S3
def download_model_from_s3():
    try:
        # Initialize the S3 client
        s3 = boto3.client("s3")
        
        # Create the local directory if it doesn't exist
        if not os.path.exists(LOCAL_MODEL_DIR):
            os.makedirs(LOCAL_MODEL_DIR)

        # List all objects in the specified S3 folder
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=MODEL_S3_FOLDER)
        if 'Contents' not in response:  # If no files are found in the folder
            raise Exception(f"No files found in S3 folder: {MODEL_S3_FOLDER}")

        # Download each file from the S3 folder
        for obj in response['Contents']:
            s3_file_path = obj['Key']  # Full path (key) of the file in S3
            file_name = os.path.basename(s3_file_path)  # Extract only the file name
            local_file_path = os.path.join(LOCAL_MODEL_DIR, file_name)  # Local path for the file

            # Skip folders or empty keys
            if not file_name:
                continue

            # Download the file from S3 to the local path
            s3.download_file(BUCKET_NAME, s3_file_path, local_file_path)
            print(f"Downloaded: {file_name} to {local_file_path}")
    except Exception as e:
        # Print and raise any errors encountered
        print(f"Error downloading model from S3: {e}")
        raise

# Download and organize model files
download_model_from_s3()

# Load the pre-trained model and tokenizer
MODEL_PATH = LOCAL_MODEL_DIR  # Path to the downloaded model files
try:
    # Load tokenizer for processing input text
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    
    # Load the model for sequence classification
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, trust_remote_code=True)
    print("Model and tokenizer loaded successfully!")
except Exception as e:
    # Handle errors during model or tokenizer loading
    print(f"Error loading model or tokenizer: {e}")
    raise

# Function to connect to the RDS database
def get_db_connection():
    try:
        # Establish connection to the RDS database
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB,
            autocommit=True  # Automatically commit changes
        )
        return connection
    except Exception as e:
        # Handle database connection errors
        print(f"Error connecting to RDS: {e}")
        raise

# Function to log prediction results to the RDS database
def log_prediction_to_rds(text, predicted_class, negative, neutral, positive, ip_address):
    try:
        # Get a database connection
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # SQL query to insert prediction results
            query = """
            INSERT INTO APP_USER_LOGS (Text, Predicted_class, Negative, Neutral, Positive, ip_address)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            # Execute the query with the given values
            cursor.execute(query, (text, predicted_class, negative, neutral, positive, ip_address))
    except Exception as e:
        # Print any errors encountered during logging
        print(f"Error logging to RDS: {e}")
    finally:
        # Ensure the connection is closed after use
        if 'connection' in locals():
            connection.close()

# Function to predict sentiment based on input text
def predict_sentiment(text, request: gr.Request):
    try:
        # Get the client's IP address from the request
        ip_address = request.client.host
        
        # Preprocess the input text using the tokenizer
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)  #pt = pytorch
        
        # Perform inference with the model
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Calculate probabilities for each sentiment class
        probs = F.softmax(outputs.logits, dim=-1)

        # Get the predicted class (0, 1, 2) and map it to (1, 2, 3)
        predicted_class = torch.argmax(probs, dim=1).item() + 1
        
        # Extract probabilities for each class
        neutral, positive, negative = probs[0].tolist()
        
        # Prepare the result to return
        result = {
            "Predicted Class": predicted_class,
            "Negative": round(negative, 4),
            "Neutral": round(neutral, 4),
            "Positive": round(positive, 4),
        }

        # Log the prediction results to the RDS database
        log_prediction_to_rds(text, predicted_class, negative, neutral, positive, ip_address)
        
        return result  # Return the prediction result
    except Exception as e:
        # Handle errors during prediction
        print(f"Error during prediction: {e}")
        return {"error": str(e)}

# Create a Gradio interface for the sentiment analysis application
iface = gr.Interface(
    fn=predict_sentiment,  # Function to call when user interacts
    inputs=gr.Textbox(lines=2, placeholder="Enter tweets here..."),  # User input: a text box
    outputs=gr.JSON(),  # Output: JSON showing prediction results
    title="Twitter Tweets Sentiment Analysis",  # Title of the app
    description="Enter Tweets and get the predicted sentiment class and probabilities.",  # Description
)

# Launch the Gradio interface
iface.launch(share=True)  # Allow public sharing with a unique link