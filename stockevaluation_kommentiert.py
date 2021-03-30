#Mehr Informationen auf https://github.com/TomIrmler/stockevaluation
#Gruppenarbeit von Le, Caspar und Tom (11A)

#Libraries für Börsendaten und Währungskurse werden importiert:
import FundamentalAnalysis as fa 
import coinoxr as oxr 

api_key = "" #apikey für FundamentalAnalysis einfügen
oxr.app_id = "" #abikey für OpenExchangeRates eingeben

#Währungskurse werden heruntergeladen:
exchange_rates = oxr.Latest().get() 

#Funktion, um eine Menge einer bestimmten Währung in Euro umzurechnen
def Euro(Wert, Währung):

    global exchange_rates
    USDtoEUR = exchange_rates.body["rates"]["EUR"]
    USDtoWährung = exchange_rates.body["rates"][Währung]
    WertinEUR = Wert / USDtoWährung * USDtoEUR
    
    return WertinEUR

#Hauptfunktion für den rating-Prozess:
def rate(ticker):

    try:
        global exchange_rates

        #Verschiedene Datensätze zu einer Aktie (Ticker) werden heruntergeladen, ausgewählt und in Variablen gespeichert:
        quote = fa.quote(ticker, api_key)[0] 
        incomeall = fa.income_statement(ticker, api_key, period="annual")
        incomevor0 = incomeall.iloc[:,0] 
        incomevor1 = incomeall.iloc[:,1]
        incomevor3 = incomeall.iloc[:,3]
        balance = fa.balance_sheet_statement(ticker, api_key, period="annual").iloc[:,0]
        cashflow = fa.cash_flow_statement(ticker, api_key, period="annual").iloc[:,0]
        DCF = fa.discounted_cash_flow(ticker, api_key).iloc[:,0]

        #Die Währung für die Datensätze wird ausgelesen:
        statement_currency = incomevor0["reportedCurrency"]
        #Die wärung für quote und DCF ist immer USD:
        quote_currency = "USD" 

        #Falls die ausgelesene Währung nicht in der Liste mit den Währungskursen ist -> Fehler:
        if statement_currency not in exchange_rates.body["rates"]:
            return "Error: Die Zahlen der angegebenen Aktie sind in einer unbekannten Währung angegeben."

        #Aus den verschiedenen Datensätzen werden relevante Zahlen extrahiert und gegebenenfalls in Euro umgerechnet:
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

        #Die Scoring Unterfunktionen werden mit deren benötigten Zahlen aufgerufen und deren Rückgabe mit ihrer Gewichtung verrechnet:
        MargeScore=rateMarge(ebitdaratio)*weight_BruttoMarge*100
        LiquidityScore=rateLiquidity(volume, price)*weight_Aktienliquidität*100
        DividendyieldScore=rateDividenyield(dividendsPaid, sharesOutstanding, price)*weight_Dividendenrendite*100
        UmsatzScore=rateUmsatz(revenue)*weight_Umsatz*100
        EKQScore=rateEKQ(totalAssets,totalLiabilities)*weight_EKQ*100
        KGVScore=rateKGV(price,eps)*weight_KGV*100
        DCFScore=rateDCFV(stockprice,dcf)*weight_DCFV*100
        GewinnwachstumScore=rateGewinnwachstum(ebitda, ebitdavor3)*weight_Gewinnwachstum*100
        KWGWVScore=rateKWGWV(price, pricevor1, ebitda, ebitdavor1)*weight_KWGWV*100
        PayoutRatioScore=ratePayoutRatio(dividendsPaid, sharesOutstanding, eps)*weight_PoR*100

        #Aus den Teil-Scores wird der Gesamtscore errechnet:
        Gesamtscore=round(KGVScore+MargeScore+EKQScore+DividendyieldScore+UmsatzScore+LiquidityScore+DCFScore+GewinnwachstumScore+KWGWVScore+PayoutRatioScore,2)

        #Scores werden für die Ausgabe gerundet:
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

        #Anhand der Gewichtung wird für die Ausgabe ein Maxilmalwert errechnet:
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

        #Die absoluten Zahlen werden für die Ausgabe gerundet:
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

        #In den Ausgabestring werden alle Variablen eingebettet und er dann returned:
        return f"""\nDer Gesamtscore für {ticker} beträgt {Gesamtscore} von 800 Punkten.\nDieser Score setzt sich wie folgt zusammen:\n
Ebitda-Marge ({nomMarge}%)\t\t\t{ScoreMargeRound} / {maxMarge}
Aktienliquidität ({nomLiquidity} mio.)\t\t{ScoreLiquidityRound} / {maxLiquidity}
Dividendenrendite ({nomdividendyield}%)\t\t{ScoreDividendyieldRound} / {maxDividendyield}
Umsatzgröße ({nomUmsatz} mio.)\t\t{ScoreUmsatzRound} / {maxUmsatz}
Eigenkapitalquote ({nomEKQ}%)\t\t{ScoreEKQRound} / {maxEKQ}
KGV ({nomKGV})\t\t\t\t{ScoreKGVRound} / {maxKGV}
Kurs-DCF-Verhältnis ({nomDCF})\t\t{ScoreDCFRound} / {maxDCF}
Ø-Ebitda Wachstum p.a. ({nomGewinnwachstum}%)\t\t{ScoreGewinnwachstumRound} / {maxGewinnwachstum}
Kurswachstum zu Gewinnwachstum ({nomKWGWV})\t{ScoreKWGWVRound} / {maxKWGWV}
Payout-Ratio ({nomPayoutRatio}%)\t\t\t{ScorePayoutRatioRound} / {maxPayoutRatio}\n"""
        
    #Falls in der Scoringfunktion ein Fehler auftritt, wird das angezeigt:
    except:
        return "Ein Fehler ist aufgetreten."


