import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.subplots as sp
from text_func import *
from dictionary import *
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import ast
import regex as re

df_1 = pd.read_csv('linkedin_jobs.csv')
df_1[['job_description_unigram', 'job_description_bigram']] = df_1[['job_description_unigram', 'job_description_bigram']].applymap(ast.literal_eval)
df_1['posting_date'] = pd.to_datetime(df_1['posting_date'])
columns_to_display = ['company', 'posting_date', 'job_title', 'seniority_level', 'job_function', 'industries']
df_1 = df_1.drop_duplicates(subset=columns_to_display)

# Flatten the list of tokens
token_1 = [token for tokens in df_1['job_description_unigram'] for token in tokens]
token_2 = [token for tokens in df_1['job_description_bigram'] for token in tokens]

# Convert bigram tuples to a single string
bigram_strings = [' '.join(bigram) for bigram in token_2]

# Count the frequency of each token
token_counts_1 = Counter(token_1)
token_counts_2 = Counter(bigram_strings)

#============================FIRST DASHBOARD=============================
# Define the plot_wordcloud function with font size scaling
def plot_wordcloud(data, font_scaling_factor=10):
    wc = WordCloud(width=800, 
                   height=800,
                   background_color='white',
                   stopwords=None,
                   min_font_size=10)
    
    # Scale the font size based on frequency
    scaled_data = {word: freq * font_scaling_factor for word, freq in data.items()}
    
    wc.generate_from_frequencies(scaled_data)
    return wc

#============================SECOND DASHBOARD=============================
# Initialize a result dictionary
result = {}

# Iterate over your dictionary
for category, words in classification_dict.items():
    # Initialize a dictionary for the category
    category_dict = {}
    
    # Iterate over the words in the category
    for word in words:
        # Count the occurrences of the word in the 'job_description' column
        category_dict[word] = df_1['job_description'].astype(str).apply(lambda x: len(re.findall(rf'\b{word}\b', x, re.IGNORECASE))).sum()
    
    # Convert the category dictionary to a DataFrame and store it in the result dictionary
    result[category] = pd.DataFrame(list(category_dict.items()), columns=['Word', 'Count'])

pl = result['programming_languages'][result['programming_languages']['Count'] > 0]
mlt = result['machine learning task'][result['machine learning task']['Count']>0]
db = result['database'][result['database']['Count']>0]
cp = result['cloud platform'][result['cloud platform']['Count']>0]
mla = result['machine learning algorithm'][result['machine learning algorithm']['Count']>0]

# Add title above select tab
st.set_page_config(layout="wide")
st.title("Job Description Dashboard")

selected_industries = st.multiselect('Select Industries', df_1['industries'].explode().unique())
selected_seniority = st.multiselect('Select Seniority Levels', df_1['seniority_level'].unique())

# Create tabs
tab1, tab2 = st.tabs(["Job Analysis", "Job Specification"])

# Filter the dataframe based on selected job description and seniority
filtered_df = df_1.copy()
if selected_industries:
    filtered_df = filtered_df[filtered_df['industries'].apply(lambda x: any(word in x for word in selected_industries))]
if selected_seniority:
    filtered_df = filtered_df[filtered_df['seniority_level'].isin(selected_seniority)]

# Generate word cloud for the filtered dataframe
token_1 = [token for tokens in filtered_df['job_description_unigram'] for token in tokens]
token_2 = [token for tokens in filtered_df['job_description_bigram'] for token in tokens]

# Convert bigram tuples to a single string
bigram_strings = [' '.join(bigram) for bigram in token_2]

# Count the frequency of each token
token_counts_1 = Counter(token_1)
token_counts_2 = Counter(bigram_strings)

# Get the top 10 words and their counts in descending order
top_10_words = dict(sorted(token_counts_1.items(), key=lambda item: item[1], reverse=True)[:10])

with tab1:
    st.title("Word Cloud of Job Description")
    st.image(plot_wordcloud(data=token_counts_1).to_image())

    # Make the bar chart horizontal and sorted in descending order
    st.title("Word Occurence of Job Description")
    st.bar_chart(pd.Series(top_10_words).sort_values(ascending=False), use_container_width=True)

    # Display DataFrame as table
    st.title("Job Data")
    st.table(filtered_df.head(20)[columns_to_display])
with tab2:
    for category, words in classification_dict.items():
        # Initialize a dictionary for the category
        category_dict = {}
        
        # Iterate over the words in the category
        for word in words:
            # Count the occurrences of the word in the 'job_description' column
            category_dict[word] = filtered_df['job_description'].astype(str).apply(lambda x: len(re.findall(rf'\b{word}\b', x, re.IGNORECASE))).sum()
        
        # Convert the category dictionary to a DataFrame and store it in the result dictionary
        result[category] = pd.DataFrame(list(category_dict.items()), columns=['Word', 'Count'])

    pl = result['programming_languages'][result['programming_languages']['Count'] > 0]
    mlt = result['machine learning task'][result['machine learning task']['Count']>0]
    db = result['database'][result['database']['Count']>0]
    cp = result['cloud platform'][result['cloud platform']['Count']>0]
    mla = result['machine learning algorithm'][result['machine learning algorithm']['Count']>0]
    stat = result['statistics'][result['statistics']['Count']>0]

    # Create individual pie charts without legend
    fig1 = go.Figure(go.Pie(labels=pl['Word'], values=pl['Count'], textinfo='label+percent', showlegend=False))
    fig1.update_layout(title_text='Programming Languages Used by Data Scientist')

    fig2 = go.Figure(go.Pie(labels=mlt['Word'], values=mlt['Count'], textinfo='label+percent', showlegend=False))
    fig2.update_layout(title_text='Machine Learning Tools Used by Data Scientist')

    fig3 = go.Figure(go.Pie(labels=mla['Word'], values=mla['Count'], textinfo='label+percent', showlegend=False))
    fig3.update_layout(title_text='Machine Learning Algorithms Used by Data Scientist')

    fig4 = go.Figure(go.Pie(labels=db['Word'], values=db['Count'], textinfo='label+percent', showlegend=False))
    fig4.update_layout(title_text='Databases Used by Data Scientist')

    fig5 = go.Figure(go.Pie(labels=cp['Word'], values=cp['Count'], textinfo='label+percent', showlegend=False))
    fig5.update_layout(title_text='Cloud Platforms Used by Data Scientist')

    fig6 = go.Figure(go.Pie(labels=stat['Word'], values=cp['Count'], textinfo='label+percent', showlegend=False))
    fig6.update_layout(title_text='Statistics Technique Used by Data Scientist')

    # Display pie charts with 3 charts per row, centered
    num_charts = 3
    num_rows = (len([fig1, fig2, fig3, fig4, fig5, fig6]) + num_charts - 1) // num_charts

    for i in range(num_rows):
        charts_in_row = [fig1, fig2, fig3, fig4, fig5, fig6][i * num_charts : (i + 1) * num_charts]
        cols = st.columns(num_charts)
        for col, chart in zip(cols, charts_in_row):
            with col:
                st.plotly_chart(chart, use_container_width=True, centered=True)