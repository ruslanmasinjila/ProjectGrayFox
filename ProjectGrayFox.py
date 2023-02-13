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
freq2     = 1500

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

numCandles     = 200
senkouShift    = 3
offset         = 1

Signals   = []

##########################################################################################


# In[1]:


def getSignals(rates_frame,strTimeframe):
    
    ichimokuValues                            =  ta.ichimoku(rates_frame["high"], rates_frame["low"], rates_frame["close"]) # returns ichimokudf, spandf
    rates_frame["rsi26"]                      =  ta.rsi(rates_frame["close"],length=26)
    #####################################################################################################
    # CURRENT STATE
    #####################################################################################################
    
    currentSenkouSpanA                        =  ichimokuValues[0]["ISA_9"].iloc[-1]      
    currentSenkouSpanB                        =  ichimokuValues[0]["ISB_26"].iloc[-1]
    currentCandleHigh                         =  rates_frame["high"].iloc[-1]
    currentCandleLow                          =  rates_frame["low"].iloc[-1]
    
    currentFuturesenkouSpanA                  =  ichimokuValues[1]["ISA_9"].iloc[-senkouShift:]      
    currentFutureSenkouSpanB                  =  ichimokuValues[1]["ISB_26"].iloc[-senkouShift:]
    
    currentRSI26                              =  rates_frame["rsi26"].iloc[-1]
    
    #####################################################################################################
    # PREVIOUS STATE
    #####################################################################################################
       
    previousSenkouSpanA                       =  ichimokuValues[0]["ISA_9"].iloc[-2]      
    previousSenkouSpanB                       =  ichimokuValues[0]["ISB_26"].iloc[-2]
    previousCandleHigh                        =  rates_frame["high"].iloc[-2]
    previousCandleLow                         =  rates_frame["low"].iloc[-2]
    
    previousFuturesenkouSpanA                 =  ichimokuValues[1]["ISA_9"].iloc[-(senkouShift+1):-1]      
    previousFutureSenkouSpanB                 =  ichimokuValues[1]["ISB_26"].iloc[-(senkouShift+1):-1]
    
    previousRSI26                             =  rates_frame["rsi26"].iloc[-2]
    
    #####################################################################################################
    # BUY SIGNAL
    #####################################################################################################
    
    previousBuyCondition =  ((previousFuturesenkouSpanA   >  previousFutureSenkouSpanB).all() and
                              previousCandleLow           >  previousSenkouSpanA              and
                              previousCandleLow           >  previousSenkouSpanB              and
                              previousRSI26               >  50)
    
    
    currentBuyCondition  =  ((currentFuturesenkouSpanA    >  currentFutureSenkouSpanB).all()  and
                              currentCandleLow            >  currentSenkouSpanA               and
                              currentCandleLow            >  currentSenkouSpanB               and
                              currentRSI26                >  50)
                           
    if((previousBuyCondition == False) and (currentBuyCondition == True)):
        Signals.append("[BUY " + strTimeframe + " NOW]")
        
    elif(previousBuyCondition == True  and currentBuyCondition == True):
        Signals.append("[BUY " + strTimeframe + "]")  
        
    #####################################################################################################
    # SELL SIGNAL
    #####################################################################################################
    
    previousSellCondition = ((previousFuturesenkouSpanA   <  previousFutureSenkouSpanB).all() and
                              previousCandleHigh          <  previousSenkouSpanA              and
                              previousCandleHigh          <  previousSenkouSpanB              and
                              previousRSI26               <  50)
    
    
    currentSellCondition  = ((currentFuturesenkouSpanA    <  currentFutureSenkouSpanB).all()  and
                              currentCandleHigh           <  currentSenkouSpanA               and
                              currentCandleHigh           <  currentSenkouSpanB               and
                              currentRSI26                <  50)
                           
    if((previousSellCondition == False) and (currentSellCondition == True)):
        Signals.append("[SELL " + strTimeframe + " NOW]")
        
    elif(previousSellCondition == True  and currentSellCondition == True):
        Signals.append("[SELL " + strTimeframe + "]")  


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
            if(Signals[0]=="[BUY M1]" or Signals[0]=="[BUY M1 NOW]"):
                for i in Signals:
                    if("BUY" in i):
                        sameSignals.append(i)
                    else:
                        break
            elif(Signals[0]=="[SELL M1]" or Signals[0]=="[SELL M1 NOW]"):
                for i in Signals:
                    if("SELL" in i):
                        sameSignals.append(i)
                    else:
                        break
            if(len(sameSignals)>0):
                if(any(["NOW" in item for item in sameSignals])):
                    display+="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  "+ str(len(sameSignals))+"\n"+" ".join(sameSignals)+"\n"
                    winsound.Beep(freq1, duration)
                else:
                    display+="************************************************  "+ str(len(sameSignals))+"\n"+" ".join(sameSignals)+"\n"
                    winsound.Beep(freq2, duration)
                    
                
        display+="==============================\n"
    print(display)
    time.sleep(60)
    os.system('cls' if os.name == 'nt' else 'clear')
    
##########################################################################################

