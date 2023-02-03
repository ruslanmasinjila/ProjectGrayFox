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
import time
import os

import winsound
duration  = 50
freq1     = 1500
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
mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15,M20,M30,H1,H2,H3,H4,H6,H8,H12,D1]
strTimeframe   = ["M1","M2","M3","M4","M5","M6","M10","M12","M15","M20","M30","H1","H2","H3","H4","H6","H8","H12","D1"]

numCandles     = 1000
offset         = 1

Signals   = []

##########################################################################################


# In[1]:


def getSignals(rates_frame,strTimeframe):
    
    rates_frame["tema50"] = ta.tema(rates_frame["close"],length=50)
    rates_frame["tema45"] = ta.tema(rates_frame["close"],length=45)
    rates_frame["tema40"] = ta.tema(rates_frame["close"],length=40)
    rates_frame["tema35"] = ta.tema(rates_frame["close"],length=35)
    rates_frame["tema30"] = ta.tema(rates_frame["close"],length=30)
    rates_frame["tema25"] = ta.tema(rates_frame["close"],length=25)
    rates_frame["tema20"] = ta.tema(rates_frame["close"],length=20)
    
   
    currentTEMA50             = rates_frame["tema50"].iloc[-1]
    currentTEMA45             = rates_frame["tema45"].iloc[-1]
    currentTEMA40             = rates_frame["tema40"].iloc[-1]
    currentTEMA35             = rates_frame["tema35"].iloc[-1]
    currentTEMA30             = rates_frame["tema30"].iloc[-1]
    currentTEMA25             = rates_frame["tema25"].iloc[-1]
    currentTEMA20             = rates_frame["tema20"].iloc[-1]
    
    previousTEMA50            = rates_frame["tema50"].iloc[-2]
    previousTEMA45            = rates_frame["tema45"].iloc[-2]
    previousTEMA40            = rates_frame["tema40"].iloc[-2]
    previousTEMA35            = rates_frame["tema35"].iloc[-2]
    previousTEMA30            = rates_frame["tema30"].iloc[-2]
    previousTEMA25            = rates_frame["tema25"].iloc[-2]
    previousTEMA20            = rates_frame["tema20"].iloc[-2]
    
    
    
    # BUY SIGNAL
    if(previousTEMA50<previousTEMA45 and
       previousTEMA45<previousTEMA40 and
       previousTEMA40<previousTEMA35 and
       previousTEMA35<previousTEMA30 and
       previousTEMA30<previousTEMA25 and
       previousTEMA25<previousTEMA20):
        pass
    else:     
        if(currentTEMA50<currentTEMA45 and
           currentTEMA45<currentTEMA40 and
           currentTEMA40<currentTEMA35 and
           currentTEMA35<currentTEMA30 and
           currentTEMA30<currentTEMA25 and
           currentTEMA25<currentTEMA20):
            Signals.append("[BUY " + strTimeframe + "]")
            
    # BUY SIGNAL
    if(previousTEMA50>previousTEMA45 and
       previousTEMA45>previousTEMA40 and
       previousTEMA40>previousTEMA35 and
       previousTEMA35>previousTEMA30 and
       previousTEMA30>previousTEMA25 and
       previousTEMA25>previousTEMA20):
        pass
    else:     
        if(currentTEMA50>currentTEMA45 and
           currentTEMA45>currentTEMA40 and
           currentTEMA40>currentTEMA35 and
           currentTEMA35>currentTEMA30 and
           currentTEMA30>currentTEMA25 and
           currentTEMA25>currentTEMA20):
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
        display+="["+cp+"]"+"\n"
        Signals =[]
        for t in range(len(mt5Timeframe)):
            rates_frame = getRates(cp, mt5Timeframe[t], numCandles)
            getSignals(rates_frame,strTimeframe[t])
        if(len(Signals)>0):
            
            M1Signals      = ("[BUY M1]"  in Signals or 
                              "[SELL M1]" in Signals)
            
            M2_M5Signals   = ("[BUY M2]"  in Signals or
                              "[BUY M3]"  in Signals or
                              "[BUY M4]"  in Signals or
                              "[BUY M5]"  in Signals or
                              "[SELL M2]" in Signals or
                              "[SELL M3]" in Signals or
                              "[SELL M4]" in Signals or
                              "[SELL M5]" in Signals)
            
            if(M1Signals):
                display+="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX "+" ".join(Signals)+"\n"
                winsound.Beep(freq1, duration)
                
            elif(M2_M5Signals):
                display+="OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO "+" ".join(Signals)+"\n"
                winsound.Beep(freq1, duration)
                
            else:
                display+="******************************************** "+" ".join(Signals)+"\n"
                winsound.Beep(freq2, duration)

        display+="==============================\n"
    print(display)
    time.sleep(60)
    os.system('cls' if os.name == 'nt' else 'clear')
##########################################################################################

