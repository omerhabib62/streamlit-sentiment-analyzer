import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px

# --- PAGE CONFIG ---
# Set the page configuration. This is the first Streamlit command.
st.set_page_config(
    page_title="Web Scraper & Sentiment Analyzer",
    page_icon="🔎",
    layout="wide"
)

# --- 1. THE SCRAPER ENGINE (CS Skill) ---
@st.cache_data(ttl=3600)  # Cache data for 1 hour to prevent re-scraping
def scrape_reviews(url):
    """
    Scrapes all review text from a given URL.
    This example is built for 'books.toscrape.com'.
    """
    try:
        # Use a user-agent to pretend to be a real browser
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for bad responses (404, 500)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is the "magic" part. We find all HTML tags that match our target.
        # For books.toscrape.com, the book titles are in an 'a' tag, inside an 'h3' tag.
        review_articles = soup.find_all('article', class_='product_pod')
        
        # Extract the "title" of the book (which we'll treat as a "review" for this demo)
        reviews = [article.find('h3').find('a')['title'] for article in review_articles]
        
        if not reviews:
            st.warning("No reviews found. Check the URL or the HTML tags.")
            return []
            
        return reviews
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error scraping URL: {e}")
        return None

# --- 2. THE ANALYZER ENGINE (BA Skill) ---
@st.cache_data  # Cache the analysis results
def analyze_sentiment(text_list):
    """
    Analyzes a list of text strings and returns their sentiment.
    """
    # Initialize the VADER analyzer
    analyzer = SentimentIntensityAnalyzer()
    results = []
    
    for text in text_list:
        # Get the polarity scores
        score = analyzer.polarity_scores(text)
        
        # The "compound" score is what matters: -1 (v. neg) to +1 (v. pos)
        compound = score['compound']
        
        # Classify the sentiment based on the compound score
        if compound >= 0.05:
            sentiment = 'Positive'
        elif compound <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
            
        results.append({
            'Review Text': text,
            'Sentiment': sentiment,
            'Score': compound
        })
        
    # Return as a Pandas DataFrame
    return pd.DataFrame(results)

# --- 3. THE STREAMLIT UI ---
st.title("🔎 Web Scraper & Sentiment Analyzer")
st.markdown("A portfolio project demonstrating web scraping (Requests/BeautifulSoup) and NLP (VaderSentiment) in a Streamlit app.")

# --- Input Box ---
st.header("1. Enter a URL to Scrape")
st.markdown("*(This demo is built to scrape `books.toscrape.com`. It will not work on all sites like Amazon or Yelp, which require more advanced scraping.)*")
default_url = "http://books.toscrape.com/"
url_to_scrape = st.text_input("Enter URL:", default_url)

if st.button("Analyze Sentiment"):
    if not url_to_scrape:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Scraping website and analyzing sentiment... This may take a moment."):
            # --- Run the Engines ---
            scraped_reviews = scrape_reviews(url_to_scrape)
            
            if scraped_reviews:
                sentiment_df = analyze_sentiment(scraped_reviews)
                
                st.success(f"Done! Analyzed {len(sentiment_df)} reviews.")
                
                # --- 4. DISPLAY RESULTS (The Dashboard) ---
                st.header("2. Sentiment Analysis Results")
                
                # --- KPIs ---
                total_reviews = len(sentiment_df)
                positive_count = len(sentiment_df[sentiment_df['Sentiment'] == 'Positive'])
                neutral_count = len(sentiment_df[sentiment_df['Sentiment'] == 'Neutral'])
                negative_count = len(sentiment_df[sentiment_df['Sentiment'] == 'Negative'])
                
                # Calculate percentages
                pos_perc = (positive_count / total_reviews) * 100
                neu_perc = (neutral_count / total_reviews) * 100
                neg_perc = (negative_count / total_reviews) * 100

                st.subheader("High-Level Summary")
                kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
                kpi_col1.metric("Positive", f"{pos_perc:.1f}%", f"{positive_count} Reviews")
                kpi_col2.metric("Neutral", f"{neu_perc:.1f}%", f"{neutral_count} Reviews")
                kpi_col3.metric("Negative", f"{neg_perc:.1f}%", f"{negative_count} Reviews")

                # --- Plotly Pie Chart ---
                st.subheader("Sentiment Breakdown")
                fig = px.pie(
                    sentiment_df, 
                    names='Sentiment', 
                    title='Sentiment of Scraped Reviews',
                    color='Sentiment',
                    color_discrete_map={
                        'Positive': 'green',
                        'Neutral': 'gray',
                        'Negative': 'red'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)

                # --- Data Table ---
                st.subheader("Analyzed Data")
                st.markdown("View the raw text and its sentiment score (-1 is Negative, +1 is Positive).")
                # We use width='stretch' to fill the container
                st.dataframe(sentiment_df.sort_values(by="Score", ascending=False), width='stretch')