# Importing dependencies
from typing import final
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from flask import Flask, render_template
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Setup  Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Visit Mars News url  using splinter module
    red_planet_url = 'https://redplanetscience.com/'
    browser.visit(red_planet_url)

    #create HTMl Object
    html = browser.html

    # Parse HTML with beautiful soup
    soup = bs(html, 'html.parser')

    red_planet_data = soup.find('div', id = 'news', class_ = 'container')

    # Extract title 
    title = soup.find('div',class_='content_title').text

    #Extract paragraph
    paragraph = red_planet_data.find('div', class_= 'article_teaser_body').text


    # visit Mars image url
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    #create HTMl Object
    image_html = browser.html

    #parse HTML with beautiful soup
    image_soup = bs(image_html, 'html.parser')

    # Print image
    featured_img_url = image_url + image_soup.find('div', class_='header').find('img', class_='headerimage').get('src')

    #visit Mars facts url
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)
    #create HTMl Object
    facts_html = browser.html
    facts_table = pd.read_html(facts_url)

    #parse HTML with beautiful soup
    facts_soup = bs(facts_html, 'html.parser')

    #Create Dataframe to store facts_table
    facts_table_df = facts_table[0]

    # Drop the Earth column
    facts_table_df = facts_table_df.drop(columns = [2])

    # Rename columns
    columns = ['Mars-Earth Comparison', 'Mars-Facts']
    facts_table_df = facts_table_df.rename(columns={0:'Mars-Earth Comparison', 1:'Mars-Facts'})

    # Convert dataframe to html
    facts_html = facts_table_df.to_html()

    # Hemispheres images
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    #create HTMl Object
    hemishpere_html = browser.html

    #parse HTML with beautiful soup
    hemisphere_soup = bs(hemishpere_html, 'html.parser')

    url = hemisphere_soup.find_all('div', class_='item')
    hemisphere_title = []
    hemispheres_img_url = []

    for x in url:
        time.sleep(2)
        hemisphere_title = x.find('h3').text
        #print(hemisphere_title)
        url1 = x.find('a', class_= 'itemLink product-item')['href']
        #print(url1)
        url2 = hemispheres_url + url1
        #print(url2)
        browser.visit(url2)
        html = browser.html
        soup = bs(html,'html.parser')
        # navigate to individual images
        src = soup.find('img', class_='wide-image').get('src')
        #print(src)
        img_url = hemispheres_url + src 
        #print(img_url)
        dictionary={"hemisphere_title": hemisphere_title,"img_url":img_url}
        #dictionary_copy = dictionary.copy()
        #print(dictionary_copy)
        hemispheres_img_url.append(dictionary)     
    

    final_data = {
        'title' : title,
        'paragraph' : paragraph,
        'feature_img_url': featured_img_url,
        'table': facts_html, 
        #'hemisphere_title':  hemisphere_title, 
        'images': hemispheres_img_url
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return final_data



