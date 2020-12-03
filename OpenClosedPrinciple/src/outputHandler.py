import pandas as pd
import time

class outputHandler():
    def __init__(self, newsDict, siteName):
        self.newsDict = newsDict
        self.siteName = siteName

    def generateCSV(self):
        localTime = time.localtime()

        df = pd.DataFrame(self.newsDict, columns=self.newsDict.keys())
        df.to_csv(f'{self.siteName}-dataframe--{localTime[0]}-{localTime[1]}-{localTime[2]}--{localTime[3]}-{localTime[4]}-{localTime[5]}.csv',
            sep=';', index=False, header=True)