#Hier folgen jetzt die Funktionen die eine Kennzahl einstufen und diesen einen Score zwischen 1 und 8 zurückgeben:
#Alle sind sehr ähnlich aufgebaut, Schwellwerte und Einstufungsbereiche sind von der Kennzahl abhängig

#Beispiel:
def rateKGV(price, eps):  

    #KGV wird aus Preis und Earnings per Share berechnet
    KGV=price/eps
    schwellenwerte=[300, 70, 40, 25, 15, 10, 0]

    #Sonderfall: wenn KGV <= 0, besonders schlecht -> score von 1
    if KGV<=0:
        return 1

    #Sonst ein loop der von schlecht bis gut durch die Schwellwertliste geht und für jeden "bestandenen" Schwellwert den Score erhöht
    #wäre auch durch mehrere ifs gegangen, mit einer Schleife ist es nur kürzer
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


def ratePayoutRatio(dividendspaid,shares,eps): 
    dividenden=dividendspaid*(-1)
    dps=dividenden/shares
    PoR=dps/eps
    schwellenwerte=[0.05,0.15,0.25,0.4,0.6,0.8]
    
    if dividendspaid==0:
        print("\nDa keine Dividende gezahlt wurde, wurde eine mittlere Einstufung des Payout-Ratio vorgenommen. Ändern Sie am besten die Gewichtung auf 0.")
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


#Hier werden die aktuell eingestellten Gewichtungen in Strings eingebettet, in Prozent umgerechnet und ausgegeben:
def showpreferences():  

    print("\nDas ist die aktuelle Gewichtung der Kennzahlen in ihrem Score:\n")
    print("KGV\t\t\t\t{0}%".format(weight_KGV*100))
    print("Ebitda-Marge\t\t\t{0}%".format(weight_BruttoMarge*100))
    print("Eigenkapitalquote\t\t{0}%".format(weight_EKQ*100))
    print("Dividendenrendite\t\t{0}%".format(weight_Dividendenrendite*100))
    print("Umsatz\t\t\t\t{0}%".format(weight_Umsatz*100))
    print("Aktienliquidität\t\t{0}%".format(weight_Aktienliquidität*100))
    print("Kurs-zu-DCF-Verhältnis\t\t{0}%".format(weight_DCFV*100))
    print("Gewinnwachstum\t\t\t{0}%".format(weight_Gewinnwachstum*100))
    print("Kurswachstum zu Gewinnwachstum\t{0}%".format(weight_Gewinnwachstum*100))
    print("Payout-Ratio\t\t\t{0}%\n".format(weight_PoR*100))


