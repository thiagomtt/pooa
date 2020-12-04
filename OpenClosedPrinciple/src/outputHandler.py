import pandas as pd
import re
import time

class outputHandler():
    def __init__(self, newsDict, siteName):
        self.newsDict = newsDict
        self.siteName = siteName

    
    def handler(self, outputFormat):
        # Check the output type 
        if re.compile('^csv').match(outputFormat.lower()):
            methodName = 'generateCSV'
        elif re.compile('^print').match(outputFormat.lower()):
            methodName = 'printOnScreen'

        method = getattr(self, methodName, lambda: 'Invalid Name')
        return method()


    def generateCSV(self):
        # Generate a .csv file with a DataFrame from Pandas
        localTime = time.localtime()

        dataFrame = pd.DataFrame(self.newsDict, columns=self.newsDict.keys())
        dataFrame.to_csv(f'{self.siteName}-dataframe--{localTime[2]}-{localTime[1]}-{localTime[0]}--{localTime[3]}-{localTime[4]}-{localTime[5]}.csv',
                sep=';', index=False, header=True)


    def printOnScreen(self):
        # Print  website news on the screen with a .csv file style
        localTime = time.localtime()

        titlesList = list(self.newsDict.keys())
        newsList = list(self.newsDict.values())
        
        print(f'-----{self.siteName} DataFrame-----')
        print(f'Obtained in: {localTime[2]}/{localTime[1]}/{localTime[0]}--{localTime[3]}h{localTime[4]}m{localTime[5]}s\n')
        print('Format:')
        print(f'{titlesList[0]} - {titlesList[1]} - {titlesList[2]}')
        i = 0
        while i<len(newsList[0]):
            print(f'{newsList[0][i]} - {newsList[1][i]} - {newsList[2][i]}')
            i+=1

