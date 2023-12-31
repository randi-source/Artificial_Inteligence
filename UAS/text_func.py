import pandas as pd
import numpy as np
import nltk

import requests
from bs4 import BeautifulSoup
import math
import time

from nltk.tokenize import word_tokenize
from langdetect import detect
from datetime import datetime
from nltk.util import ngrams

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('sentiwordnet')

pd.options.mode.chained_assignment = None

#=======================================WEB SCRAPING============================================

def scrape_linkedin_jobs(number_of_jobs, exact_match):
    l=[]
    o={}
    k=[]

    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%2Bscientist&location=Indonesia&geoId=102478259&currentJobId=3787773447&start={}'

    number_of_loops = math.ceil(number_of_jobs/25)

    for i in range(0,number_of_loops):
        res = requests.get(target_url.format(i))
        soup=BeautifulSoup(res.text,'html.parser')
        alljobs_on_this_page=soup.find_all("li")
        print(len(alljobs_on_this_page))
        for x in range(0,len(alljobs_on_this_page)):
            jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
            l.append(jobid)
        time.sleep(1)

    target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

    for j in range(0,len(l)):
        resp = requests.get(target_url.format(l[j]))
        soup=BeautifulSoup(resp.text,'html.parser')
        try:
            o["company"]=soup.find("div",{"class":"top-card-layout__card relative p-2 papabear:p-details-container-padding"}).find("a").find("img").get('alt')
        except:
            o["company"]=None
        try:
            o["job_posting_time"]=soup.find('span', {"class":"posted-time-ago__text topcard__flavor--metadata"}).text.strip()
        except:
            o["job_posting_time"]=None
        try:
            o["number_applicant"]=soup.find('span',{"class":"num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"})
            
            if o["number_applicant"] is not None:
                o["number_applicant"]=soup.find('span',{"class":"num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"}).text.strip().replace(" applicants","")
            else: 
                o["number_applicant"]=soup.find('figcaption', {"class": "num-applicants__caption"}).text.strip().replace("Over 200 applicants", "200")
        except:
            o["number_applicant"]=None
        try:
            o["job_title"]=soup.find("div",{"class":"top-card-layout__entity-info flex-grow flex-shrink-0 basis-0 babybear:flex-none babybear:w-full babybear:flex-none babybear:w-full"})\
                .find("a").find("h2").text.strip()
        except:
            o["job_title"]=None
        try:
            job_description = soup.find("div", {"class":"description__text description__text--rich"}).find("section").find("div").find_all("ul")
            bullet_opt = ' '.join([li.text for ul in job_description for li in ul.find_all('li')])
            o["job_description"] = bullet_opt
        except:
            o["job_description"]=None
        try:
            # Find the <li> elements by class name
            li_elements = soup.find("ul",{"class":"description__job-criteria-list"}).find_all("li")

            # Loop through the <li> elements
            for li in li_elements:
                # Get the <h3> text
                h3_text = li.find('h3').text.strip()

                # If the <h3> text is 'Industries', 'Job function', or 'Seniority level'
                if h3_text in ['Industries', 'Job function', 'Seniority level']:
                    # Get the text within the <span>
                    value = li.find('span').text.strip()

                    # Assign the value to the corresponding key in the dictionary
                    o[h3_text.lower().replace(' ', '_')] = value
        except:
            o["industries"] = None
            o["job_function"] = None
            o["seniority_level"] = None
        k.append(o)
        o={}

    df = pd.DataFrame(k).dropna()

    if (exact_match):
        df = df[df['job_title'].str.contains('Data Scientist', case=False, na=False)]

    return df

#=======================================DATA CLEANSING============================================

def replace_description(df):
    df["job_description_prep"] = df["job_description"].replace("\s+", " ", regex=True).replace("[^-9A-Za-z ]", "", regex=True)
    return df

def add_language(df):
    df['language'] = df['job_description_prep'].apply(lambda text: detect(text) if text else None)
    return df

def filter_language(df):
    return df[df['language'] !='id']

def lower_case(df):
    df['job_description_prep'] = df['job_description_prep'].str.lower()
    return df

def tokenize(df):
    df['job_description_prep'] = df['job_description_prep'].apply(word_tokenize)
    return df

def remove_stopwords(df):
    stopwords = nltk.corpus.stopwords.words('english')
    df['job_description_prep'] = df['job_description_prep'].apply(lambda tokens: [token for token in tokens if token not in stopwords])
    return df

def lemmatize(df):
    lemmatizer = nltk.WordNetLemmatizer()
    df['job_description_prep'] = df['job_description_prep'].apply(lambda tokens: [lemmatizer.lemmatize(token) for token in tokens])
    return df

def to_timedelta(s):
    units = s.split(' ')
    if 'day' in units[1]:
        return pd.to_timedelta(int(units[0]), unit='d')
    elif 'week' in units[1]:
        return pd.to_timedelta(int(units[0])*7, unit='d')
    elif 'month' in units[1]:
        return pd.to_timedelta(int(units[0])*30, unit='d')

def add_posting_date(df):
    df['timedelta'] = df['job_posting_time'].apply(to_timedelta)
    scraping_date = datetime.today()
    df['posting_date'] = scraping_date - df['timedelta']
    df = df.drop("timedelta", axis=1)
    return df

def create_ngrams(df, column, n):
    return df[column].apply(lambda row: list(ngrams(row, n)))


def process_dataframe(df):
    df = replace_description(df)
    df = add_language(df)
    df = filter_language(df)
    df = lower_case(df)
    df = tokenize(df)
    df = remove_stopwords(df)
    df = lemmatize(df)
    df = add_posting_date(df)
    df['job_description_bigram'] = create_ngrams(df, 'job_description_prep', 2)
    df.rename(columns={"job_description_prep":"job_description_unigram"}, inplace=True)
    return df

