#-*- coding:UTF-8 -*-

import datetime
import json
import numpy as np
import pandas as pd


__author__ = "Leo.Tao   Tianli.Zhang"


'''

    ### This records included each stocks'
    ||
    ||
    ||
    ||
    \/
    Records.Symbol
    Records.Position ===========> percentage of total asset  (0 to 1)
    Records.Average_cost
    Records.Last
    Records.PNL


'''
# @TODO


class Records():
    '''
    Function return  a dictionary with information of one stock
    symbol: underlying stock
    Position: percentage
    NumOfShare: purchase how many share
    AverageCost:
    LastPrice:
    '''

    def __init__(self,symbol,position,NumOfShare,average_cost,lastprice):
        self.Symbol = symbol
        self.Position = position
        self.NumOfShare = NumOfShare
        self.AverageCost = average_cost
        self.LastPrice = lastprice

    def __str__(self):

        return self.Symbol
        #return ('\n'+'Symbol:'+self.Symbol+'\n'+'Position: '+self.Position +'\n'
        #        + 'NumOfShare: '+self.NumOfShare + '\n' + 'AverageCost: '+self.AverageCost + '\n'+
        #        'LastPrice: '+ self.LastPrice + '\n'
        #        )




if __name__=="__main__":
    record = Records(symbol='APPL',position='0.5',NumOfShare='100',average_cost='120',lastprice='121')
    print(record)
    