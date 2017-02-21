#-*- coding:UTF-8 -*-

import datetime
import json
import numpy as np
import pandas as pd
from StockRecord import Records


__author__ = "Leo.Tao   Tianli.Zhang"




'''
                Included all the records,equity,cash and PNL

    formatting:

    {
        ts:{
                symbol:StockRecord
                symbol:StockRecord
                .
                .
                .
                CASH:
                EQUITY:
            }
        .
        .
        .
        .

    }
===========
Methods:
Update

'''

# @TODO

class Content():

    """
    DataBase to record all the results of each trading
    Creating a DataFrame from dictionary
    This class only handle the records from STockRecoks and calculated Equity and Cash
    """

    def __init__(self):
        self.length = 0
        self.allStocks = []
        self.df = pd.DataFrame()


    def add(self, timestamp:int, listOfRecords:[Records], cash:float, equity:float):
        """
        !!!!!!!!!!!!There is one target under each timestamp!!!!!!!!!!!!!

        """
        dic = {}
        for i in listOfRecords:
            dic[i.Symbol]=i
            if i.Symbol not in self.allStocks:
                self.allStocks.append(i.Symbol)

        new_add = pd.DataFrame({'TS':[timestamp],'CASH':[cash],'EQUITY':[equity],'portfolio':[dic]},index=[timestamp])
        if self.length == 0:
            self.df = new_add

        elif timestamp not in self.df['TS']:
            self.df = pd.concat([self.df,new_add],axis=0)

        else:
            raise 'Duplicated timestamp'

        self.length+=1

    def pop(self):
        """
        Delet first item in the DataFrame
        :return:
        """
        self.df = self.df[1:]

    def get_ContentDataFrame(self):
        """
        return updated dataframe of content
        :return:
        """
        return self.df









if __name__=="__main__":
    event = Content()
    record1 = Records('APPL','0.5','99','99','100')
    record2 = Records('APL','0.5','99','99','100')
    event.add('1',[record1,record2],'10000','10000')
    event.add('2', [record1, record2], '10000', '10000')
    #event.add('2',[record2],'10000','10000')
    #event.add('2', 'APL', '0.5', '99', '99', '100', '10000', '10000')
    print(event.df)