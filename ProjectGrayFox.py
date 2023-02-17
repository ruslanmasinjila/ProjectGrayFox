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
freq1     = 2000
freq2     = 1000

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

numCandles     = 200
offset         = 1
Signals        = []

##########################################################################################


# In[1]:


def getSignals(rates_frame,strTimeframe):
    
    
    ichimokuValues            =  ta.ichimoku(rates_frame["high"], rates_frame["low"], rates_frame["close"])
    currentOpen               = rates_frame["open"].iloc[-1]
    currentClose              = rates_frame["close"].iloc[-1]
    currentHigh               = rates_frame["high"].iloc[-1]
    currentLow                = rates_frame["low"].iloc[-1]
    currentIsGreen            = (currentClose > currentOpen)
    currentIsRed              = (currentClose < currentOpen)
    currentSenkouSpanA        =  ichimokuValues[0]["ISA_9"].iloc[-1]      
    currentSenkouSpanB        =  ichimokuValues[0]["ISB_26"].iloc[-1]
    
    previousOpen              = rates_frame["open"].iloc[-2]
    previousClose             = rates_frame["close"].iloc[-2]
    previousHigh              = rates_frame["high"].iloc[-2]
    previousLow               = rates_frame["low"].iloc[-2]
    previousIsGreen           = (previousClose > previousOpen)
    previousIsRed             = (previousClose < previousOpen)
    previousSenkouSpanA       =  ichimokuValues[0]["ISA_9"].iloc[-2]      
    previousSenkouSpanB       =  ichimokuValues[0]["ISB_26"].iloc[-2]
 
    
    # BUY SIGNAL
    if(currentLow  > previousLow and currentHigh > previousHigh):
        if(currentClose > previousHigh):
            if(((currentOpen  < currentSenkouSpanA  or currentOpen  < currentSenkouSpanB)  and (currentClose  > currentSenkouSpanA  and currentClose  > currentSenkouSpanB)) or
               ((previousOpen < previousSenkouSpanA or previousOpen < previousSenkouSpanB) and (previousClose > previousSenkouSpanA and previousClose > previousSenkouSpanB))):
                Signals.append("[BUY " + strTimeframe + " NOW]")
            elif(currentLow > currentSenkouSpanA and currentLow > currentSenkouSpanB):
                Signals.append("[BUY " + strTimeframe + "]")
            else:
                Signals.append("==")
                

    # SELL SIGNAL
    if(currentLow < previousLow and currentHigh < previousHigh):
        if(currentClose < previousLow):
            if(((currentOpen  > currentSenkouSpanA  or currentOpen  > currentSenkouSpanB)  and (currentClose  < currentSenkouSpanA  and currentClose  < currentSenkouSpanB)) or
               ((previousOpen > previousSenkouSpanA or previousOpen > previousSenkouSpanB) and (previousClose < previousSenkouSpanA and previousClose < previousSenkouSpanB))):
                Signals.append("[SELL " + strTimeframe + " NOW]")
            elif(currentHigh < currentSenkouSpanA and currentHigh < currentSenkouSpanB):
                Signals.append("[SELL " + strTimeframe + "]")
            else:
                Signals.append("==")
                

                    
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
        display+="["+cp+"]"+"\n"
        Signals =[]
        
        for t in range(len(mt5Timeframe)):
            rates_frame = getRates(cp, mt5Timeframe[t], numCandles)
            getSignals(rates_frame,strTimeframe[t])
            
        sameSignals = []
        if(len(Signals)>0): 
            if("BUY" in Signals[0]):
                for i in Signals:
                    if("BUY" in i):
                        sameSignals.append(i)
                    else:
                        break
            elif("SELL" in Signals[0]):
                for i in Signals:
                    if("SELL" in i):
                        sameSignals.append(i)
                    else:
                        break
            if(len(sameSignals)>0):
                if(sameSignals[0]=="[BUY M1 NOW]" or sameSignals[0]=="[SELL M1 NOW]"):
                    display+="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  "+ str(len(sameSignals))+"\n"+" ".join(sameSignals)+"\n"
                    winsound.Beep(freq1, duration)
                elif(sameSignals[0]=="[BUY M1]" or sameSignals[0]=="[SELL M1]"):
                    display+="**************************************************  "+ str(len(sameSignals))+"\n"+" ".join(sameSignals)+"\n"
                    winsound.Beep(freq2, duration)

        display+="==============================\n"
    print(display)
    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    
##########################################################################################

