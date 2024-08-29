# -*- coding: utf-8 -*-
"""P1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1keJyxmZVBPW0jKB_d2x7SWe6ygjSFhGW
"""

# Import necessary libraries
import pandas as pd
import numpy as np


df=pd.read_csv('Youtube-Spam-Dataset.csv')
df.head()

# Check for missing values
df.isnull().sum()

# Drop rows with missing values
df.dropna(inplace=True)

# Distribution of spam vs non-spam comments
plt.figure(figsize=(6,4))
sns.countplot(x='CLASS', data=df)
plt.title('Distribution of Spam vs Non-Spam Comments')
plt.xlabel('Class (0: Non-Spam, 1: Spam)')
plt.ylabel('Count')
plt.show()

# Convert the 'DATE' column to datetime
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

# Extract features from the 'DATE' column
df['YEAR'] = df['DATE'].dt.year
df['MONTH'] = df['DATE'].dt.month
df['DAY'] = df['DATE'].dt.day
df['HOUR'] = df['DATE'].dt.hour

# Select only numeric columns for correlation analysis
numeric_df = df.select_dtypes(include=[np.number])
plt.figure(figsize=(10,8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

# Vectorize the 'CONTENT' column using TF-IDF
tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
X = tfidf.fit_transform(df['CONTENT'])
y = df['CLASS']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Shape of X_train: ", X_train.shape)
print("Shape of X_test: ", X_test.shape)

# Train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Display the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Display the classification report
print(classification_report(y_test, y_pred))


import streamlit as st
import cohere


# Initialize Cohere client
co = cohere.Client('pGbElaDbFkEHelKRVKyQG6QoTB14XF4iQ0iOMEqP')


def fetch_comments(video_id):
    comments = []
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    for item in results['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return comments

def detect_spam(comment):
    response = co.classify(
        model='large',  # Change to your specific model if needed
        inputs=[comment]
    )
    return response.classifications[0].prediction == 'spam'

# Streamlit UI
st.title("YouTube Comment Spam Detector")

video_id = st.text_input("Enter YouTube Video ID:")

if video_id:
    comments = fetch_comments(video_id)
    st.write("Fetched Comments:")
    for comment in comments:
        is_spam = detect_spam(comment)
        st.write(f"Comment: {comment}")
        st.write(f"Spam: {'Yes' if is_spam else 'No'}")
