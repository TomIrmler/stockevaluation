#Mehr Informationen auf https://github.com/TomIrmler/stockevaluation
#Gruppenarbeit von Le, Caspar und Tom (11A)

import FundamentalAnalysis as fa
import coinoxr as oxr
from urllib.error import HTTPError

fa_key_list = [
"eac1e8123c3c726a7b4ea0afab0435ae",
"bffa35224a8bfafcb001a86d8f83e9c8",
"e438c06772eb98390b1e07e0ab32b4bc",
"dd9ed4ecf6358d53a810b784681ad599",
"2355734d1486c0599f415923d59c1387",
"5fbfd27ef7db1675a45ab5dc495e4d5c",
"69e09ca16aff5a81a2ff3dbf9da36f23",
"57e021944cf7e0798365be42b1204f52",
"2f0eeac2bc7c37dfeffb3c9df5189d11",
"977acb09f1542f4b0ee486a776ba3f75",
"60791a05960a90f65b7fcbb8710d731e",
"2571916569bb27780b565d4763c8ff51",
"5159debfefae913686331ec86787ab38",
"f2954eaa06c1207b8b5fea46e5843af8",
"9d8cb0c401b232abcf2f30c5be446881",
"43730b668f3faa9dd2d6b51cc1a2e19f",
"710b04258c7c2499e9d741901bfc64cd",
"f555ddf7c9887d53d80383de750168b2",
"3d3548b991f6645d504d30cce4ef1034",
"5c2269c01cf20536ff22a6c420d6f49c",
"0020ef2d96e0f264a8ffd5df676de913",
"69aed82b47593159b4cca43e9822ac10",
"05d509e0fb6763d26f9379dc5b991cb9",
"0f3b3316959b66a95ef0794130caee64",
"6d92662bb3ca726ba12c7b0f9915748c",
"ba3f3065495b04c9bf686206a5184fb8",
"f6f38d3dc1a5b1df39f764ee0d5834cb",
"27d184007110aaf8d53c15423b80db6f",
"16366fe8670fe6bac9ef08ef3f0b449c",
"65c28a0d1a075b479c672532f8d3f847",
"d1846a3511dffd3a0891c19cb6c4b019",
"5f526fc972683e8f2f1ded7ead9b3c13",
"ca2d7911492c920aab10c257daf623c5",
"5c047480a5eb6533dd47853593f594d2",
"6ba601aa917c30bfc514a47c03434095",
"d9257db90df7056b2b7bde9674beb02c",
"a0464683a51a4cb856c947ce9db32f78",
"907fa277ce14f196fad0d0470301e4bd",
"7d6edf8099d7359b459ea810925c7343",
"56c3159c838957ac376cc424d7345bcf",
"68a647e9187d42e33829d2625ce54931",
"bbae43c3bfb2c3c0811ae1ffd9b8d04c",
"5773c17f08fb9fa3afdaafeb37bf4989",
"3acf60a981ae476f3affdd0ea4afcd6b",
"3bdb84aded3c6ece9c6d2ab013903f73",
"ad00601ed189c6f369418c982b2bc640",
"ee002a54d9dfdd97b10c77aff69da47c",
"8c2d3e1727fbc2bcc9216414aa96b009",
"c945da48933f57f71b8aaf7f6561f004",
"c0b7f60dd03a4424e97897303c6291b4",
"008ebc576253d43950dd0ea81590dfbd"
]
fa_key_num = 0
api_key = fa_key_list[0] #apikey noch einfügen
oxr.app_id = "8da07fea22fb4d6d98f657bdcbcad0d5" #man hat 1000 Anfragen im Monat, sprich man kann das Programm 1000 Mal starten, dann halt anderes Konto.        apikey noch einfügen

exchange_rates = oxr.Latest().get()


def Euro(Wert, Währung):

    global exchange_rates
    USDtoEUR = exchange_rates.body["rates"]["EUR"]
    USDtoWährung = exchange_rates.body["rates"][Währung]
    WertinEUR = Wert / USDtoWährung * USDtoEUR
    
    return WertinEUR


