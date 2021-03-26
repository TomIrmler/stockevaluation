import FundamentalAnalysis as fa

api_key = "e438c06772eb98390b1e07e0ab32b4bc"

ticker = "AAPL"

DCF = fa.discounted_cash_flow(ticker, api_key).iloc[:,0]

Stockprice = DCF["Stock Price"]
dcf = DCF["DCF"]


def rateDCFV(Stockprice, dcf):
    DCFV = dcf/Stockprice
    schwellenwerte=[2 ,1.75, 1.5, 1.25, 1, 0.8, 0.6, 0.4]

    if DCFV>=2.5:
        return 1

    elif DCFV<=0.4:
        return 8

    else:
        score=2
        i=0



        while DCFV<schwellenwerte[i]:
            score +=1
            i+=1

    return score


print(rateDCFV(Stockprice, dcf))

