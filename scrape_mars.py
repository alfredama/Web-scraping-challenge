from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    #setting my url variable 
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(2) 

    # setting my html and reading it with beautiful soup 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    latest_info = {}

    #filtering my results down to the titles  based on the HTML class identified 
    results = soup.body.find_all('div', class_='content_title')
    latest_info["latest_title"] = results[1].text
    results = soup.find_all('div', class_="article_teaser_body")
    latest_info["latest_Paragraph"] = results[0].text

    #setting my url variable 
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #launching my browser using the chromedriver extension 
    browser.visit(url)
    time.sleep(2)
    # setting my html and reading it with beautiful soup 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
   #filtering my results down to the image URL  based on the HTML class identified 
    results = soup.body.find_all('a', class_='fancybox')
    latest_info["latest_image_url"] = "https://www.jpl.nasa.gov" + str(results[1].get('data-fancybox-href'))

    url = 'https://space-facts.com/mars/'
    dframe = pd.read_html(url,header=0)
    latest_info["html_file"] = dframe[0].to_html()

    url = "https://twitter.com/marswxreport?lang=ens"
    #launching my browser using the chromedriver extension 
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.body.find_all('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    latest_info["Mars_tweet"] = results[0].text

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    #launching my browser using the chromedriver extension 
    browser.visit(url)
    time.sleep(2) 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #filtering my result from the html page
    results = soup.body.find_all('div', class_='description')
    #Creating a list for my extracted results
    counter = 0
    #filtering my result from the html page
    for result in results:
        page_link = result.find('a')['href']
        url = "https://astrogeology.usgs.gov" + str(page_link)
        browser.visit(url)
        time.sleep(2)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        #filtering my result from the html page
        res_url = soup.body.find_all('h2', class_='title')
        title = res_url[0].text
        
        #filtering my result from the html page
        res_url = soup.body.find_all('img', class_='wide-image')
        image = res_url[0].get('src')
        image_url = "https://astrogeology.usgs.gov" + str(image)
        
        #storing my results in a list 
        latest_info[f'Title{counter}'] = title
        latest_info[f'Image_url{counter}'] = image_url
        print(latest_info)  
        counter += 1
        
    # Return results
    browser.quit()
    print(latest_info)    
    return latest_info