def rate(ticker, mode):

    global exchange_rates

    try:
        quote = fa.quote(ticker, api_key)[0] 
        incomeall = fa.income_statement(ticker, api_key, period="annual")
        incomevor0 = incomeall.iloc[:,0] 
        incomevor1 = incomeall.iloc[:,1]
        incomevor3 = incomeall.iloc[:,3]
        balance = fa.balance_sheet_statement(ticker, api_key, period="annual").iloc[:,0]
        cashflow = fa.cash_flow_statement(ticker, api_key, period="annual").iloc[:,0]
        DCF = fa.discounted_cash_flow(ticker, api_key).iloc[:,0]

        statement_currency = incomevor0["reportedCurrency"]
        quote_currency = "USD" 

        if statement_currency not in exchange_rates.body["rates"]:
            return "Error: Die Zahlen der Aktie \"{0}\" sind in einer unbekannten Währung angegeben.".format(ticker)

        ebitda = Euro(incomevor0["ebitda"], statement_currency)  
        ebitdavor1 = Euro(incomevor1["ebitda"], statement_currency)
        ebitdavor3 = Euro(incomevor3["ebitda"], statement_currency)       
        revenue = Euro(incomevor0["revenue"], statement_currency) 
        volume = quote["volume"]
        incomevor1day = incomevor1["acceptedDate"].split()[0]
        price = Euro(quote["price"], quote_currency)
        pricevor1 = Euro(fa.stock_data_detailed(ticker, api_key, begin= incomevor1day, end = incomevor1day).iloc[0][0], quote_currency)
        dividendsPaid = Euro(cashflow["dividendsPaid"], statement_currency)
        sharesOutstanding = quote["sharesOutstanding"]
        totalAssets = Euro(balance["totalAssets"], statement_currency)
        totalLiabilities = Euro(balance["totalLiabilities"], statement_currency)
        stockprice = Euro(DCF["Stock Price"], quote_currency)
        dcf = Euro(DCF["DCF"], quote_currency)
        ebitdaratio = Euro(incomevor0["ebitdaratio"], statement_currency)
        eps = Euro(incomevor0["eps"], statement_currency)

        MargeScore=rateMarge(ebitdaratio)*weight_BruttoMarge*100
        LiquidityScore=rateLiquidity(volume, price)*weight_Aktienliquidität*100
        DividendyieldScore=rateDividenyield(dividendsPaid, sharesOutstanding, price)*weight_Dividendenrendite*100
        UmsatzScore=rateUmsatz(revenue)*weight_Umsatz*100
        EKQScore=rateEKQ(totalAssets,totalLiabilities)*weight_EKQ*100
        KGVScore=rateKGV(price,eps)*weight_KGV*100
        DCFScore=rateDCFV(stockprice,dcf)*weight_DCFV*100
        GewinnwachstumScore=rateGewinnwachstum(ebitda, ebitdavor3)*weight_Gewinnwachstum*100
        KWGWVScore=rateKWGWV(price, pricevor1, ebitda, ebitdavor1)*weight_KWGWV*100
        PayoutRatioScore=ratePayoutRatio(dividendsPaid, sharesOutstanding, eps, mode)*weight_PoR*100

        Gesamtscore=round(KGVScore+MargeScore+EKQScore+DividendyieldScore+UmsatzScore+LiquidityScore+DCFScore+GewinnwachstumScore+KWGWVScore+PayoutRatioScore,2)

        ScoreMargeRound=round(MargeScore,2)
        ScoreLiquidityRound=round(LiquidityScore,2)
        ScoreDividendyieldRound=round(DividendyieldScore,2)
        ScoreUmsatzRound=round(UmsatzScore,2)
        ScoreEKQRound=round(EKQScore,2)
        ScoreKGVRound=round(KGVScore,2)
        ScoreDCFRound=round(DCFScore,2)
        ScoreGewinnwachstumRound=round(GewinnwachstumScore,2)
        ScoreKWGWVRound=round(KWGWVScore,2)
        ScorePayoutRatioRound=round( PayoutRatioScore,2)

        maxMarge=round(weight_BruttoMarge*800,2)
        maxLiquidity=round(weight_Aktienliquidität*800,2)
        maxDividendyield=round(weight_Dividendenrendite*800,2)
        maxEKQ=round(weight_EKQ*800,2)
        maxKGV=round(weight_KGV*800,2)
        maxUmsatz=round(weight_Umsatz*800,2)
        maxDCF=round(weight_DCFV*800,2)
        maxGewinnwachstum=round(weight_Gewinnwachstum*800,2)
        maxKWGWV=round(weight_KWGWV*800,2)
        maxPayoutRatio=round(weight_PoR*800,2)

        nomMarge=round(ebitdaratio*100,2)
        nomdividendyield=round((dividendsPaid*(-1)/sharesOutstanding)/price*100,2)
        nomEKQ=round(((totalAssets-totalLiabilities)/totalAssets)*100,2)
        nomKGV=round(price/eps,2)
        nomLiquidity=round(volume*price/1000000,2)
        nomUmsatz=round(revenue/1000000,2)
        nomDCF=round(dcf/stockprice,2)
        nomGewinnwachstum=round((((ebitda-ebitdavor3)/ebitdavor3)/3)*100,2)
        nomKWGWV=round(((price-pricevor1)/pricevor1)/((ebitda-ebitdavor1)/ebitdavor1),2)
        nomPayoutRatio=round(((dividendsPaid/sharesOutstanding)/eps)*(-100), 2)

        if mode == "compare":
            return Gesamtscore
        
        else:
            return f"""\nDer Gesamtscore für {ticker} beträgt {Gesamtscore} von 800 Punkten.\nDieser Score setzt sich wie folgt zusammen:\n
Ebitda-Marge ({nomMarge}%)\t\t\t\t{ScoreMargeRound} / {maxMarge}
Aktienliquidität ({nomLiquidity} mio.)\t\t\t{ScoreLiquidityRound} / {maxLiquidity}
Dividendenrendite ({nomdividendyield}%)\t\t\t{ScoreDividendyieldRound} / {maxDividendyield}
Umsatzgröße ({nomUmsatz} mio.)\t\t\t{ScoreUmsatzRound} / {maxUmsatz}
Eigenkapitalquote ({nomEKQ}%)\t\t\t{ScoreEKQRound} / {maxEKQ}
KGV ({nomKGV})\t\t\t\t\t{ScoreKGVRound} / {maxKGV}
Kurs-DCF-Verhältnis ({nomDCF})\t\t\t{ScoreDCFRound} / {maxDCF}
Ø-Ebitda Wachstum p.a. ({nomGewinnwachstum}%)\t\t\t{ScoreGewinnwachstumRound} / {maxGewinnwachstum}
Kurswachstum zu Gewinnwachstum ({nomKWGWV})\t\t{ScoreKWGWVRound} / {maxKWGWV}
Payout-Ratio ({nomPayoutRatio}%)\t\t\t\t{ScorePayoutRatioRound} / {maxPayoutRatio}\n"""
    
    except HTTPError as err:
        if err.code == 403:
            if switchkey() == True:
                rate(ticker, mode)
            else:
                return "Alle API-Keys für FundamentalAnalysis sind aufgebraucht."
            
    except:
        return "Ein Fehler ist aufgetreten."

