from Base_Strategy import Basic_strategy
from dbCon import MONGODB
import pandas as pd
from StockRecord import Records


class idots_strategy(Basic_strategy):
    def data_handler(self,front_df,back_df):

        # 将原始数据转换成Record格式
        # :return: Record lsit

        last_share = self.get_last_shareNum()
        front_record = Records('Apr 16',last_share['Apr 16'],front_df['Open'].item(),front_df['Settle'].item())
        back_record = Records('May 16',last_share['May 16'],back_df['Open'].item(),back_df['Settle'].item())
        return front_record,back_record

    def long_short_signal(self,listOfRecords:[Records]):
        if self.check_if_in_position() == False:
            return {'Apr 16':-1,'May 16':1}
        else:
            return {'Apr 16':0,'May 16':0}


if __name__=='__main__':
    dbCon = MONGODB('stock_data')
    front_vix = dbCon.read_mongo('VIX_2016',{'_id':'CFE_J16_VX'})[0].iloc[::-1]
    front_vix['Date'] = front_vix.index.to_datetime()
    front_vix.set_index('Date', inplace=True)
    front_vix.sort_index(inplace=True)
    front_vix = front_vix['2015-09-22':'2016-04-20']

    back_vix = dbCon.read_mongo('VIX_2016',{'_id':'CFE_K16_VX'})[0].iloc[::-1]
    back_vix['Date'] = back_vix.index.to_datetime()
    back_vix.set_index('Date', inplace=True)
    back_vix.sort_index(inplace=True)
    back_vix = back_vix['2015-09-22':'2016-04-20']

    #print(pd.concat([front_vix,back_vix[20:]],axis=1).dropna())

    idots = idots_strategy()
    first_recordfront = Records('Apr 16', 0,front_vix[0:1]['Open'].item(),front_vix[0:1]['Settle'].item())
    first_recordback = Records('May 16', 0, back_vix[0:1]['Open'].item(), back_vix[0:1]['Settle'].item())
    idots.initiate([first_recordfront,first_recordback],10000,front_vix[0:1].index[0])
    for i in range(1,len(front_vix)):
        front,back = idots.data_handler(front_vix[i:i+1],back_vix[i:i+1])
        timestamp = front_vix[i:i+1].index[0]
        idots.event_handler({'Apr 16':2000,'May 16':2000},cal_style=0,timeStamp=timestamp,row_data = [front,back])
        #if i == 10: break
    print(idots.display_all_content())




