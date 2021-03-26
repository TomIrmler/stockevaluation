profile = fa.profile(ticker, api_key)


elif input_main[0] == "info":
                if len(input_main) == 2:
                    print(info(input_main[1]))
                else:
                    print('Geben Sie EIN Ticker Symbol hinter "info" ein.')


def info(ticker):
    name = profile["companyName"]
    exchangeShortName = profile["exchangeShortName"]
    sector = profile["sector"]
    description = profile["description"]
    fullTimeEmployees = profile["fullTimeEmployees"]
    ceo = profile["ceo"]
    address = profile["adress"]

    return(info)