#Das ist einfach nur unsere Hilfe-Ausgabe
def helppage():

    print("""\nDas ist die Anleitung zu unserem Programm:\n\nset\t\t\t\t\t- Kennzahlen gewichten\nshow\t\t\t\t\t- aktuelle Gewichtung anzeigen
rate + <Ticker Symbol>\t\t\t- Rating durchführen\ninfo + <Ticker Symbol>\t\t\t- Informationen anzeigen\nende\t\t\t\t\t- Programm beenden\n""")


#Hilfsfunktion für setpreferences()
def askforpref(k_index, total):

    #Je nach Kennzahlnummer wird eine anderer Fragesatz zurückgegeben
    #Außerdem werden die übrigen zu gewichtenden Zahlen errechnet und die noch zu vergebende Menge wird eingebettet
    k_strings = ["der KGV", "die Ebitda-Marge", "die Eigenkapitalquote", "die Dividendenrendite", "der Umsatz", "die Aktienliquidität", "das Kurs-zu-DCF-Verhältnis", "das Verhältnis von Kurswachstum zu Gewinnwachstum", "das Payout-Ratio", "das Gewinnwachstum" ]
    k_string = k_strings[k_index]
    übrige = 10-k_index
    return f"\nWie viel Prozent des Scores soll {k_string} ausmachen?\nSie können noch {total}% auf {übrige} Kennzahlen aufteilen: "


#Diese Funktion lässt den Nutzer neue Gewichtungen einstellen
def setpreferences():

    #Zuerst werden die aktuellen Gewichtungen und eine Anleitung ausgegeben
    showpreferences()
    print("Es müssen 100% auf die 10 verschiedenen Kennzahlen aufgeteilt werden:")

    #definition einiger Variablen
    total = 100.0
    new_weights = [0,0,0,0,0,0,0,0,0,0]
    i = 0

    #Es gibt 10 zu ändernde Gewichtungen
    while i < 10:
        try:
            #An der Stelle i wird in der Liste der neuen Gewihtungen das also float Zahl gespeichert,
            #was der Nutzer auf die Frage, die askforpref() ihm stellt antwortet
            #askforpref() baut anhand der Nummer der Kennzahl bzw. i und der zu Vergebenden Menge eine angepasste Aufforderung zusammen
            new_weights[i] = float(input(askforpref(i, total)))

            #Dieser Wert wird von der zu vergebenden Menge abgezogen
            total -= new_weights[i]

            #Wenn das geklappt hat gehe zur nächsten Gewichtung
            i += 1

        except:
            #Falls der Nutzer keine Zahl eingibt, kommt es zum Fehler in dem "try"-Bereich
            #Dann wird diese Fehlermeldung ausgegeben und die gleiche Gewichtung wird nochmal abgefragt
            print("\nGeben Sie bitte eine ZAHL ein.\n")
            
    #Wenn die Summe der neuen Gewichtungen 100 bzw. 100% entspricht werden die globalen Gewichtung verändert
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

        #Die neuen Gewichtungen sind in Prozent angaben angegeben, die globalen Gewichtungen sind in Dezimalzahlen: 20%/100 -> 0.2
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


