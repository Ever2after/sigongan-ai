import gspread
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials

class GSpread:
    def __init__(self, url = 'https://docs.google.com/spreadsheets/d/15Ngz28B0hMa1NsTr7JG5GqV0-Nrhd67BDKQCPDZjzjM/edit#gid=0', keyPath = './gdkey.json'):
        self.keyPath = keyPath
        self.url = url

    def loadSheet(self):
        gc = gspread.service_account(filename=self.keyPath)
        sh = gc.open_by_url(self.url)
        return sh
    
    def updateByDf(self, df, startRC):
        sh = self.loadSheet().sheet1
        start = f'R{startRC[0]}C{startRC[1]}'
        end = f'R{startRC[0]+df.shape[0]-1}C{startRC[1]+df.shape[1]}'
        sh.update(f'{start}:{end}', df.to_numpy().tolist())
        

