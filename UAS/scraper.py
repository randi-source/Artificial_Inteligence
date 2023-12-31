from text_func import *
from dictionary import *
import pandas as pd

max_attempts = 3

for attempt in range(max_attempts):
    try:
        print("Scraping in progress...")
        try:
            existing_df = pd.read_csv('linkedin_jobs.csv')
            existing_df['posting_date'] = pd.to_datetime(existing_df['posting_date'])
        except FileNotFoundError:
            existing_df = pd.DataFrame()


        #print("==========EXISTING DF=============")
        #print(existing_df.head())

        new_df = scrape_linkedin_jobs(number_of_jobs=300, exact_match=True)
        new_df = process_dataframe(new_df)
        print("==========NEW DF=============")
        print(new_df.head())
        print(new_df.count())

        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        #combined_df = combined_df.drop_duplicates(subset=['company', 'job_title'])

        print("=========COMBINED DF===========")
        print(combined_df.head())
        print(combined_df.count())

        combined_df.to_csv('linkedin_jobs.csv', encoding='utf-8', index=False)
        print("Success")
        break
    except Exception as e:
        print(f"Attempt {attempt+1} failed with error: {e}")
        if attempt + 1 == max_attempts:
            raise

