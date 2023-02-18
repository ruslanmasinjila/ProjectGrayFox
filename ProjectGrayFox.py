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
freq1     = 1500
freq2     = 2000

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

numCandles     = 2
offset         = 0
buySignals     = []
sellSignals    = []

##########################################################################################


# In[1]:


def getbuySignals(rates_frame,strTimeframe):
    
    
    currentOpen               = rates_frame["open"].iloc[-1]
    currentClose              = rates_frame["close"].iloc[-1]
    currentIsGreen            = (currentClose > currentOpen)
    currentIsRed              = (currentClose < currentOpen)
    
    # BUY SIGNAL
    if(currentIsGreen):
        buySignals.append("[BUY " + strTimeframe + "]")
    else:
        buySignals.append("X")
                

    # SELL SIGNAL
    if(currentIsRed):
        sellSignals.append("[SELL " + strTimeframe + "]")
    else:
        sellSignals.append("X")
              
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

        buySignals     = []
        sellSignals    = []
        
        for t in range(len(mt5Timeframe)):
            rates_frame = getRates(cp, mt5Timeframe[t],numCandles)
            getbuySignals(rates_frame,strTimeframe[t])
            
        consecutiveBuySignals = []
        if(len(buySignals)>0): 
            if(buySignals[0]=="[BUY M1]"):
                for i in buySignals:
                    if("BUY" in i):
                        consecutiveBuySignals.append(i)
                    else:
                        break
        consecutiveSellSignals = []
        if(len(sellSignals)>0):
            if(sellSignals[0]=="[SELL M1]"):
                for i in sellSignals:
                    if("SELL" in i):
                        consecutiveSellSignals.append(i)
                    else:
                        break
                        
        if(len(consecutiveBuySignals)>0):
            if(len(consecutiveBuySignals)<=18):
                display+="["+cp+"]: "+"********************  "+"[" + '{:02d}'.format(len(consecutiveBuySignals))  + "]" + " " + consecutiveBuySignals[-1] + "\n"
                winsound.Beep(freq1, duration)
            else:
                display+="["+cp+"]: "+"XXXXXXXXXXXXXXXXXXXX  "+"[" + '{:02d}'.format(len(consecutiveBuySignals))  + "]" + " " + consecutiveBuySignals[-1] + "\n"
                winsound.Beep(freq2, duration)
                
            
        if(len(consecutiveSellSignals)>0):
            if(len(consecutiveSellSignals)<=18):
                display+="["+cp+"]: "+"********************  "+"[" + '{:02d}'.format(len(consecutiveSellSignals)) + "]" + " " + consecutiveSellSignals[-1] + "\n"
                winsound.Beep(freq1, duration)
            else:
                display+="["+cp+"]: "+"XXXXXXXXXXXXXXXXXXXX  "+"[" + '{:02d}'.format(len(consecutiveSellSignals)) + "]" + " " + consecutiveSellSignals[-1] + "\n"
                winsound.Beep(freq2, duration)
            
    print(display)
    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    
##########################################################################################

