import FundamentalAnalysis as fa
import coinoxr as oxr

api_key = '2355734d1486c0599f415923d59c1387'

oxr.app_id = "8da07fea22fb4d6d98f657bdcbcad0d5" #man hat 1000 Anfragen im Monat, sprich man kann das Programm 1000 Mal starten, dann halt anderes Konto.
exchange_rates = oxr.Latest().get()

def Euro(Wert, Währung):
    global exchange_rates
    USDtoEUR = exchange_rates.body["rates"]["EUR"]
    USDtoWährung = exchange_rates.body["rates"][Währung]
    WertinEUR = Wert / USDtoWährung * USDtoEUR
    
    return WertinEUR

def rate(ticker):

    global exchange_rates

    try:
        quote = fa.quote(ticker, api_key)[0] 
        income = fa.income_statement(ticker, api_key, period="annual").iloc[:,0] 
        balance = fa.balance_sheet_statement(ticker, api_key, period="annual").iloc[:,0]
        cashflow = fa.cash_flow_statement(ticker, api_key, period="annual").iloc[:,0]
        
        statement_currency = income["reportedCurrency"]
        quote_currency = "USD" 

        if statement_currency not in exchange_rates.body["rates"]:
            return "Error: Die Zahlen der angegebenen Aktie sind in einer unbekannten Währung angegeben."

        if type(quote["pe"]) == float or type(quote["pe"]) == int:
            KGV = quote["pe"]
            KGVScore=rateKGV(KGV)*weight_KGV*100

        else:
            return "Error: Die angegebene Aktie hat kein KGV. Versuchen Sie eine andere Aktie, wie z.B. AAPL oder AMZN."

        grossProfit = Euro(income["grossProfit"], statement_currency)         
        revenue = Euro(income["revenue"], statement_currency) 
        volume = quote["volume"]
        price = Euro(quote["price"], quote_currency)
        dividendsPaid = Euro(cashflow["dividendsPaid"], statement_currency)
        sharesOutstanding = quote["sharesOutstanding"]
        totalAssets = Euro(balance["totalAssets"], statement_currency)
        totalLiabilities = Euro(balance["totalLiabilities"], statement_currency)


        MargeScore=rateMarge(grossProfit, revenue)*weight_BruttoMarge*100
        LiquidityScore=rateLiquidity(volume, price)*weight_Aktienliquidität*100
        DividendyieldScore=rateDividenyield(dividendsPaid, sharesOutstanding, price)*weight_Dividendenrendite*100
        UmsatzScore=rateUmsatz(revenue)*weight_Umsatz*100
        EKQScore=rateEKQ(totalAssets,totalLiabilities)*weight_EKQ*100

        Gesamtscore=round(KGVScore+MargeScore+EKQScore+DividendyieldScore+UmsatzScore+LiquidityScore,2)

        ScoreMargeRound=round(MargeScore,2)
        ScoreLiquidityRound=round(LiquidityScore,2)
        ScoreDividendyieldRound=round(DividendyieldScore,2)
        ScoreUmsatzRound=round(UmsatzScore,2)
        ScoreEKQRound=round(EKQScore,2)
        ScoreKGVRound=round(KGVScore,2)
 
        maxMarge=round(weight_BruttoMarge*800,2)
        maxLiquidity=round(weight_Aktienliquidität*800,2)
        maxDividendyield=round(weight_Dividendenrendite*800,2)
        maxEKQ=round(weight_EKQ*800,2)
        maxKGV=round(weight_KGV*800,2)
        maxUmsatz=round(weight_Umsatz*800,2)

        nomMarge=round(grossProfit/revenue*100,3)
        nomdividendyield=round((dividendsPaid*(-1)/sharesOutstanding)/price*100,3)
        nomEKQ=round(((totalAssets-totalLiabilities)/totalAssets)*100,3)
        nomKGV=round(KGV,2)
        nomLiquidity=round(volume*price/1000000,2)
        nomUmsatz=round(revenue/1000000,2)


        print(f"""Der Gesamtscore für {ticker} beträgt {Gesamtscore} von 800 Punkten.\nDieser Score setzt sich wie folgt zusammen:\n
Bruttomarge ({nomMarge}%)\t\t\t{ScoreMargeRound} / {maxMarge}
Aktienliquidität ({nomLiquidity} mio)\t\t{ScoreLiquidityRound} / {maxLiquidity}
Dividendenrendite ({nomdividendyield} %)\t\t{ScoreDividendyieldRound} / {maxDividendyield}
Umsatzgröße ({nomUmsatz} mio)\t\t{ScoreUmsatzRound} / {maxUmsatz}
Eigenkapitalquote ({nomEKQ} %)\t\t{ScoreEKQRound} / {maxEKQ}
KGV ({nomKGV})\t\t\t\t{ScoreKGVRound} / {maxKGV}""")
        

    except:
        print("Ein Fehler ist aufgetreten.")