def switchkey():
    global api_key
    global fa_key_num

    try:
        fa_key_num += 1
        api_key = fa_key_list[fa_key_num]
        return True
        
    except IndexError:
        return False 

def compare(tickerliste):
    flist = []
    highest = []
    returnstring = ""
    tabanzahl = len(max(tickerliste))

    print("")

    for ticker in tickerliste:

        rating = [rate(ticker, "compare"), ticker]
        if rating[0] == "Ein Fehler ist aufgetreten.":
            rating[0] = "Fehler"
        
        elif rating[0] == "Alle API-Keys für FundamentalAnalysis sind aufgebraucht.":
            return rating[0]
            
        flist.append(rating)
        print("Ticker {0}/{1} gerated. ({2})".format(tickerliste.index(ticker)+1, len(tickerliste), ticker) + " "*(len(tickerliste[tickerliste.index(ticker)-1])-len(ticker)), end="\r")
    
    flist.sort(key=lambda x: x[0] if x[0] != "Fehler" else -10, reverse=True)
    
    highest = [rating for rating in flist if rating[0] == flist[0][0] and flist[0][0] != "Fehler"]
    failed = [rating for rating in flist if rating[0] == "Fehler"]
    flist = flist[len(highest):[-len(failed) if len(failed) > 0 else None][0]]

    returnstring += "Es wurden insgesamt {0} Ticker gerated, bei {1} ist ein Fehler aufgetreten.".format(len(tickerliste), len(failed))
    returnstring += "\n\nAlle Ergebnisse im Überblick:\nTicker:\t\tScore:\n"

    for index, rating in enumerate(highest):
        if index == 0:
            returnstring += "\n"
        returnstring += "{0}. {1}\t\t{2}\n".format(index+1, rating[1], rating[0])
    
    for index, rating in enumerate(flist):
        if index == 0:
            returnstring += "\n"
        returnstring += "{0}. {1}\t\t{2}\n".format(index+1+len(highest), rating[1], rating[0])

    for index, rating in enumerate(failed):
        if index == 0:
            returnstring += "\n"
        returnstring += "{0}. {1}\t\t{2}\n".format(index+1+len(highest)+len(flist), rating[1], rating[0])

    return returnstring



