from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests
import re

# STEP 1: Initialize Browser Function
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# STEP 2: Scrape Data
# First Scrape: Headlines
def scrape_mars_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the headline
    title = soup.find('div', class_='content_title')
    title_text = title.text

    # Get the subhead
    paragraph = soup.find('div', class_='article_teaser_body')
    p_text = paragraph.text

    # Store scraped data in a dictionary
    headlines = {
        'title':title_text,
        'headline': p_text
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return headlines

# Second Scrape: Mars_Image
def scrape_mars_img():
    browser = init_browser()
    # Visit visitcostarica.herokuapp.com
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the current img
    url_text = soup.select('article.carousel_item')[0]['style']
    partial_url = re.search("(?<=').+(?=')",url_text).group()
    full_url = "https://www.jpl.nasa.gov" + partial_url

    # Store scraped data in a dictionary
    img_dict = {
        "featured_image_url": full_url
        }

    #Close the browser after scraping
    browser.quit()

    return img_dict

# Third Scrape: Mars Weather
def scrape_mars_weather():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest tweet
    tweet = soup.find('div', class_='js-tweet-text-container')
    mars_weather = tweet.text

    # Store scraped data in a dictionary
    latest_tweet = {
        "mars_weather": mars_weather
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return latest_tweet

# Fourth Scrape: HTML Table
import requests
url = "https://space-facts.com/mars/"
response = requests.get(url)
response.text[:100] # Access the HTML with the text property

class HTMLTableParser:

    def parse_url(self, url):
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        return [(table['id'],self.parse_html_table(table))\
                for table in soup.find_all('table')]  

    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return df
        
# Use HTML TableParser to parse results into table
hp = HTMLTableParser()
table = hp.parse_url(url)[0][1] # Grabbing the table from the tuple
html_table = table.to_html(classes='table',index=False,escape=False)
html_table.replace('\n', '')

# Fifth Scrape: Mars Hemispheres Titles & Full Images
def scrape_mars_hemisphere():
    browser = init_browser()
    #go to url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(3)
    page_source = browser.html
    soup = bs(page_source,"lxml")
    
    #get the titles
    hemisphere_titles = [x.text for x in soup.select("h3")]
    
    #get the image urls
    all_links = ["https://astrogeology.usgs.gov" + x["href"] \
        for x in soup.select(".item > .product-item")]
    image_links = []
    
    for link in all_links:
        browser.visit(link)
        page_source = browser.html
        soup = bs(page_source,"lxml")
        image_link = "https://astrogeology.usgs.gov" + str(soup.select(".wide-image")[0]["src"])
        image_links.append(image_link)
    
    #zip titles and links into dictionary within a list
    hemispheres_list = []
    for x,y in zip(hemisphere_titles,image_links):
        hemispheres_dict = {"title":x,"image_url":y}
        hemispheres_list.append(hemispheres_dict)

    # Close the browser after scraping
    browser.quit()

    # Return results
    return hemispheres_list

# STEP 6: Put all scraped data into dictionary
def scrape_info():
     scraped_data = {
         "headlines_dict":scrape_mars_info(),
         "img_dict":scrape_mars_img(),
         "weather_dict":scrape_mars_weather(),
         "table_list":html_table,
         "hemispheres_list":scrape_mars_hemisphere()
     }
     return scraped_data