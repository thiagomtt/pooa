from bs4 import BeautifulSoup
import re

class newsHandler():
    def __init__(self, htmlText, siteName):
        self.htmlText = htmlText
        self.siteName = siteName


    def handler(self):
        # Return dictionary with website news
        dictNews = {'Category': [],
                    'Title': [],
                    'Link': []
                    }

        # Standardized function names 
        # Checks if function exists with getattr() 
        methodName = 'news' + self.siteName
        method = getattr(self, methodName, lambda:'Invalid function name')
        return method(dictNews)
        

    def newsGlobo(self, dictNews):
        categories = {'hui-color-sports': 'Esporte',
                    'hui-color-journalism': 'Jornalismo',
                    'hui-color-entertainment': 'Entretenimento',
                    'hui-color-technology': 'Tecnologia'}

        for news in self.htmlText('a', {'class': re.compile('^hui-highlight__link|^topglobocom')}):
            newsLink = news.get('href').rstrip('\n')
            if newsLink:
                newsTitle = news.get('title').rstrip('\n')
                newsTitleStrings = newsTitle.split()
                if len(newsTitleStrings) >= 5:
                    dictNews['Title'].append(newsTitle)
                    dictNews['Link'].append(newsLink)
                    try:
                        for parent in news.parents:
                            classe = parent.get('class')
                            for element in classe:
                                if element in categories.keys():
                                    dictNews['Category'].append(
                                        categories.get(element))
                    except:
                        pass

        return dictNews


    def newsEstadao(self, dictNews):
        for news in self.htmlText.find_all('a'):
            newsContents = news.contents
            newsTitle = news.get('title')
            newsLink = news.get('href')
            if newsLink:
                try:
                    title_strings = newsTitle.split()
                except:
                    pass
                if newsTitle != None and len(title_strings) > 5:
                    try:
                        if newsTitle == newsContents[0].strip() and not newsTitle in dictNews['Title']:
                            dictNews['Category'].append('Notícia')
                            dictNews['Title'].append(newsTitle)
                            dictNews['Link'].append(newsLink)
                    except:
                        pass

        return dictNews


    def newsTechtudo(self, dictNews):
        for news in self.htmlText('a', {'class': re.compile('^feed-post-link|^bstn-hl-link')}):
            newsLink = news.get('href')
            if news.get('class')[0] == 'bstn-hl-link':
                for title in news.find('span', {'class': re.compile('^bstn-hl-title')}):
                    newsTitle = title
            else:
                newsTitle = news.contents[0]

            dictNews['Category'].append('Tecnologia')
            dictNews['Title'].append(newsTitle)
            dictNews['Link'].append(newsLink)
        
        return dictNews


    def newsTerra(self, dictNews):
        for news in self.htmlText('a', {'target': re.compile('^_top|_blank')}):
            if news.get('title') != None:
                newsTitle = news.get('title').strip()
                newsLink = news.get('href').strip()

                if not newsTitle in dictNews['Title'] and len(newsTitle.split()) > 4:
                    dictNews['Category'].append('Notícia')
                    dictNews['Title'].append(newsTitle)
                    dictNews['Link'].append(newsLink)
            else:
                if len(news.contents) == 1:
                    newsLink = news.get('href').strip()
                    try:
                        while news.parent.get('title') == None:
                            if news.parent != None:
                                news = news.parent
                        newsTitle = news.parent.get('title').strip()
                        if not newsTitle in dictNews['Title'] and len(newsTitle.split()) > 4:
                            dictNews['Category'].append('Notícia')
                            dictNews['Title'].append(newsTitle)
                            dictNews['Link'].append(newsLink)
                    except:
                        pass
        
        return dictNews


    def newsPelando(self, dictNews):

        for news in self.htmlText('a', {'class': re.compile('^cept-tt')}):
            newsLink = news.get('href').rstrip('\n')
            if newsLink:
                newsTitle = news.get('title').rstrip('\n')
                dictNews['Category'].append('Promoção')
                dictNews['Title'].append(newsTitle)
                dictNews['Link'].append(newsLink)

        return dictNews