def rateKGV(price, eps):  
    KGV=price/eps
    schwellenwerte=[300, 70, 40, 25, 15, 10, 0]

    if KGV<=0:
        return 1

    else:
        score=2
        i=0
        while KGV<schwellenwerte[i]:
            score +=1
            i+=1

    return(score)


def rateMarge(Marge): 
    schwellenwerte=[0.01,0.05,0.075,0.1,0.15,0.25,0.35]
    
    if Marge<0.01:
        return 1
        
    elif Marge>=0.35:
        return 8
        
    else:
        score=1
        i=0
        while Marge>=schwellenwerte[i]:
            score+=1
            i+=1

    return(score)


def rateLiquidity(volume, price):
    Liquidity=volume*price
    schwellenwerte = [50000,150000,300000,500000,1000000,2000000,5000000]

    if Liquidity<50000:
        return 1

    elif Liquidity>=5000000:
        return 8

    else:
        score=1
        i=0
        while Liquidity>=schwellenwerte[i]:
            score +=1
            i+=1

    return(score)


def rateDividenyield(dividendpaid, shares, price):
    dividend=dividendpaid*(-1)/shares
    dividendyield=dividend/price
    schwellenwerte=[0,0.01,0.02,0.03,0.035,0.04,0.05]

    if dividendyield ==0:
        return 1

    elif dividendyield>=0.05:
        return 8

    else:
        score=1
        i=0
        while dividendyield>=schwellenwerte[i]:
                score +=1
                i+=1

    return(score)


def rateUmsatz(umsatz):
	schwellenwerte=[500000000,5000000000,15000000000,50000000000,120000000000,200000000000,250000000000,250000000000]

	if umsatz<500000000:
		return 1

	elif umsatz>=250000000000:
		return 8

	else:
		score=1
		i=0
		while umsatz>=schwellenwerte[i]:
			score +=1
			i+=1

	return(score)

def rateEKQ(assets, liabilities):
    EKQ=(assets-liabilities)/assets
    schwellenwerte=[0.02,0.1,0.2,0.3,0.4,0.6,0.8]

    if EKQ<0.02:
        return 1

    elif EKQ>=0.8:
        return 8

    else:
        score=1
        i=0
        while EKQ>schwellenwerte[i]:
            score +=1
            i+=1

    return(score)


def rateDCFV(stockprice, dcf):
    DCFV = stockprice/dcf
    schwellenwerte=[1.5 ,1.3, 1.15, 1.075, 1, 0.9, 0.7, 0.4]

    if DCFV>=1.5:
        return 1

    elif DCFV<=0.4:
        return 8

    else:
        score=1
        i=0
        while DCFV<=schwellenwerte[i]:
            score +=1
            i+=1

    return score


def rateGewinnwachstum(gewinn, gewinnvor3):  
    GewinnWachstum=((gewinn-gewinnvor3)/gewinnvor3)/3
    schwellenwerte=[0,0.05,0.1,0.15,0.25,0.4,0.55]
    
    if GewinnWachstum<=0:
        return 1

    elif GewinnWachstum>=0.55:
        return 8

    else:
        score=1
        i=0
        while GewinnWachstum>=schwellenwerte[i]:
            score+=1
            i+=1

    return(score)


