from text_func import *
from dictionary import *
import pandas as pd

df_0 = scrape_linkedin_jobs(number_of_jobs=50, exact_match=True)
df_1 = process_dataframe(df_0, '27 December 2023')