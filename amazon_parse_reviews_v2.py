#!/usr/bin/env python3

import argparse
import pandas as pd
import argparse
import subprocess
import json
import os
import openai
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import nltk
import seaborn as sns
import re
from bs4 import BeautifulSoup
from re import search
import time
import os
from sklearn.feature_extraction.text import CountVectorizer
from yellowbrick.text import FreqDistVisualizer
import re
import seaborn as sb

## Sample Usage: python amazon_parse_reviews_v2.py -input background_data.csv -prerunData output_monitor_review_data.csv -runOpenAi False

## Set-up input arguments
parser = argparse.ArgumentParser(description='Parser is used to extract content from urls listed in input file')
parser.add_argument('-input','--inputfile', help='Provide full input file path', required=True)
parser.add_argument('-output','--outputfile', help='Provide output file name (csv)', required=False)
parser.add_argument('-runOpenAi', '--runOpenAi', help='Input either `True` or `False`', required=False)
parser.add_argument('-apikey','--apikey', help='Provide OpenAI API key', required=False)
parser.add_argument('-prerunData', '--prerunData', help='Input either `True` for loading pre-run openAI data or `False` running openAI to extract keywords', required=False)

## Arguments
args = parser.parse_args()
input_name=args.inputfile
output_name=args.outputfile
key_name=args.apikey
run_command=args.runOpenAi
pre_run_data=args.prerunData

## openai api key
openai_api_key=key_name
openai.api_key = openai_api_key

## set-up driver:
def driver_load():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver

## Extract Urls from background data
def load_urls(input_path):
    output_data=pd.read_csv(input_path)
    url_data=[]
    for index, row in output_data.iterrows():
        url_data.append([index, row['Url']])
    return url_data

## Load background data frame
def load_df(input_path):
    output_data=pd.read_csv(input_path)
    return(output_data)

## Commands for running openAI models
def generate_keywords(input_string):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt="Extract keywords from this text:\n\n" + input_string,
        temperature=0.3,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.8,
        presence_penalty=0
        )
    return response

## Headers for webdriver
def parse_url_reviews(input_url_index, input_driver):
    headers={'authority': 'www.amazon.com',
     'pragma': 'no-cache',
     'cache-control': 'no-cache',
     'dnt': '1',
     'upgrade-insecure-requests': '1',
     'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
     'sec-fetch-site': 'none',
     'sec-fetch-mode': 'navigate',
     'sec-fetch-dest': 'document',
     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}
    print('Parsing:', input_url_index[1])
    input_driver.get(input_url_index[1])
    ## Scrape target url
    elems = driver.find_elements(By.XPATH, "//a[@href]")
    target_urls=[]
    for elem in elems:
        if re.search("product-reviews", elem.get_attribute("href")) and re.search("Type=all_reviews", elem.get_attribute("href")) and not re.search("filterByStar", elem.get_attribute("href")):
            target_urls.append(elem.get_attribute("href"))
        else:
            continue
    target_urls_revised=list(set(target_urls))[0]
    driver.get(target_urls_revised)
    content=input_driver.page_source
    soup=BeautifulSoup(content,"lxml")
    time.sleep(15)
    textFile=[]
    textFilterList=[]
    reviewScoreList=[]
    subStringDrop1="people found this helpful"
    for i in soup.find_all('span', attrs={'data-hook':True}):
        if i.find('span') is not None:
            textFile.append(i.find('span').text)
    for i in textFile:
        if search(subStringDrop1, str(i)):
           continue
        elif len(i) == 0:
            continue
        else:
            textFilterList.append(i)
    for i in soup.find_all('div', id='cm_cr-review_list'):
        for j in i.find_all('a', attrs={'class': 'a-link-normal'}):
            if j.find('span', attrs={'class': 'a-icon-alt'}) is not None:
                reviewScoreList.append(float(j.find('span', attrs={'class': 'a-icon-alt'}).text[0:3]))
    output_df_reviews=pd.DataFrame(zip(textFilterList, reviewScoreList))
    output_df_reviews.columns=['review_content','score']
    output_df_reviews['keywords']=''
    output_keyword_list=[]
    output_text_list=list(output_df_reviews['review_content'])
    return(output_text_list,output_df_reviews, input_url_index[0])

