#-*- coding:UTF-8 -*-

import datetime
import json
import numpy as np
import pandas as pd
from Content import Content
from StockRecord import Records
import math

'''
Structured Data feed into Base_Strategy, Invoke StockRecord, Organized data(Portfolio) store into Content.py

'''

class Basic_strategy():


    def __init__(self,stock_data):
        newStrategy = Content()
        #   Content is a data frame
        self.Content = newStrategy.df

    def data_handler(self):
        """
        Transfer row data into Stock Record class
        :return: list of Stock_record
        """
        # @TODO


    def long_short_signal(self,records:[Records]):
        """
        Step 1
        Produce signal of long short for each stock records, Key strategy here
        :return: dictionary of signal for each stock profile inside
        {record.Symbol:signal, record.Symbol:signal}
        """
        raise NotImplementedError


    def position_handler(self,quantity:{},listOfRecords:[Records],Style=0,initialCapital=100000):
        """
        Step2
        Position change style:
        :0: Change by quantity
        :1: Change by percentage of initial cash
        :2: Change by percentage of NumOfShare holding====> usually used when you are in position
        :3: Smart allocation=============> maintain fixed ratio between each stock total value # @TODO

        :return: you can implement and algo by your thought
        """
        if Style == 0: return quantity
        elif Style ==1:
            for record in listOfRecords:
                # share to buy = floor(percentage * inital capital / current price)
                quantity[record.Symbol] = math.floor(quantity[record.Symbol]*initialCapital/record.LastPrice)

        elif Style == 2:
            for record in listOfRecords:
                # share to buy = floor(percentage * NumOfShare)
                quantity[record.Symbol] = math.floor(quantity[record.Symbol] *  record.NumOfShare)





    def position_change(self,quantity:{},listOfRecords:[Records],signals:{}):
        """
        Step 2
        pass long short signal to here and calculated how much position should be changed for each stock records


        :return: list of Records
        """
        updated_listOfRecord = []
        for record in listOfRecords:
            sig = signals[record.Symbol]
            qut = quantity[record.Symbol]
            record.NumOfShare += sig*qut
            updated_listOfRecord.append(record)
        return updated_listOfRecord



    def _cash_calculate(self,updated_listOfRecord):
        """
        Cash(t) = Cash(t-1)+sum((Share(t-1)-Share(t))*lastprice(t))
        cash: cash value @ t
        """
        last_records = self.Content[-1:]
        last_Cash = last_records['CASH']
        last_portfolio = last_records['portfolio']  # This is a dictionary
        total_value = []
        for element in updated_listOfRecord:
            if element.Symbol not in last_portfolio:
                total_value.append(element.NumOfShare*element.LastPrice)
            else:
                total_value.append((last_portfolio[element.Symbol].NumOfShare - element.NumOfShare) * element.LastPrice)

        return sum([total_value])

    def _equity_calculate(self):

    def _position_clear(self):

    def event_handler(self):



