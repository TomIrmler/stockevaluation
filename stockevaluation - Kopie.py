import FundamentalAnalysis as fa

api_key = 'APIKEY'

def rate(ticker):

    try:
        quote = fa.quote(ticker, api_key)
        income = fa.income_statement(ticker, api_key, period="annual")
        balance = fa.balance_sheet_statement(ticker, api_key, period="annual")
        cashflow = fa.cash_flow_statement(ticker, api_key, period="annual")


        if type(quote[0]["pe"]) == float or type(quote[0]["pe"]) == int:
            KGV = quote[0]["pe"]
            KGVScore=rateKGV(KGV)*weight_KGV*100

        else:
            return "Error: Die angegebene Aktie hat kein KGV. Versuchen Sie eine andere Aktie, wie z.B. AAPL oder AMZN."

        grossProfit = income["2020"]["grossProfit"]
        revenue = income["2020"]["revenue"]
        volume = quote[0]["volume"]
        price = quote[0]["price"]
        dividendsPaid = cashflow["2020"]["dividendsPaid"]
        sharesOutstanding = quote[0]["sharesOutstanding"]
        totalAssets = balance["2020"]["totalAssets"]
        totalLiabilities = balance["2020"]["totalLiabilities"]


        MargeScore=rateMarge(grossProfit, revenue)*weight_BruttoMarge*100
        LiquidityScore=rateLiquidity(volume, price)*weight_Aktienliquidität*100
        DividendyieldScore=rateDividenyield(dividendsPaid, sharesOutstanding, price)*weight_Dividendenrendite*100
        UmsatzScore=rateUmsatz(revenue)*weight_Umsatz*100
        EKQScore=rateEKQ(totalAssets,totalLiabilities)*weight_EKQ*100

        Gesamtscore=round(KGVScore+MargeScore+EKQScore+DividendyieldScore+UmsatzScore+LiquidityScore,2)

        M=round(MargeScore,2)
        L=round(LiquidityScore,2)
        D=round(DividendyieldScore,2)
        U=round(UmsatzScore,2)
        E=round(EKQScore,2)
        K=round(KGVScore,2)
        wb=round(weight_BruttoMarge*800,2)
        wl=round(weight_Aktienliquidität*800,2)
        wd=round(weight_Dividendenrendite*800,2)
        we=round(weight_EKQ*800,2)
        wk=round(weight_KGV*800,2)
        wu=round(weight_Umsatz*800,2)
        Marge=round(grossProfit/revenue*100,3)
        dividendyield=round((dividendsPaid*(-1)/sharesOutstanding)/price*100,3)
        EKQ=round(((totalAssets-totalLiabilities)/totalAssets)*100,3)
        K=round(KGV,2)
        Liquidität=round(volume*price/1000000,2)
        Umsatz=round(revenue/1000000,2)

    


        
        print(f"""Der Gesamtscore für {ticker} beträgt {Gesamtscore} von 800 Punkten.\nDieser Score setzt sich wie folgt zusammen:\n
Bruttomarge ({Marge}%)\t\t\t{M} / {wb}
Aktienliquidität ({Liquidität} mio)\t\t{L} / {wl}
Dividendenrendite ({dividendyield}%)\t\t{D} / {wd}
Umsatzgröße ({Umsatz} mio)\t\t{U} / {wu}
Eigenkapitalquote ({EKQ}%)\t\t{E} / {we}
KGV ({K})\t\t\t\t{K} / {wk}""")
        

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
    schwellenwerte=[0.01,0.03,0.05,0.07,0.1,0.15,0.2]
    
    if Marge<0.01:
        return 1
        
    elif Marge>=0.2:
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
    print("""\nDas ist die Anleitung zu unserem Programm:\n\nsetprefernces\t\t-\t\tKennzahlen gewichten\nshowpreferences\t\t-\t\taktuelle Gewichtung anzeigen
rate + <Ticker Symbol>\t-\t\tRating durchführen\nSTRG + C\t\t-\t\tProgramm beenden\n""")

def setpreferences():
    showpreferences()
    print("Sie können 100% auf die 6 verschiedenen Kennzahlen aufteilen:")

    new_weight_KGV = float(input("Wie viel Prozent des Scores soll das KGV ausmachen?"))
    new_weight_BruttoMarge = float(input("Wie viel Prozent des Scores soll die Brutto-Marge ausmachen?"))
    new_weight_EKQ = float(input("Wie viel Prozent des Scores soll die Eigenkapitalquote ausmachen?"))
    new_weight_Dividendenrendite = float(input("Wie viel Prozent des Scores soll die Dividendenrendite ausmachen?"))
    new_weight_Umsatz = float(input("Wie viel Prozent des Scores soll der Umsatz ausmachen?"))
    new_weight_Aktienliquidität = float(input("Wie viel Prozent des Scores soll die Aktienliquidität ausmachen?"))

    if new_weight_KGV+new_weight_BruttoMarge+new_weight_EKQ+new_weight_Dividendenrendite+new_weight_Umsatz+new_weight_Aktienliquidität == 100.0:
        global weight_KGV
        global weight_BruttoMarge
        global weight_EKQ
        global weight_Dividendenrendite
        global weight_Umsatz
        global weight_Aktienliquidität

        weight_KGV = new_weight_KGV/100
        weight_BruttoMarge = new_weight_BruttoMarge/100
        weight_EKQ = new_weight_EKQ/100
        weight_Dividendenrendite = new_weight_Dividendenrendite/100
        weight_Umsatz = new_weight_Umsatz/100
        weight_Aktienliquidität = new_weight_Aktienliquidität/100

    else:
        print("Die Summe ihrer Prozentangaben liegt über 100. Ihre Eingaben wurden nicht übernommen.")


weight_KGV = 1/6
weight_BruttoMarge = 1/6
weight_EKQ = 1/6
weight_Dividendenrendite = 1/6
weight_Umsatz = 1/6
weight_Aktienliquidität = 1/6




try:

    print("""\n\nDer Aktienbewerter bewertet eine Aktie nach personalisiert gewichtbaren Kennzahlen. Die Interpretation dieser Kennzahlen
(was gut und was schlecht ist) sieht große, nicht zu hoch bewertete Unternehmen mit hoher Dividendenrendite als ideal an. \nDer höchste Score liegt bei 800.
Tippen Sie 'hilfe', um eine Übersicht aller Befehle zu erhalten.\n""")

    while True:

        input_main = input("<§> ")

        if input_main.isspace() == False and input_main != "":

            input_main = input_main.split()

            if input_main[0] == "setpreferences" and len(input_main) == 1:
                setpreferences()

            elif input_main[0] == "showpreferences" and len(input_main) == 1:
                showpreferences()

            elif input_main[0] == "rate":
                if len(input_main) == 2:
                    rate(input_main[1])
                else:
                    print('Geben Sie EIN Ticker Symbol hinter "rate" ein.')

            elif input_main[0] == "hilfe":
                helppage()

            else:
                print('Unbekannter Befehl. Geben Sie "hilfe" ein, um die Anleitung angezeigt zu bekommen.' )


except KeyboardInterrupt:
        print("\nBEENDET")
