#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##########################################################################################
# ProjectGrayFox
# AUTHOR: RUSLAN MASINJILA
##########################################################################################
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import numpy as np
import more_itertools as mit
import time
import os

import winsound
duration  = 50
freq      = 1500

# NUMBER OF COLUMNS TO BE DISPLAYED
pd.set_option('display.max_columns', 500)

# MAXIMUM TABLE WIDTH TO DISPLAY
pd.set_option('display.width', 1500)      
 
# ESTABLISH CONNECTION TO MT5 TERMINAL
if not mt5.initialize():
    print("initialize() FAILED, ERROR CODE =",mt5.last_error())
    quit()

##########################################################################################


# In[ ]:


# MT5 TIMEFRAME
MN1  = mt5.TIMEFRAME_MN1
W1   = mt5.TIMEFRAME_W1
D1   = mt5.TIMEFRAME_D1
H12  = mt5.TIMEFRAME_H12
H8   = mt5.TIMEFRAME_H8
H6   = mt5.TIMEFRAME_H6
H4   = mt5.TIMEFRAME_H4
H3   = mt5.TIMEFRAME_H3
H2   = mt5.TIMEFRAME_H2
H1   = mt5.TIMEFRAME_H1
M30  = mt5.TIMEFRAME_M30
M20  = mt5.TIMEFRAME_M20
M15  = mt5.TIMEFRAME_M15
M12  = mt5.TIMEFRAME_M12
M10  = mt5.TIMEFRAME_M10
M6   = mt5.TIMEFRAME_M6
M5   = mt5.TIMEFRAME_M5
M4   = mt5.TIMEFRAME_M4
M3   = mt5.TIMEFRAME_M3
M2   = mt5.TIMEFRAME_M2
M1   = mt5.TIMEFRAME_M1

currency_pairs = None
with open('instruments.txt') as f:
    currency_pairs = [line.rstrip('\n') for line in f]


# TIMEFRAMES
mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15,M20,M30,H1,H2,H3,H4,H6,H8,H12,D1,W1,MN1]
strTimeframe   = ["M1","M2","M3","M4","M5","M6","M10","M12","M15","M20","M30","H1","H2","H3","H4","H6","H8","H12","D1","W1","MN1"]

numCandles     = 6
offset         = 1

Signals   = []

##########################################################################################


# In[1]:


def getSignals(rates_frame,strTimeframe):
    
    firstOpen                =      rates_frame["open"].iloc[-1]
    firstHigh                =      rates_frame["high"].iloc[-1]
    firstLow                 =      rates_frame["low"].iloc[-1]
    firstClose               =      rates_frame["close"].iloc[-1]
    firstSize                =      abs(firstClose - firstOpen)
    firstIsGreen             =      (firstClose > firstOpen)
    firstIsRed               =      (firstClose < firstOpen)
    
    secondOpen               =      rates_frame["open"].iloc[-2]
    secondHigh               =      rates_frame["high"].iloc[-2]
    secondLow                =      rates_frame["low"].iloc[-2]
    secondClose              =      rates_frame["close"].iloc[-2]
    secondSize               =      abs(secondClose - secondOpen)
    secondIsGreen            =      (secondClose > secondOpen)
    secondIsRed              =      (secondClose < secondOpen)
    
    thirdOpen                =      rates_frame["open"].iloc[-3]
    thirdHigh                =      rates_frame["high"].iloc[-3]
    thirdLow                 =      rates_frame["low"].iloc[-3]
    thirdClose               =      rates_frame["close"].iloc[-3]
    thirdSize                =      abs(thirdClose - thirdOpen)
    thirdIsGreen             =      (thirdClose > thirdOpen)
    thirdIsRed               =      (thirdClose < thirdOpen)
    
    fourthOpen               =      rates_frame["open"].iloc[-4]
    fourthHigh               =      rates_frame["high"].iloc[-4]
    fourthLow                =      rates_frame["low"].iloc[-4]
    fourthClose              =      rates_frame["close"].iloc[-4]
    fourthSize               =      abs(fourthClose - fourthOpen)
    fourthIsGreen            =      (fourthClose > fourthOpen)
    fourthIsRed              =      (fourthClose < fourthOpen)
    
    fifthOpen                =      rates_frame["open"].iloc[-5]
    fifthHigh                =      rates_frame["high"].iloc[-5]
    fifthLow                 =      rates_frame["low"].iloc[-5]
    fifthClose               =      rates_frame["close"].iloc[-5]
    fifthSize                =      abs(fifthClose - fifthOpen)
    fifthIsGreen             =      (fifthClose  > fifthOpen)
    fifthIsRed               =      (fifthClose < fifthOpen)
    
    
    #####################################################################################################
    # BUY SIGNAL
    #####################################################################################################
    
    if(thirdIsRed):
        if(fourthIsGreen and secondIsGreen):
            if(thirdLow < firstLow and thirdLow < secondLow):
                if(thirdLow < fourthLow and thirdLow < fifthLow):
                    Signals.append("[BUY " + strTimeframe + "]")

    #####################################################################################################
    # SELL SIGNAL
    #####################################################################################################

    if(thirdIsGreen):
        if(fourthIsRed and secondIsRed):
            if(thirdHigh > firstHigh and thirdHigh > secondHigh):
                if(thirdHigh > fourthHigh and thirdHigh > fifthHigh):
                    Signals.append("[SELL " + strTimeframe + "]")
    
##########################################################################################


# In[ ]:


# Gets the most recent <numCandles> prices for a specified <currency_pair> and <mt5Timeframe>
def getRates(currency_pair, mt5Timeframe, numCandles):
    rates_frame =  mt5.copy_rates_from_pos(currency_pair, mt5Timeframe, offset, numCandles)
    rates_frame = pd.DataFrame(rates_frame)
    return rates_frame

##########################################################################################


# In[ ]:


banner = ""
banner+="##############################\n"
banner+="           SIGNALS            \n"
banner+="##############################\n"
while(True):
    
    display = banner
    for cp in currency_pairs:
        Signals =[]
        
        for t in range(len(mt5Timeframe)):
            rates_frame = getRates(cp, mt5Timeframe[t], numCandles)
            getSignals(rates_frame,strTimeframe[t])
            
        if(len(Signals)>0):
            display+="["+cp+"]: "+ "******** "+" ".join(Signals)+"\n"
    print(display)
    time.sleep(60)
    os.system('cls' if os.name == 'nt' else 'clear')
    
##########################################################################################

