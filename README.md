# Web Scraper & Sentiment Analysis (NLP) Dashboard

🔴 LIVE APP: https://omer-sentiment-app.streamlit.app

![Sentiment Dashboard Screenshot](https://raw.githubusercontent.com/omerhabib62/streamlit-sentiment-analyzer/main/sentiment_screenshot.png)

1. Project Overview

This is an advanced portfolio project that demonstrates my ability to handle external, unstructured web data and perform AI/NLP analysis.

This app scrapes a given URL, extracts all review text, and then performs real-time sentiment analysis (using NLP) to classify each review as "Positive," "Negative," or "Neutral." It then presents the results in a high-level executive dashboard.

This is the "engine" for a powerful tool that could analyze competitor reviews, product feedback, or social media mentions.

2. Features

🔎 Live Web Scraper: User inputs a URL, and the app scrapes the data in real-time.

🤖 NLP Sentiment Analysis: Uses vaderSentiment to analyze the text and classify it.

📊 KPI Dashboard: Instantly calculates the % breakdown of Positive, Neutral, and Negative reviews.

📈 Interactive Pie Chart: A Plotly chart for a clear visual breakdown of sentiment.

📄 Data Table: Shows the raw review text and its corresponding sentiment score.

3. Tech Stack

This project proves my expertise in:

Python: The core logic.

Web Scraping: Requests (for HTTP) and BeautifulSoup4 (for HTML parsing).

NLP (Natural Language Processing): vaderSentiment for fast, accurate sentiment analysis.

Streamlit: For the interactive web UI and running the full pipeline.

Pandas: For organizing the final data.

Plotly: For the pie chart visualization.

4. How to Run Locally

Clone this repository: git clone [YOUR_REPO_URL]

Navigate to the folder: cd streamlit-sentiment-analyzer

Install dependencies: pip install -r requirements.txt

Run the app: streamlit run app.py