def rateKWGWV(price, pricevor1, gewinn, gewinnvor1):
    KW=(price-pricevor1)/pricevor1
    GW=(gewinn-gewinnvor1)/gewinnvor1
    KWGWV=KW/GW
    schwellenwerte=[0.5,0.75,1,1.4,2,3,4]

    if KWGWV>=4:
        return 1

    elif KWGWV<=0.5:
        return 8

    else:
        score=8
        i=0
        while KWGWV>schwellenwerte[i]:
            score-=1
            i+=1

    return(score)


def ratePayoutRatio(dividendspaid,shares,eps, mode): 
    dividenden=dividendspaid*(-1)
    dps=dividenden/shares
    PoR=dps/eps
    schwellenwerte=[0.05,0.15,0.25,0.4,0.6,0.8]
    
    if dividendspaid==0:
        if mode != "compare":
            print("\nDa keine Dividende gezahlt wurde, wurde bei eine mittlere Einstufung des Payout-Ratio vorgenommen. Ändern Sie am besten die Gewichtung auf 0.")
        return 4

    elif PoR>=0.8:
        return 1

    elif PoR<0:
        return 1 

    elif PoR<=0.05 and PoR>0:
        return 8
        
    else:
        score=8
        i=0
        while PoR>schwellenwerte[i]:
            score-=1
            i+=1

    return(score)    


def showpreferences():  

    print("\nDas ist die aktuelle Gewichtung der Kennzahlen in ihrem Score:\n")
    print("KGV\t\t\t\t{0}%".format(weight_KGV*100))
    print("Ebitda-Marge\t\t\t{0}%".format(weight_BruttoMarge*100))
    print("Eigenkapitalquote\t\t{0}%".format(weight_EKQ*100))
    print("Dividendenrendite\t\t{0}%".format(weight_Dividendenrendite*100))
    print("Umsatz\t\t\t\t{0}%".format(weight_Umsatz*100))
    print("Aktienliquidität\t\t{0}%".format(weight_Aktienliquidität*100))
    print("Kurs-zu-DCF-Verhältnis\t\t{0}%".format(weight_DCFV*100))
    print("Kurswachstum zu Gewinnwachstum\t{0}%".format(weight_Gewinnwachstum*100))
    print("Payout-Ratio\t\t\t{0}%".format(weight_PoR*100))
    print("Gewinnwachstum\t\t\t{0}%\n".format(weight_Gewinnwachstum*100))
   

def helppage():

    print("""\nDas ist die Anleitung zu unserem Programm:\n\nset\t\t\t\t\t- Kennzahlen gewichten\nshow\t\t\t\t\t- aktuelle Gewichtung anzeigen
rate + <Ticker Symbol>\t\t\t- Rating durchführen\nrate + <mehrere Ticker Symbole>\t\t- Aktien vergleichen\ninfo + <Ticker Symbol>\t\t\t- Informationen anzeigen\nende\t\t\t\t\t- Programm beenden\n""")


def askforpref(k_index, total):

    k_strings = ["der KGV", "die Ebitda-Marge", "die Eigenkapitalquote", "die Dividendenrendite", "der Umsatz", "die Aktienliquidität", "das Kurs-zu-DCF-Verhältnis", "das Verhältnis von Kurswachstum zu Gewinnwachstum", "das Payout-Ratio", "das Gewinnwachstum" ]
    k_string = k_strings[k_index]
    übrige = 10-k_index
    return f"\nWie viel Prozent des Scores soll {k_string} ausmachen?\nSie können noch {total}% auf {übrige} Kennzahlen aufteilen: "


