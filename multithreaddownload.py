import json
import concurrent.futures
import time
from urllib.request import urlopen

api_key = "69e09ca16aff5a81a2ff3dbf9da36f23"
tickerliste = "AAPL  MSFT AMZN FB GOOGL TSLA BRK.B JPM JNJ V UNH DIS NVDA HD PG MA BAC PYPL INTC CMCSA XOM VZ NFLX ADBE CSCO T ABT CVX KO PFE CRM MRK PEP AVGO ABBV WMT TMO TXN ACN NKE MCD WFC MDT COST QCOM C HON NEE UNP LLY LIN AMGN DHR BMY LOW BA PM ORCL AMAT SBUX CAT UPS IBM RTX MS DE GE GS MMM BLK INTU AMT MU TGT NOW SCHW AMD BKNG CVS MO LRCX FIS ISRG SPGI ANTM CHTR CI GILD MDLZ ADP PLD TFC SYK TJX USB CCI PNC ZTS TMUS CSX ATVI DUK CME GM COP CB FISV BDX FDX NSC CL EL SO ICE ITW APD MMC ADSK GPN D EQIX SHW COF ADI NXPI ILMN PGR ETN VRTX BSX EMR ECL KLAC HUM AON EW TWTR WM REGN NOC DG "
tickerliste=tickerliste.split()
print(len(tickerliste))

def get_data(link):
    try:  
        r = urlopen(link)
        data = json.loads(r.read().decode("utf-8"))
        print(data, "\n")
        
    except:
        pass

def get_ticker(ticker):

    quoter = "https://financialmodelingprep.com/api/v3/quote/" + ticker + "?apikey=" + api_key
    balancer = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/" + ticker + "?limit=1" + "&apikey=" + api_key
    cashflowr = "https://financialmodelingprep.com/api/v3/cash-flow-statement/" + ticker + "?limit=1" + "&apikey=" + api_key
    DCFr = "https://financialmodelingprep.com/api/v3/discounted-cash-flow/" + ticker + "?apikey=" + api_key
    incomer = "https://financialmodelingprep.com/api/v3/income-statement/" + ticker + "?limit=4" + "&apikey=" + api_key
    link_list = [quoter, balancer, cashflowr, DCFr, incomer]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(get_data, link_list)

time1 = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        executor.map(get_ticker, tickerliste)

#for ticker in tickerliste:
#    get_ticker(ticker)

time2 = time.perf_counter()
print(time2-time1)
