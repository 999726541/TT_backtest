#-*- coding:UTF-8 -*-

import datetime
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient

class MONGODB():


    ####注意,为了避免too much file error 24,每个表格为一个链接,尽量不要同时打开200+的table############


    def __init__(self, db,host='192.168.0.14', port=27017, username='admin', password='gwise123',):
        '''
        :param db: DataBase name
        :param host:
        :param port:
        :param username:
        :param password:
        '''
        if username and password:
            mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
            self._client = MongoClient(mongo_uri)
        else:
            self._client = MongoClient(host, port)
        self.conn = self._client[db]

    def read_mongo(self, collection, query=None, no_id=True):  #return list

        # 从数据库拿AAPL的股票数据
        # Eg. read_mongo('stock_price',query={'_id':'AAPL'})


        cursor = self.conn[collection].find(query)
        print('getting data...')
        # Expand the cursor and construct the DataFrame
        df = []
        for element in cursor:
            # Delete the _id
            if no_id:
                try:
                    df.append(pd.DataFrame(element).drop('_id', axis=1))
                except Exception as e:
                    raise 'Format of db is not right, plz check the database is {xx:{aaa:bbb}}'
            else:
                try:
                    df.append(pd.DataFrame(element))
                except Exception as e:
                    raise 'Format of db is not right, plz check the database is {xx:{aaa:bbb}}'
        self._client.close()
        return df

    def write_to_mongo(self,df,collection,id=None):
        db = self.conn
        content = json.loads(df.to_json())
        if id != None:
            content['_id'] = id
        db[collection].insert(content)
        self._client.close()

    def append(self,df,collection,id=None):
        dic = {}
        db = self.conn
        columns = list(df.columns)
        for i in range(len(df)):
            for ele in columns:
                dic[ele + '.' +str(df[i:i+1].index[0])] = list(df[i:i+1][ele])[0]
        print(dic)
        db[collection].update({'_id':id},{'$set':dic},True)
        self._client.close()

    def read_origin(self, collection, query=None, no_id=True):
        cursor = self.conn[collection].find(query)
        print('getting data...')
        # Expand the cursor and construct the DataFrame
        self._client.close()
        return [i for i in cursor]



if __name__=='__main__':
    event = MONGODB('stock_data')
    data = event.read_mongo('leo_signal',{'_id':'WIMHY'})[0]
    print(data)
    '''
    data = pd.read_excel('/Users/leotao/Downloads/Book3.xlsx')
    data = data.sort_values('Date')
    data.set_index('Date',inplace=True)
    data['Adj_Close'] = data.Close
    data['Symbol'] = 'WIMHY'
    # update.loc[:,'test']= 'ooo'
    event.write_to_mongo(data,'stock_daily_2015',id = 'WIMHY')
    #event.append(update,'stock_daily_2015',id='AAPL')
    '''

    #print(update)
    #content = json.loads(update.to_json())
    #event.append(update,'stock_price','AAPL')
    #print(event.read_mongo('stock_price',query={'_id':'AAPL'}))