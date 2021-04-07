import json
import concurrent.futures
import time
from urllib.request import urlopen

api_key = "60791a05960a90f65b7fcbb8710d731e"
ticker = "FB"


def get_data(link):
    try:  
        r = urlopen(link)
        data = json.loads(r.read().decode("utf-8"))
        return data
        
    except Exception as err:
        return err
        

def get_ticker(ticker):

    quoter = "https://financialmodelingprep.com/api/v3/quote/" + ticker + "?apikey=" + api_key
    balancer = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/" + ticker + "?limit=1" + "&apikey=" + api_key
    cashflowr = "https://financialmodelingprep.com/api/v3/cash-flow-statement/" + ticker + "?limit=1" + "&apikey=" + api_key
    DCFr = "https://financialmodelingprep.com/api/v3/discounted-cash-flow/" + ticker + "?apikey=" + api_key
    incomer = "https://financialmodelingprep.com/api/v3/income-statement/" + ticker + "?limit=4" + "&apikey=" + api_key
    link_list = [quoter, balancer, cashflowr, DCFr, incomer]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        threadlist = {executor.submit(get_data, link): link for link in link_list}
    
    return [thread.result() for thread in threadlist]    

time1 = time.perf_counter()

quote, balance, cashflow, DCF, income = get_ticker(ticker)
print(quote, balance, cashflow, DCF, income, sep="\n\n")

time2 = time.perf_counter()
print(time2-time1)
