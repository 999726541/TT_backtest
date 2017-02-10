#-*- coding:UTF-8 -*-

import datetime
import json
import numpy as np
import pandas as pd

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