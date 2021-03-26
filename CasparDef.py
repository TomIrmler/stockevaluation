def rateGewinnwachstum(gewinn, gewinnvor3):  
    GewinnWachstum=((gewinn-gewinnvor3)/gewinnvor3)/3
    schwellenwerte=[0,0.05,0.1,0.15,0.25,0.4,0.55,]
    
    if GewinnWachstum<=0:
        return 1

    elif GewinnWachstum>0.55:
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

def ratePayoutRatio(dividendspaid,shares,eps):                   #abfrage, dass falls dividenspaid=0 ist, ratePayoutRation geskippt wird

    dps=dividendspaid/shares
    PoR=dps/eps
    schwellenwerte=[0.05,0.15,0.25,0.4,0.6,0.8]

    if Por>=0.8:
        return 1
        
    elif PoR<=0.05:
        return 8
        
    else:
        score=8
        i=0
        
        while Por>schwellenwerte[i]:
            score-=1
            i+=1
    return(score)                             
