import streamlit as st
from streamlit_option_menu import option_menu
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import torch
import datetime
#connection for mysql database
import mysql.connector
mydb = mysql.connector.connect(host="database-1.c98ye0wu4lb7.ap-south-1.rds.amazonaws.com",
                               user="admin",
                               password="RajaHari190699",
                               port=3306)
mycursor = mydb.cursor(buffered=True)

#streamlit page configure
st.set_page_config(page_title="Sentiment Analysis",
                   page_icon=":flag-sa:",
                   layout="wide")


# Initialize the model and tokenizer
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

# Predict sentiment function
def predict_sentiment(text):
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')

    with torch.no_grad():  # Ensure no gradients are computed
        output = model(**encoded_input)

    logits = output.logits.detach().numpy()[0]
    scores = softmax(logits)

    # Format results
    ranking = np.argsort(scores)[::-1]
    result = ""
    for i in range(scores.shape[0]):
        label = config.id2label[ranking[i]]
        score = scores[ranking[i]]
        result += f"{i+1}) {label} {np.round(float(score), 4)}\n"

    return result

def save(name):
    dt=datetime.datetime.now()
    mycursor.execute("create database if not exists sentiment")
    mycursor.execute("use sentiment")

    mycursor.execute("create table if not exists userinfo(ID int AUTO_INCREMENT PRIMARY KEY,Name varchar(255),Time Datetime)")
    query='''insert into userinfo(Name,Time) Values(%s,%s)'''
    mycursor.execute(query,(name,dt))
    mydb.commit()
    return st.write("Your Entry is Registered")

# Streamlit interface
selected = option_menu(None, ["Home", 'Analysis','Documentation'], 
           icons=['house', 'activity'], menu_icon="cast",
           orientation="horizontal")

#Home
if selected=="Home":
    st.title(":red[Welcome to Sentiment Analysis]")
    st.write("")

    st.markdown("## :green[About Sentiment Analysis]")
    st.markdown("#### 👉 Sentiment analysis is a technique used to determine the emotional tone behind a series of words.")
    st.markdown("#### 👉 It involves analyzing text data like reviews, social media posts, or customer feedback to classify it as :rainbow[Positive], :rainbow[Negative], or :rainbow[Neutral].")
    st.markdown("#### 👉 This helps businesses understand customer opinions, track brand sentiment, and gauge public reaction to events or products.")
    st.write("")
    st.markdown("## :green[Project's Problem Statements]")
    st.markdown("#### 🚩 The task is to deploy a Machine Learning or Deep learning or Pretrained or Fine Tuned sentiment analysis model.")
    st.markdown("#### 🚩 The deployment should leverage AWS services like S3, EC2, RDS")
    st.markdown("#### 🚩 Make it accessible through a web application built with Streamlit or Gradio.")
    st.write("")
    st.markdown("## :green[Project Preperation]")
    st.markdown("#### ✔️ A Pretrained :red[RoBERTA-base] Sentiment Analysis model is utilised,")
    st.markdown("#### ✔️ AWS :red[S3] for storing the model and application files,")
    st.markdown("#### ✔️ AWS :red[EC2] for running the application,")
    st.markdown("#### ✔️ AWS :red[RDS] database for storing username and login time,")
    st.markdown("#### ✔️ Build with :red[Streamlit] web application.")

#Analysis
if selected=="Analysis":
    st.title(":red[Welcome to Sentiment Analysis]")

    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'name_saved' not in st.session_state:
        st.session_state.name_saved = False

    Name=st.text_input("Please Sign up by entering your name",value=st.session_state.name)

    if Name.strip():
        st.session_state.name = Name

        if not st.session_state.name_saved:
            save(Name)
            st.session_state.name_saved = True 
            st.markdown(f"##### :green[Hello {Name} 🤗, you are now gained access to do Sentiment Analysis ✔️]")

        # Text input from the user
        user_input = st.text_area("Enter Text", height=100)

        # Display results when the button is clicked
        if st.button("Analyze Sentiment"):
            if user_input:
                sentiment_result = predict_sentiment(user_input)
                st.text_area("Sentiment Analysis Results", value=sentiment_result, height=100)
            else:
                st.warning("Please enter some text to analyze.")
    else:
        st.warning("Please Enter your name to proceed further")

#documentation

if selected=="Documentation":
    st.markdown("## :blue[Objective]")
    st.markdown("#### 📢 To deploy Pretrained sentiment analysis model using AWS, making it accessible through a web application built with Streamlit")

    st.markdown("## :blue[Model Preperation]")
    st.markdown("#### 📢 Utilized a appropriate pretrained model from huggingface models.")
    st.write("")

    st.markdown("## :blue[Infrastructure Setup]")
    st.markdown("#### 📢 Launched an Amazon EC2 instance with appropriate IAM roles and security groups.")
    st.markdown("#### 📢 Ensured that EC2 instance has internet access via an Internet Gateway.")
    st.markdown("#### 📢 Created an S3 storage bucket to store app.py file.")
    st.write("")

    st.markdown("## :blue[Environment Configurations]")
    st.markdown("#### 📢 Installed required packages on EC2 instance like mysqlconnector,transformers,torch,streamlit,python,pip,scipy.")
    st.markdown("#### 📢 Coded to download app.py file from S3 bucket.")
    st.write("")

    st.markdown("## :blue[Database Setup]")
    st.markdown("#### 📢 Setted up an Amazon RDS database instance to store user information (username and login time).")
    st.write("")

    st.markdown("## :blue[Security Configurations]")
    st.markdown("#### 📢 Configured a security group to allow inbound traffic on the port used by the web application (default: 8501 for Streamlit).")
    st.write("")
    
    st.markdown("## :blue[Application Deployment]")
    st.markdown("#### 📢 Run the Streamlit application on the EC2 instance which is stored in S3.")