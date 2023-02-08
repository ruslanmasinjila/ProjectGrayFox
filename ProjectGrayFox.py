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
mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15,M20,M30,H1,H2,H3,H4,H6,H8,H12,D1]
strTimeframe   = ["M1","M2","M3","M4","M5","M6","M10","M12","M15","M20","M30","H1","H2","H3","H4","H6","H8","H12","D1"]

numCandles     = 200
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
    
    tenkanSen_0                               =  ichimokuValues[0]["ITS_9"].iloc[-1]      
    kijunSen_0                                =  ichimokuValues[0]["IKS_26"].iloc[-1]     
    senkouSpanA_0                             =  ichimokuValues[0]["ISA_9"].iloc[-1]      
    senkouSpanB_0                             =  ichimokuValues[0]["ISB_26"].iloc[-1]
    candleClose_0                             =  rates_frame["close"].iloc[-1]
    
    chikouSpan_L26                            =  ichimokuValues[0]["ICS_26"].iloc[-27]
    tenkanSen_L26                             =  ichimokuValues[0]["ITS_9"].iloc[-27]      
    kijunSen_L26                              =  ichimokuValues[0]["IKS_26"].iloc[-27]     
    senkouSpanA_L26                           =  ichimokuValues[0]["ISA_9"].iloc[-27]      
    senkouSpanB_L26                           =  ichimokuValues[0]["ISB_26"].iloc[-27]
    candleOpen_L26                            =  rates_frame["open"].iloc[-27]
    candleClose_L26                           =  rates_frame["close"].iloc[-27]

    
    senkouSpanA_R26                           =  ichimokuValues[1]["ISA_9"].iloc[-1]      
    senkouSpanB_R26                           =  ichimokuValues[1]["ISB_26"].iloc[-1]
    
    currentRSI_0                              =  rates_frame.iloc[-1].rsi26
    currentRSI_L26                            =  rates_frame.iloc[-27].rsi26
    
    #####################################################################################################
    # PREVIOUS STATE
    #####################################################################################################
    
    tenkanSen_L1                              =  ichimokuValues[0]["ITS_9"].iloc[-2]      
    kijunSen_L1                               =  ichimokuValues[0]["IKS_26"].iloc[-2]     
    senkouSpanA_L1                            =  ichimokuValues[0]["ISA_9"].iloc[-2]      
    senkouSpanB_L1                            =  ichimokuValues[0]["ISB_26"].iloc[-2]
    candleClose_L1                            =  rates_frame["close"].iloc[-2]
    
    chikouSpan_L27                            =  ichimokuValues[0]["ICS_26"].iloc[-28]
    tenkanSen_L27                             =  ichimokuValues[0]["ITS_9"].iloc[-28]      
    kijunSen_L27                              =  ichimokuValues[0]["IKS_26"].iloc[-28]     
    senkouSpanA_L27                           =  ichimokuValues[0]["ISA_9"].iloc[-28]      
    senkouSpanB_L27                           =  ichimokuValues[0]["ISB_26"].iloc[-28]
    candleOpen_L27                            =  rates_frame["open"].iloc[-28]
    candleClose_L27                           =  rates_frame["close"].iloc[-28]
    
    senkouSpanA_R25                           =  ichimokuValues[1]["ISA_9"].iloc[-2]      
    senkouSpanB_R25                           =  ichimokuValues[1]["ISB_26"].iloc[-2]
    
    previousRSI_0                             =  rates_frame.iloc[-2].rsi26
    previousRSI_L27                           =  rates_frame.iloc[-28].rsi26
    
    #####################################################################################################
    # BUY SIGNAL
    #####################################################################################################
    
    previousBuyCondition =  (candleClose_L1   >  tenkanSen_L1    and
                             tenkanSen_L1     >  kijunSen_L1     and
                             kijunSen_L1      >  senkouSpanA_L1  and
                             kijunSen_L1      >  senkouSpanB_L1  and
                            
                             chikouSpan_L27   >  tenkanSen_L27   and
                             chikouSpan_L27   >  kijunSen_L27    and
                             chikouSpan_L27   >  senkouSpanA_L27 and
                             chikouSpan_L27   >  senkouSpanB_L27 and
                             chikouSpan_L27   >  candleOpen_L27  and
                             chikouSpan_L27   >  candleClose_L27 and
                             senkouSpanA_R25  >  senkouSpanB_R25 and
                             previousRSI_0    >  50              and
                             previousRSI_L27  >  50)
    
    # Previous Top Line of Sight between Chikou Span and current candle close
    previousTopLOS       = ((chikouSpan_L27   >  rates_frame["open"].iloc[-27:-3]).all() and
                            (chikouSpan_L27   >  rates_frame["close"].iloc[-27:-3]).all())
    
    
    currentBuyCondition  =  (candleClose_0    >  tenkanSen_0     and
                             tenkanSen_0      >  kijunSen_0      and
                             kijunSen_0       >  senkouSpanA_0   and
                             kijunSen_0       >  senkouSpanB_0   and
                            
                             chikouSpan_L26   >  tenkanSen_L26   and
                             chikouSpan_L26   >  kijunSen_L26    and
                             chikouSpan_L26   >  senkouSpanA_L26 and
                             chikouSpan_L26   >  senkouSpanB_L26 and
                             chikouSpan_L26   >  candleOpen_L26  and
                             chikouSpan_L26   >  candleClose_L26 and
                             senkouSpanA_R26  >  senkouSpanB_R26 and
                             currentRSI_0     >  50              and
                             currentRSI_L26   >  50)
    
    # Current Top Line of Sight between Chikou Span and current candle close
    currentTopLOS        = ((chikouSpan_L26   >  rates_frame["open"].iloc[-26:-2]).all()  and
                            (chikouSpan_L26   >  rates_frame["close"].iloc[-26:-2]).all())
    

                            
    if((previousBuyCondition and previousTopLOS == False) and (currentBuyCondition and currentTopLOS  == True)):
        Signals.append("[BUY " + strTimeframe + " NOW]")
        
    elif(previousBuyCondition == True  and currentBuyCondition == True):
        Signals.append("[BUY " + strTimeframe + "]")  
        
    #####################################################################################################
    # SELL SIGNAL
    #####################################################################################################

    previousSellCondition  = (candleClose_L1  <  tenkanSen_L1    and
                              tenkanSen_L1    <  kijunSen_L1     and
                              kijunSen_L1     <  senkouSpanA_L1  and
                              kijunSen_L1     <  senkouSpanB_L1  and
                              
                              chikouSpan_L27  <  tenkanSen_L27   and
                              chikouSpan_L27  <  kijunSen_L27    and
                              chikouSpan_L27  <  senkouSpanA_L27 and
                              chikouSpan_L27  <  senkouSpanB_L27 and
                              chikouSpan_L27  <  candleOpen_L27  and
                              chikouSpan_L27  <  candleClose_L27 and
                              senkouSpanA_R25 <  senkouSpanB_R25 and
                              previousRSI_0   <  50              and
                              previousRSI_L27 <  50)
    
    # Previous Bottom Line of Sight between Chikou Span and current candle close
    previousBottomLOS     = ((chikouSpan_L27  <  rates_frame["open"].iloc[-27:-3]).all() and
                            (chikouSpan_L27   <  rates_frame["close"].iloc[-27:-3]).all())
    
    
    currentSellCondition  = (candleClose_0    <  tenkanSen_0     and
                             tenkanSen_0      <  kijunSen_0      and
                             kijunSen_0       <  senkouSpanA_0   and
                             kijunSen_0       <  senkouSpanB_0   and
         
                             chikouSpan_L26   <  tenkanSen_L26   and
                             chikouSpan_L26   <  kijunSen_L26    and
                             chikouSpan_L26   <  senkouSpanA_L26 and
                             chikouSpan_L26   <  senkouSpanB_L26 and
                             chikouSpan_L26   <  candleOpen_L26  and
                             chikouSpan_L26   <  candleClose_L26 and
                             senkouSpanA_R26  <  senkouSpanB_R26 and
                             currentRSI_0     <  50              and
                             currentRSI_L26   <  50)
    
    # Current Bottom Line of Sight between Chikou Span and current candle close
    currentBottomLOS      = ((chikouSpan_L26  <  rates_frame["open"].iloc[-26:-2]).all()  and
                            (chikouSpan_L26   <  rates_frame["close"].iloc[-26:-2]).all())
    

    if((previousSellCondition and previousBottomLOS == False) and (currentSellCondition and currentBottomLOS  == True)):
        Signals.append("[SELL " + strTimeframe + " NOW]")
    
    elif(previousSellCondition == True  and currentSellCondition == True):
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
            #if(all("BUY" in Signal for Signal in Signals) or all("SELL" in Signal for Signal in Signals)):
            if(Signals[0]=="[BUY M1]" or Signals[0]=="[SELL M1]"):
                display+="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"+" ".join(Signals)+"\n"
                winsound.Beep(freq1, duration)
            else:
                display+="********************************************\n"+" ".join(Signals)+"\n"
                winsound.Beep(freq2, duration)
                
        display+="==============================\n"
    print(display)
    time.sleep(60)
    os.system('cls' if os.name == 'nt' else 'clear')
    
##########################################################################################