def rateKGV(KGV):
    schwellenwerte=[300, 70, 40, 25, 15, 10]

    if KGV<=0:
        return 1

    else:
        score=2
        i=0

        while KGV<schwellenwerte[i]:
            score +=1
            i+=1

    return(score)

def rateMarge(gewinn, umsatz):
    Marge=gewinn/umsatz
    schwellenwerte=[0.02,0.05,0.1,0.15,0.2,0.3,0.5]
    
    if Marge<0.02:
        return 1
        
    elif Marge>=0.5:
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



def showpreferences():
    print("\nDas ist die aktuelle Gewichtung der Kennzahlen in ihrem Score:\n")
    print("KGV\t\t\t\t{0}%".format(weight_KGV*100))
    print("Brutto-Marge\t\t\t{0}%".format(weight_BruttoMarge*100))
    print("EKQ\t\t\t\t{0}%".format(weight_EKQ*100))
    print("Dividenderendite\t\t{0}%".format(weight_Dividendenrendite*100))
    print("Umsatz\t\t\t\t{0}%".format(weight_Umsatz*100))
    print("Aktienliquidität\t\t{0}%\n".format(weight_Aktienliquidität*100))

def helppage():
    print("""\nDas ist die Anleitung zu unserem Programm:\n\nsetprefernces\t\t\t\t-Kennzahlen gewichten\nshowpreferences\t\t\t\t-aktuelle Gewichtung anzeigen
rate + <Ticker Symbol>\t\t\t-Rating durchführen\nSTRG + C\t\t\t\t-Programm beenden\n""")

def askforpref(k_index, total):
    k_strings = ["der KGV", "die Brutto-Marge", "der EKQ", "die Dividendenrendite", "der Umsatz", "die Aktienliquidität"]
    k_string = k_strings[k_index]
    übrige = 6-k_index
    return f"\nWie viel Prozent des Scores soll {k_string} ausmachen?\nSie können noch {total}% auf {übrige} Kennzahlen aufteilen: "

def setpreferences():

    showpreferences()
    print("Es müssen 100% auf die 6 verschiedenen Kennzahlen aufgeteilt werden:")

    total = 100.0
    new_weights = [0,0,0,0,0,0]
    i = 0

    while i < 6:
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

        weight_KGV = new_weights[0]/100
        weight_BruttoMarge = new_weights[1]/100
        weight_EKQ = new_weights[2]/100
        weight_Dividendenrendite = new_weights[3]/100
        weight_Umsatz = new_weights[4]/100
        weight_Aktienliquidität = new_weights[5]/100

        print("")

    else:
        print("Die Summe Ihrer Prozentangaben liegt über 100. Ihre Eingaben wurden nicht übernommen.\n")


weight_KGV = 1/6
weight_BruttoMarge = 1/6
weight_EKQ = 1/6
weight_Dividendenrendite = 1/6
weight_Umsatz = 1/6
weight_Aktienliquidität = 1/6

running = True

try:

    print("""\n\nDer Aktienbewerter bewertet eine Aktie nach personalisiert gewichtbaren Kennzahlen. Die Interpretation dieser Kennzahlen
(was gut und was schlecht ist) sieht große, nicht zu hoch bewertete Unternehmen mit hoher Dividendenrendite als ideal an. \nDer höchste Score liegt bei 800.
Tippen Sie 'hilfe', um eine Übersicht aller Befehle zu erhalten.\n""")

    while running == True:

        input_main = input("<§> ")

        if input_main.isspace() == False and input_main != "":

            input_main = input_main.split()

            if input_main[0] == "setpreferences" and len(input_main) == 1:
                setpreferences()

            elif input_main[0] == "showpreferences" and len(input_main) == 1:
                showpreferences()

            elif input_main[0] == "rate":
                if len(input_main) == 2:
                    print(rate(input_main[1]))
                else:
                    print('Geben Sie EIN Ticker Symbol hinter "rate" ein.')

            elif input_main[0] == "hilfe":
                helppage()

            elif input_main[0] == "ende":
                running = False

            else:
                print('Unbekannter Befehl. Geben Sie "hilfe" ein, um die Anleitung angezeigt zu bekommen.' )


except KeyboardInterrupt:
        print("\nBEENDET")