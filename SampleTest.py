from Base_Strategy import Basic_strategy
from dbCon import MONGODB
import pandas as pd
from StockRecord import Records


class idots_strategy(Basic_strategy):
    def data_handler(self,front_df,back_df):
        last_share = self.get_last_shareNum()
        front_record = Records('Apr 16',last_share['Apr 16'],front_df['item'].item(),front_df['Settle'].item())
        back_record = Records('May 16',last_share['May 16'],front_df['item'].item(),front_df['Settle'].item())
        return front_record,back_record





if __name__=='__main__':
    dbCon = MONGODB('stock_data')
    front_vix = dbCon.read_mongo('VIX_2016',{'_id':'CFE_J16_VX'})[0]
    back_vix = dbCon.read_mongo('VIX_2016',{'_id':'CFE_K16_VX'})[0]
    print(front_vix.index)
    idots = idots_strategy()
    first_recordfront = Records('Apr 16',0,front_vix[0:1]['Open'].item(),front_vix[0:1]['Settle'].item())
    first_recordback = Records('May 16', 0, back_vix[0:1]['Open'].item(), back_vix[0:1]['Settle'].item())
    idots.initiate([first_recordfront,first_recordback],10000,front_vix[0:1].index[0])