def setpreferences():

    showpreferences()
    print("Es müssen 100% auf die 10 verschiedenen Kennzahlen aufgeteilt werden:")

    total = 100.0
    new_weights = [0,0,0,0,0,0,0,0,0,0]
    i = 0

    while i < 10:
        try:
            new_weights[i] = float(input(askforpref(i, total)))
            total -= new_weights[i]
            i += 1
        except:
            print("\nGeben Sie bitte eine ZAHL ein.\n")
            
    if  sum(new_weights) == 100:

        global weight_KGV
        global weight_BruttoMarge
        global weight_EKQ
        global weight_Dividendenrendite
        global weight_Umsatz
        global weight_Aktienliquidität
        global weight_DCFV 
        global weight_KWGWV 
        global weight_PoR 
        global weight_Gewinnwachstum

        weight_KGV = new_weights[0]/100
        weight_BruttoMarge = new_weights[1]/100
        weight_EKQ = new_weights[2]/100
        weight_Dividendenrendite = new_weights[3]/100
        weight_Umsatz = new_weights[4]/100
        weight_Aktienliquidität = new_weights[5]/100
        weight_DCFV = new_weights[6]/100
        weight_KWGWV = new_weights[7]/100
        weight_PoR = new_weights[8]/100
        weight_Gewinnwachstum = new_weights[9]/100

        print("")

    else:
        print("Die Summe Ihrer Prozentangaben liegt über 100. Ihre Eingaben wurden nicht übernommen.\n")


def info(ticker):

    try:
        profile = fa.profile(ticker, api_key)[0]

        symbol = ticker
        name = profile["companyName"]
        exchangeShortName = profile["exchangeShortName"]
        sector = profile["sector"]
        fullTimeEmployees = profile["fullTimeEmployees"]
        ceo = profile["ceo"]
        address = profile["address"]
        city = profile["city"]
        state = profile["state"]
        country = profile["country"]
        ipo = profile["ipoDate"].split("-")
        ipoYear = ipo[0]
        ipoMonth = ipo[1]
        ipoDay = ipo[2]

        return f"""\nTicker\t\t\t\t{symbol}
Name\t\t\t\t{name}
Exchange\t\t\t{exchangeShortName}
Sektor\t\t\t\t{sector}
Mitarbeiter\t\t\t{fullTimeEmployees}
CEO\t\t\t\t{ceo}
Adresse\t\t\t\t{address}
Stadt\t\t\t\t{city}, {state}, {country}
Börsengang\t\t\t{ipoDay}.{ipoMonth}.{ipoYear}\n"""

    except HTTPError as err:
        if err.code == 403:
            if switchkey() == True:
                rate(ticker, mode)
            else:
                return "Alle API-Keys für FundamentalAnalysis sind aufgebraucht."

    except:
        return "Ein Fehler ist aufgetreten."



weight_KGV = 1/10
weight_BruttoMarge = 1/10
weight_EKQ = 1/10
weight_Dividendenrendite = 1/10
weight_Umsatz = 1/10
weight_Aktienliquidität = 1/10
weight_DCFV = 1/10
weight_KWGWV = 1/10
weight_PoR = 1/10
weight_Gewinnwachstum = 1/10

running = True

try:
    print("""\n\nDer Aktienbewerter bewertet eine Aktie nach personalisiert gewichtbaren Kennzahlen. Die Interpretation dieser Kennzahlen
(was gut und was schlecht ist) sieht Value-Unternehmen mit hoher Dividendenrendite als ideal an. \nDer höchste Score liegt bei 800.
Tippen Sie 'hilfe', um eine Übersicht aller Befehle zu erhalten.\n""")

    while running == True:

        input_main = input("<§> ")

        if input_main.isspace() == False and input_main != "":

            input_main = input_main.split()
            input_main = [content.upper() if index != 0 else content for index, content in enumerate(input_main)]

            if input_main[0] == "set" and len(input_main) == 1:
                setpreferences()

            elif input_main[0] == "show" and len(input_main) == 1:
                showpreferences()

            elif input_main[0] == "rate":
                if len(input_main) == 2:
                    print(rate(input_main[1], "rate"))
		
                elif len(input_main) == 1:
                    print('Geben Sie ein Ticker Symbol hinter "rate" ein.')

                else:
                    print(compare(input_main[1:]))

            elif input_main[0] == "info":
                if len(input_main) == 2:
                    print(info(input_main[1]))
                else:
                    print('Geben Sie EIN Ticker Symbol hinter "info" ein.')

            elif input_main[0] == "hilfe":
                helppage()

            elif input_main[0] == "ende":
                running = False
		print("BEENDET")
		
            else:
                print('Unbekannter Befehl. Geben Sie "hilfe" ein, um die Anleitung angezeigt zu bekommen.' )

except KeyboardInterrupt:
        print("\nBEENDET")
