Amazon Product Reviews Sentiment Analysis
Overview
This project aims to perform sentiment analysis on Amazon product reviews, specifically focusing on reviews for Amazon Alexa devices. Using the provided amazon_alexa.tsv data file, the analysis includes data preprocessing, sentiment analysis, and visualization of the results.



Features
Data preprocessing to clean and prepare the review data.
Sentiment analysis using natural language processing (NLP) techniques.
Visualization of sentiment distribution and insights.
Requirements
Python 3.6+
Pandas library
NLTK (Natural Language Toolkit) library
Matplotlib library
Seaborn library
Installation
Clone the repository:




Copy code
git clone https://github.com/yourusername/amazon-reviews-sentiment-analysis.git
cd amazon-reviews-sentiment-analysis
Install the required Python packages:



Copy code
Download the dataset:
The dataset is available in the Github Repository.



Ensure the amazon_alexa.tsv file is correctly placed in the project directory.
Run the Analysis:



Copy code
jupyter notebook sentiment_analysis.ipynb
Open the Jupyter Notebook and run all cells to perform the sentiment analysis.
Output:



The notebook will generate visualizations and insights on the sentiment of the product reviews.
Data Explanation
Dataset: amazon_alexa.tsv
The dataset contains reviews for Amazon Alexa devices with the following columns:



rating: The rating given by the user.
date: The date of the review.
variation: The variation of the product.
verified_reviews: The text of the review.
feedback: Whether the feedback was positive (1) or negative (0).
