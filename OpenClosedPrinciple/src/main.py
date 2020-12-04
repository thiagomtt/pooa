from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import re
from outputHandler import outputHandler
from newsHandler import newsHandler


class Site():
    def __init__(self, url):
        if re.compile('^https').match(url):    
            self.url = url
        else:
            self.url = f'https://{url}'
        
        # Get website name from URL 
        if re.compile('^https://www.').match(self.url):
            name = re.search('www.(.+?).com', self.url).group(1)
        else:
            name = re.search('//(.+?).com', self.url).group(1)
        self.name = name.capitalize()
    
    def getUrl(self):
        return self.url

    def getName(self):
        return self.name

    def getNews(self):
        # Return a dictionary with news from HTML
        return newsHandler(self.getHTML(), self.name).handler()

    def getHTML(self):
        # Web scrapper for infinite scrolling page
        driver = webdriver.Chrome(
            executable_path='/home/thiago/pooa/OpenClosedPrinciple/bin/chromedriver')
        driver.get(self.url)
        time.sleep(1)
        scroll_pause_time = 1
        # Get the screen height of the web
        screen_height = driver.execute_script("return window.screen.height;")
        i = 1

        while True:
            # Scroll one screen height each time
            driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            # Update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break
        
        # Beautifulsoup treatment
        html = driver.page_source
        htmlText = BeautifulSoup(html, 'html.parser')
        
        # Close browser
        driver.quit()

        return htmlText


def main():
    # Globo
    globo = Site('www.globo.com')
    newsGlobo = globo.getNews()
    outputHandler(newsGlobo, globo.getName()).handler('CSV')

    # Estadao
    estadao = Site('www.estadao.com.br')
    newsEstadao = estadao.getNews()
    outputHandler(newsEstadao, estadao.getName()).handler('csv')

    # Techtudo
    techtudo = Site('www.techtudo.com.br')
    newsTechTudo = techtudo.getNews()
    outputHandler(newsTechTudo, techtudo.getName()).handler('csv')

    # Terra
    terra = Site('www.terra.com.br')
    newsTerra = terra.getNews()
    outputHandler(newsTerra, terra.getName()).handler('csv')

    # Pelando
    pelando = Site('www.pelando.com.br')
    newsPelando = pelando.getNews()
    outputHandler(newsPelando, 'Pelando').handler('print')

if __name__ == "__main__":
    main()
