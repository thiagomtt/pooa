from bs4 import BeautifulSoup
import re

def newsHandler(htmlText, siteName):
    sitesAvailable = {'Globo': newsGlobo(htmlText),
                      'Estadao': newsEstadao(htmlText),
                      'Techtudo': newsTechtudo(htmlText),
                      'Terra': newsTerra(htmlText),
                      'Pelando': newsPelando(htmlText)}

    if siteName in sitesAvailable.keys():
        return sitesAvailable.get(siteName)


def newsGlobo(htmlText):
    dictNews = {'Category': [],
                'Title': [],
                'Link': [],
                }
    categories = {'hui-color-sports': 'Esporte',
                  'hui-color-journalism': 'Jornalismo',
                  'hui-color-entertainment': 'Entretenimento',
                  'hui-color-technology': 'Tecnologia'}

    for news in htmlText('a', {'class': re.compile('^hui-highlight__link|^topglobocom')}):
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


def newsEstadao(htmlText):
    dictNews = {'Title': [],
                'Link': [],
                }

    for news in htmlText.find_all('a'):
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
                        dictNews['Title'].append(newsTitle)
                        dictNews['Link'].append(newsLink)
                except:
                    pass

    return dictNews


def newsTechtudo(htmlText):
    dictNews = {'Category': [],
                'Title': [],
                'Link': [],
                }

    for news in htmlText('a', {'class': re.compile('^feed-post-link|^bstn-hl-link')}):
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


def newsTerra(htmlText):
    dictNews = {'Title': [],
                'Link': [],
                }

    for news in htmlText('a', {'target': re.compile('^_top|_blank')}):
        if news.get('title') != None:
            newsTitle = news.get('title').strip()
            newsLink = news.get('href').strip()

            if not newsTitle in dictNews['Title'] and len(newsTitle.split()) > 4:
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
                        dictNews['Title'].append(newsTitle)
                        dictNews['Link'].append(newsLink)
                except:
                    pass
    
    return dictNews


def newsPelando(htmlText):
    dictNews = {'Category': [],
                'Title': [],
                'Link': []}

    for news in htmlText('a', {'class': re.compile('^cept-tt')}):
        newsLink = news.get('href').rstrip('\n')
        if newsLink:
            newsTitle = news.get('title').rstrip('\n')
            dictNews['Category'].append('Promoção')
            dictNews['Title'].append(newsTitle)
            dictNews['Link'].append(newsLink)

    return dictNews
