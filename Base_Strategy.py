#-*- coding:UTF-8 -*-

import datetime
import json
import numpy as np
import pandas as pd
from Content import Content
from StockRecord import record

'''
Structured Data feed into Base_Strategy, Invoke StockRecord, Organized data(Portfolio) store into Content.py

'''

class Basic_strategy():


    def __init__(self,stock_data):
        newStrategy = Content()
        #   Content is a data frame
        self.Content = newStrategy.df



    def long_short_signal(self):
        """
        Step 1
        Produce signal of long short for each stock records, Key strategy here
        :return:
        """
        raise NotImplementedError

    def position_change(self,records:[record]):
        """
        Step 2
        pass long short signal to here and calculated how much position should be changed for each stock records
        :return: list of Records
        """

    def _cash_calculate(self,cash):
        """
        Cash(t) = Cash(t-1)+sum((Share(t-1)-Share(t))*lastprice(t))
        cash: cash value @ t
        """




    def _equity_calculate(self):

    def _position_clear(self):

    def event_handler(self):



