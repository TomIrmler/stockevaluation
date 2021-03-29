# stockevaluation

Für das Benutzen des Programms müssen Sie über den pip-Installer die Libraries FundamentalAnalysis (*pip install FundamentalAnalysis*) und coinoxr (*pip install coinoxr*) installieren.

Der Aktienbewerter bewertet Aktien anhand von 10 Kennzahlen. Es wird ein Gesamtscore aus den erreichten Scores der verschiedenen Kennzahlen errechnet, wobei der höchste erreichbare Score bei 800 liegt. Die 10 verschiedenen Kennzahlen lassen sich je nach individuellen Präferenzen gewichten. Auf die Anpassbarkeit der Interpretation der Kennzahlen, also welcher Wert bei welcher Kennzahl welchen Score erreicht, wurde verzichtet, da der nötige Aufwand nicht mit dem Ziel eines schnellen Überblicks über die Qualität verschiedener Aktien vereinbar ist. Die festgelegte Interpretation der Kennzahlen sieht fundamental kerngesunde,wachsende und große sowie günstig bis moderat bewertete Unternehmen, mit hoher Dividendenrendite bei geringem Payout-Ratio als Ideal an (Value-Investing). Die genauen Intervalle der Interpretation kann der beiliegenden CSV-Tabelle entnommen werden. Es ist zu beachten, dass momentan leider nur Aktien bewertet werden können, die am NewYorkStockExchange notieren.
Neben dem Score können grundlegende Informationen zu Unternehmen angezeigt werden. 

Es ist zu beachten, dass das Ziel des Aktienbewerters, wie angedeutet, ist, eine Einschätzung zu treffen, ob es sich lohnt, eine tiefere Analyse anzugehen. Der errechnete Score sollte also nicht als volle Fundamentalanalyse angesehen werden, ist somit also auch keiner Anlageberatung, insbesondere keiner persönlichen Anlageberatung, gleichzusetzen.

Eine Anleitung des Programms ist im Programm selbst zu finden.



**kurze Erklärung der verwendeten Kennzahlen:**

<h1>KGV:</h1> <br>
Kurs-Gewinn-Verhältnis, setzt den Kurs eines Unternehmens in Verhältnis zum Gewinn pro Aktie des vergangenen Geschäftsjahres.

EBITDA-Marge:
Verhältnis von EBITDA zum Umsatz. EBITDA sind die Gewinne vor Steuern, Zinsen und Abschreibungen. 

Handelsvolumen:
Der Kurs einer Aktie multipliziert mit der am letzten Tag gehandelten Stückzahl dieser Aktien. Es gibt Auskunft über die Liquidität der jeweiligen Aktie.

Dividendenrendite:
Gibt Auskunft über die jährlich ausgeschüttete Dividende im Verhältnis zum Aktienkurs.

Umsatz:
Alle Einnahmen eines Unternehmens aus Verkäufen. Wird hier als Anhaltspunkt für die Größe eines Unternehmens benutzt.

Eigenkapitalquote:
Setzt das Eigenkapital eines Unternehmens in Verhältnis zum Gesamtkapital. Es lässt sich eine Aussage zur finanziellen Lage des Unternehmens treffen. Vor allem bei Banken und Versicherungen ist die Eigenkapitalquote sehr niedrig, was allerdings per se nicht schlecht ist. Insbesondere die Eigenkapitalquote ist teilweise Branchenabhängig.

Kurs-zu-discounted-Cashflow-Verhältnis:
DCF ist der während der gesamten Lebensdauer des Unternehmens zu erwartende erwirtschaftete Cashflow (inflationsbereinigt). Auf eine Aktie runtergerechnet und im Verhältnis mit dem jeweiligen Kurs ergibt sich eine Einstufung der Bewertung (overvalued, fair, undervalued) des Unternehmens.

EBITDA-Wachstum (Gewinnwachstum):
Gibt hier die durchschnittliche Wachstumsrate der EBITDA pro Jahr der letzten drei Jahre an.

Kurswachstum-zu-EBITDA-Wachstum-Verhältnis:
Setzt Kurswachstum und EBITDA-Wachstum ins Verhältnis. Es lässt sich ableiten, wie die Aktie im Vergleich zu den EBITDA des Unternehmens bewertet ist. Grundlage ist das Wachstum beider Kennzahlen über das vergangene Geschäftsjahr

Payout-Ratio:
Setzt gezahlte Dividende und Gewinne (nach Steuer; "Gewinn pro Aktie") des Unternehmens ins Verhältnis. Es lässt sich ableiten, wieviel Prozent des Gewinns das Unternehemen auszahlt und wieviel Kapital für eventuelle Rücklagen oder Investitionen verbleiben.












