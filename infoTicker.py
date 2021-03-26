import FundamentalAnalysis as fa

api_key = 'e438c06772eb98390b1e07e0ab32b4bc'
ticker = 'AAPL'

elif input_main[0] == "info":
                if len(input_main) == 2:
                    print(rate(input_main[1]))
                else:
                    print('Geben Sie EIN Ticker Symbol hinter "info" ein.')


def info(ticker):
    profile = fa.profile(ticker, api_key)
    return profile