## Run openAI model on parsed text-data
def run_openai(input_text_list, file_tag_name, output_review_data):
    output_keyword_list=[]
    for i in input_text_list:
        output_json=generate_keywords(i)
        pdObj = pd.json_normalize(output_json)
        output_keyword_list.append(pd.json_normalize(pdObj['choices'][0][0])['text'][0].replace('\n',''))
    output_review_data['keywords']=output_keyword_list
    if not os.path.exists('output_review_data'):
        os.makedirs('output_review_data')
    pd.DataFrame(output_review_data).to_csv('output_review_data/product' + str(file_tag_name))

## Run parsing content function
def run_full_df(input_url_file_path, driver):
    input_df=load_df(input_url_file_path)
    input_df['keywords']=''
    urls_list=load_urls(input_url_file_path)
    keywords_parsed=[]
    if run_command==True:
        for i in urls_list:
            out=parse_url_reviews(i, driver)
            run_openai(out[0], out[1], out[2])
    else:
        output_df=pd.read_csv(pre_run_data)
        return(output_df)

## Combine review data files
def process_output_files(input_path):
    file_list=[]
    for file in os.listdir(input_path):
        file_list.append(os.path.join(input_path, file))
    li = []
    for filename in file_list:
        df = pd.read_csv(filename, index_col=None, header=0)
        df['filename']=os.path.basename(filename)
        li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)
    output_keyterms=frame[['filename','keywords','score']]
    return output_keyterms

## Apply reformatting to extracted keywords
def format_output(input_string_keywords):
    out=str(input_string_keywords).lower().replace('-',',').split(',')
    return out

## Flatten list
def flatten(input_list):
    return [item for sublist in input_list for item in sublist]

## Optional remove stop terms
def remove_stop(output_sample_list):
    nltk.download("stopwords")
    stop_word_list=nltk.corpus.stopwords.words('english')
    keyword_list=[]
    for i in output_sample_list:
        if i not in stop_word_list:
            keyword_list.append(i)
        else:
            continue
    removed = [w for w in keyword_list if not w.isalnum()]
    return removed

## Combine and filter key term list
def combine_output(output_data):
    output_list=output_data['keywords']
    out=[]
    for i in output_list:
        out.append(format_output(i))
    combined_list=flatten(out)
    revised_comb=list(map(lambda n: n.strip(), combined_list))
    error_string='person found this helpful'
    rev_list=[]
    for i in revised_comb:
        if i == '' or re.search(error_string, str(i)) or re.search('most recent', str(i)):
            continue
        else:
            rev_list.append(i)
    return(rev_list)

## Combines background data if returning keyterm data from scraping:
def combine_background_keyterms(input_file_url_path, current_keyterm_data):
    background_data=pd.read_csv(input_file_url_path)
    index_key_list=[]
    for index,j in background_data.iterrows():
        index_key_list.append('product' +str(index))
    background_data['filename']=index_key_list
    combined_data=pd.merge(current_keyterm_data, background_data, how='inner', on='filename')
    return(combined_data)

## Generate list of positive and negative review keyterms
def subset_sentiment(output_keyterms_df):
    positive_reviews=output_keyterms_df[output_keyterms_df['score']>2]
    positive_keyterms=combine_output(positive_reviews)
    pd.DataFrame(positive_keyterms).to_csv('positive_review_terms.csv')
    negative_reviews=output_keyterms_df[output_keyterms_df['score']<3]
    negative_keyterms=combine_output(negative_reviews)
    pd.DataFrame(negative_keyterms).to_csv('negative_review_terms.csv')

if __name__ == '__main__':
    driver=driver_load()
    output_df_reviews=run_full_df(input_name, driver)
    subset_sentiment(output_df_reviews)
