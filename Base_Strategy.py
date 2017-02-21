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

    def __init__(self):
        self._newStrategy = Content()   # This a class
            # This is float
        #   Content is a data frame

    def display_all_content(self):
        return self._newStrategy.df

    def data_handler(self,**kwargs):
        """

        Fetch data from DataBase


        Transfer row data into Stock Record class
        :return: list of Stock_record
        class of Records

        Symbol
        NumOfShare(t-1)
        Position(t-1)
        AveragePrice(t)
        LastPrice(t)
        """
        raise NotImplementedError

    def long_short_signal(self,listOfRecords:[Records]):
        """
        Step 1
        Produce signal of long short for each stock records, Key strategy here
        :return: dictionary of signal for each stock profile inside
        {record.Symbol:signal, record.Symbol:signal}
        """
        print(" Impelement ur strategy Here")
        raise NotImplementedError

    def position_handler(self,quantity:{},listOfRecords:[Records],Style=0,**mutiple):
        """
        Step2
        Position change style:
        :0: Change by quantity
        :1: Change by percentage of initial cash
        :2: Change by percentage of NumOfShare holding====> usually used when you are in position
        :3: fixed ratio quantity is the ratio {'AAPL':2,"APL":3} ratio  2:3

        :return: you can implement and algo by your thought
        >>> record1 = Records('AAPL',0.1,10,139.22,100)
        >>> record2 = Records('APL',0.1,10,10.3,10)
        >>> listrecord = [record1,record2]
        >>> quantity = {'AAPL':0.2,"APL":0.3}
        >>> testt = Basic_strategy(100000)
        >>> zz = testt.position_handler(quantity,listrecord,Style=1)
        >>> print(zz['APL'] == 2912)    # {'APL': 2912, 'AAPL': 143}
        True
        """

        if Style == 0: return quantity
        elif Style ==1:
            for record in listOfRecords:
                # share to buy = floor(percentage * inital capital / current price)
                quantity[record.Symbol] = math.floor(quantity[record.Symbol]*self._initialCash/record.AverageCost)
            return quantity

        elif Style == 2:
            for record in listOfRecords:
                # share to buy = floor(percentage * NumOfShare)
                quantity[record.Symbol] = math.floor(quantity[record.Symbol] * record.NumOfShare)
            return quantity

        elif Style ==3:
            for record in listOfRecords:
                quantity[record.Symbol] = quantity[record.Symbol] * mutiple
            return quantity
        elif Style ==4 :
            raise NotImplementedError

    def _record_update(self,quantity:{},listOfRecords:[Records],signals:{}):
        """
        Step 2
        pass long short signal to here and calculated how much position should be changed for each stock records


        :return: list of Records
        >>> record1 = Records('AAPL',0.1,10,200,100)
        >>> record2 = Records('APL',0.1,10,20,10)
        >>> listrecord = [record1,record2]
        >>> quantity = {'AAPL':100,"APL":0}
        >>> signal={'AAPL':-1,"APL":1}
        >>> testt = Basic_strategy(100000)
        >>> zz = testt._record_update(quantity,listrecord,signal)
        >>> a = zz[1].display_all()
        >>> print(a)
        <BLANKLINE>
        Symbol:APL
        Position: 0.1
        NumOfShare: 10
        AverageCost: 20
        LastPrice: 10
        <BLANKLINE>
        """
        updated_listOfRecord = []
        for record in listOfRecords:
            sig = signals[record.Symbol]
            qut = quantity[record.Symbol]
            record.NumOfShare += sig*qut
            updated_listOfRecord.append(record)
        return updated_listOfRecord

    def _cash_calculate(self,updated_listOfRecord:[Records]):
        """
        Step 3
        Cash(t) = Cash(t-1)+sum((Share(t-1)-Share(t))*lastprice(t))
        cash: cash value @ t

        >>> record1 = Records('AAPL',0.1,10,200,100)
        >>> record2 = Records('APL',0.1,10,20,10)
        >>> listrecord = [record1,record2]
        >>> testt = Basic_strategy(100000)
        >>> testt._cash_calculate(listrecord)
        97800
        """

        if self._newStrategy.length == 0:
            # Check if this is the first data come in
            raise notInitiateError
        else:
            last_records = self.get_last_row()
            last_Cash = last_records['CASH'].item()
            last_portfolio = last_records['portfolio'].item()  # This is a dictionary
            total_change_value = []
        for element in updated_listOfRecord:
            total_change_value.append((last_portfolio[element.Symbol].NumOfShare - element.NumOfShare) * element.AverageCost)

        return last_Cash + sum(total_change_value)

    def _equity_calculate(self,updated_listOfRecord:[Records],current_cash):
        """
        Equity = Cash(t) + sum(NumOfStock(t)*Price(t))
        :param updated_listOfRecord:
        :return:
        >>> record1 = Records('AAPL',0.1,10,200,100)
        >>> record2 = Records('APL',0.1,10,20,10)
        >>> listrecord = [record1,record2]
        >>> testt = Basic_strategy(100000)
        >>> testt._equity_calculate(listrecord,100000)
        102200
        """
        total_value = []
        for element in updated_listOfRecord:
            total_value.append(element.NumOfShare*element.LastPrice)
        return sum(total_value) + current_cash

    def stop_loss_win(self,listOfRecord:[Records],stop_ratio):
        """
        Here implement your stop loss and win strategy, this will be claculated after your stock change
        If Triggered, it will override the Long Short signal

        it will not trigger when there is no position
        once it triggered it return a dictionary with now much share are going to be clear
        ratio = equity(t)/equity(t-1) = [cash(t-1) + sum(NumOfShare(t-1)*LastPrice(t))]/equity(t-1)
        :return: {'Symbol':NumOfShare...}

        default  equity down than .95
        """
        last_row = self.get_last_row()
        last_equity = last_row['EQUITY'].item()
        last_cash = last_row['CASH'].item()
        underlying_value = []
        NumShares = {}
        for element in listOfRecord:
            underlying_value.append(element.NumOfShare * element.LastPrice)
            NumShares[element.Symbol] = -element.NumOfShare
        ratio = (last_cash+ sum(underlying_value))/last_equity  # Calculate equity ratio compare to last time
        print(ratio)
        if ratio <= stop_ratio:
            return NumShares
        else:
            return None

    def check_if_in_position(self):
        """
        Check if there is any position,
        No position :return: False
        Holding position :return: True
        >>> testt = Basic_strategy(100000)
        >>> record1 = Records('AAPL',0,2,200,100)
        >>> testt._newStrategy.add('111',[record1],1000,10000)
        >>> testt.check_if_in_position()
        True
        """
        last_records = self.get_last_portfolio()
        for symbol in last_records:
            if last_records[symbol].NumOfShare == 0:
                continue
            else:
                return True
        return False

    def event_handler(self,quantity,cal_style,timeStamp,row_data): # row_data: Generate a List of Records
        checkLost = self.stop_loss_win(row_data,stop_ratio=0.95)    # Generate dictionary Tell me how many shares you need to sell
        # step 1 check lost win
        if checkLost != None:
            print('stop lost,ratio:', checkLost)
            signal = {}
            for element in row_data:
                signal[element.Symbol] = 1
            updated_record = self._record_update(checkLost,row_data,signal)
        else:
            signal = self.long_short_signal(row_data)
            position_change = self.position_handler(quantity,row_data,Style=cal_style)
            updated_record = self._record_update(position_change,row_data,signal)

        updated_cash = self._cash_calculate(updated_record)
        updated_equity = self._equity_calculate(updated_record,updated_cash)
        self._newStrategy.add(timestamp=timeStamp,listOfRecords=updated_record,cash=updated_cash,equity=updated_equity)

    def get_last_row(self):
        """
        If this is first row return None
         >>> testt = Basic_strategy()
         >>> testt.get_last_row()

        """

        last_row = self._newStrategy.get_ContentDataFrame()[-1:]
        if len(last_row) == 0:
            raise notInitiateError
        else:
            return last_row

    def get_last_portfolio(self):
        """
        >>> testt = Basic_strategy(100000)
        >>> testt.get_last_row()
        """
        return self.get_last_row()['portfolio'].item()

    def initiate(self,listOfRecord:[Records],initial_cash,timestamp):
        self._initialCash = initial_cash
        self._newStrategy.add(timestamp=timestamp,listOfRecords=listOfRecord,cash=initial_cash,equity=initial_cash)

    def get_last_shareNum(self):
        last_port = self.get_last_portfolio()
        dic = {}
        for element in last_port:
            dic[element] = last_port[element].NumOfShare
        return dic

    def append(self,timeStamp,updated_record,updated_cash,updated_equity):
        self._newStrategy.add(timestamp=timeStamp, listOfRecords=updated_record, cash=updated_cash,
                              equity=updated_equity)

if __name__=='__main__':
    testt = Basic_strategy()