#Funktion, um Informationen zu einer Aktie auszugeben
def info(ticker):

    try:
        #Herunterladen eines Datensatzes in dem relevante Infos stehen:
        #Das [0] wählt aus einem pandas.Dataframe mit einer Spalte die eine Spalte nochmal aus und macht somit eine pandas.Series Liste daraus
        #Das hat den Vorteil, dass man unten dann direkt mit dem label in [] einen Wert wählen kann
        profile = fa.profile(ticker, api_key)[0]

        #Daten werden aus der Liste geholt
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
        #Das Börseneintrittsdatum ist im Format "2021-3-30" angegeben. Wir wollen "30.3.2021".
        #Dazu wird der Datumsstring an den Bindestrichen gedreiteilt und aus der entstandenen Liste werden danach das Jahr, der Monat und der Tag geholt
        ipo = profile["ipoDate"].split("-")
        ipoYear = ipo[0]
        ipoMonth = ipo[1]
        ipoDay = ipo[2]

        #Hier werden alle Variablen in den Ausgabestring eingebettet
        return f"""\nTicker\t\t\t\t{symbol}
Name\t\t\t\t{name}
Exchange\t\t\t{exchangeShortName}
Sektor\t\t\t\t{sector}
Mitarbeiter\t\t\t{fullTimeEmployees}
CEO\t\t\t\t{ceo}
Adresse\t\t\t\t{address}
Stadt\t\t\t\t{city}, {state}, {country}
Börsengang\t\t\t{ipoDay}.{ipoMonth}.{ipoYear}\n"""

    except:
        return "Ein Fehler ist aufgetreten."


#Bis hier waren Funktionen, ab hier fängt der eigentliche Programmablauf an


#Standard Gewichtungenn werden definiert
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

#über das auf "False" Stellen der variable running kann die Endlosschleife des Programms gestoppt werden
running = True

try:
    #Anleitung:
    print("""\n\nDer Aktienbewerter bewertet eine Aktie nach personalisiert gewichtbaren Kennzahlen. Die Interpretation dieser Kennzahlen
(was gut und was schlecht ist) sieht große, nicht zu hoch bewertete Unternehmen mit hoher Dividendenrendite als ideal an. \nDer höchste Score liegt bei 800.
Tippen Sie 'hilfe', um eine Übersicht aller Befehle zu erhalten.\n""")

    #Hauptschleife
    while running == True:
        
        #Prompt bzw. Eingabemöglichkeit für den Nutzer
        input_main = input("<§> ")

        #Eingaben werden nicht beachtet, sind sie nur Leerzeichen oder nichts (der Nutzer hat nur Enter gedrückt)
        if input_main.isspace() == False and input_main != "":

            #Der eingabestring wird in seine Wörter geteilt -> Befehle mir mehreren Komponenten werden möglich
            input_main = input_main.split()

            #Falls der Nutzer NUR "set" eingibt -> setpreferences()
            if input_main[0] == "set" and len(input_main) == 1:
                setpreferences()

            #Falls der Nutzer NUR "show" eingibt -> showpreferences()
            elif input_main[0] == "show" and len(input_main) == 1:
                showpreferences()

            #Falls der Nutzer "rate" eingibt und danach EIN weiteres Wort, wende auf dieses weitere Wort die "rate"-Funktion an
            elif input_main[0] == "rate":
                if len(input_main) == 2:
                    print(rate(input_main[1]))
                else:
                    print('Geben Sie EIN Ticker Symbol hinter "rate" ein.')

            #Falls der Nutzer "info" eingibt und danach EIN weiteres Wort, wende auf dieses weitere Wort die "info"-Funktion an
            elif input_main[0] == "info":
                if len(input_main) == 2:
                    print(info(input_main[1]))
                else:
                    print('Geben Sie EIN Ticker Symbol hinter "info" ein.')

            #Hilfefunktion
            elif input_main[0] == "hilfe":
                helppage()

            #Wenn der Nutzer "ende" eingibt, setze running auf False -> while Schleife endet und Programm endet
            elif input_main[0] == "ende":
                running = False

            #Wenn keine der Bedingungen erfüllt ist -> "unbekannter Befehl"
            else:
                print('Unbekannter Befehl. Geben Sie "hilfe" ein, um die Anleitung angezeigt zu bekommen.' )

#Falls der Nuter das Programm über <STRG> + <C> beendet, wird "BEENDET" ausgegeben
except KeyboardInterrupt:
        print("\nBEENDET")