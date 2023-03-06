#Import library
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import csv

# Function to extract Product title
def get_Product_title(soup):
    try:
        #Outer tag object
        title = soup.find('span', attrs = {'id':'productTitle'})

        #Inner tag object
        title_text = title.text

        #Clean title
        title_string = title_text.strip()
    except:
        title_string = ''
    return title_string
# Function to extract Product price
def get_price(soup):
    try:
        price = soup.find('span', attrs= {'class':'a-offscreen'}).text.strip()
    except:
        price = ''
    return price
# Function to extract Product rate
def get_rate(soup):
    try:
        rate = soup.find('span', attrs={'class':'a-icon-alt'}).text.strip()
    except:
        rate = ''
    return rate
#Function to extract Number of User review
def get_review(soup):
    try:
        review_count = soup.find('span', attrs = {'id':'acrCustomerReviewText'}).text.strip()
    except:
        review_count = ''
    return review_count

if __name__ == '__main__':
    #headers for request
    head = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    #the webpage URL
    URL = "https://www.amazon.com/s?k=play+stations+4&crid=1E266Y2KT4CK&sprefix=play+stations.+4%2Caps%2C338&ref=nb_sb_noss_1"

    #http request
    webpage = requests.get(URL, headers=head)

    #soup object contain all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    #fetch link as list of tag object
    links = soup.find_all('a', attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    #store links
    links_list = []

    #loop for extract links from tag object
    for link in links:
        links_list.append(link.get('href'))

    dict_list = {'title' :[], 'price' : [], 'rate' : [], 'reviews': []}

    #loop product detail from each link
    for link in links_list:
        new_webpage = requests.get('https://amazon.com' + link, headers=head)
        new_soup = BeautifulSoup(new_webpage.content, 'html.parser')
    
        #Function call to display all info product
        dict_list['title'].append(get_Product_title(new_soup))
        dict_list['price'].append(get_price(new_soup))
        dict_list['rate'].append(get_rate(new_soup))
        dict_list['reviews'].append(get_review(new_soup))

amazon_df = pd.DataFrame.from_dict(dict_list)
amazon_df['title'].replace('', np.nan, inplace= True)
amazon_df = amazon_df.dropna(subset=['title'])
amazon_df.to_csv('amazon_data.csv', header=True, index= False)
print('done')