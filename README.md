# Amazon_Scraper

Given product url, this amazon scraper can scrape important details of a specific product. For this project we scrape different features of computer monitors to help consumers breakdown the many unique features of computer monitors. This project was done in a co

A simple amazon scraper to extract product details and prices from Amazon.com using Selenium Webdriver and Webdriver_manager. 


From a terminal 

1. Clone this project  `https://github.com/erjonb19/Amazon_Monitor_Scraper`
2. Install Requirements 
`from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pyttsx3pip3`

# Scrape Products from Search Results

This scraper can scrap as many pages as possible, scrapes were usually done at around 10-15 pages of products.

1. Add Amazon Product URLS to [search.url](search.url)
1. Run `amazon_scraper.ipynb`
1. Get data from [output.csv](output.csv)


## Example Data Format

### Product Details
```csv
{
Name:,Url:,Rating:,Ratings:,Price:,Display Size:,Refresh Rate:,Resolution:,Response Time:,Manufacturer:,Ports:,Curved:,Speakers:,Height Adjustable:

1,"LG 34WP88C-B 34-inch Curved 21:9 UltraWide QHD (3440x1440) IPS Display with Ergo Stand (Extend/Retract/Swivel/Height/Tilt), USB Type C (90W Power delivery), DCI-P3 95% Color Gamut with HDR 10",https://www.amazon.com/LG-34WP88C-B-34-inch-Curved-UltraWide/dp/B09BP279HR/ref=sr_1_omk_4?crid=2HRQHDDQ8D5R0&keywords=computer+monitor&qid=1648946051&sprefix=computer+monitor%2Caps%2C192&sr=8-4,4.6 out of 5 stars,954,$799.99,34 inches,60 hertz,3440x1440,5 milliseconds,LG,Type-C,True,True,True

2,"HP 23.8"" LED Backlit Monitor, Low Blue Light (V241ib, Black)",https://www.amazon.com/HP-Backlit-Monitor-Light-V241ib/dp/B09JL4W5CQ/ref=sr_1_5?crid=2HRQHDDQ8D5R0&keywords=computer+monitor&qid=1648946051&sprefix=computer+monitor%2Caps%2C192&sr=8-5,4.7 out of 5 stars,500,$164.99,23.8 inches,76 hertz,1920x1080,14 milliseconds,HP,HDMI,False,False,False

}
