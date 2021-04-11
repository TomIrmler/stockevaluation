<h1>stockevaluation</h1>

<h3>Vorraussetzungen</h3>
Für das Benutzen der stockevalation_fa.py müssen Sie über den pip-Installer die Librarie FundamentalAnalysis (*pip install FundamentalAnalysis*) installieren. Für alle anderen Dateien brauchen sie keine weiteren Libraries zu installieren.

<h3>Grundlegendes</h3>
Der Aktienbewerter bewertet Aktien anhand von 10 Kennzahlen. Es wird ein Gesamtscore aus den erreichten Scores der verschiedenen Kennzahlen errechnet, wobei der höchste erreichbare Score bei 800 liegt. Die 10 verschiedenen Kennzahlen lassen sich je nach individuellen Präferenzen gewichten. Auf die Anpassbarkeit der Interpretation der Kennzahlen, also welcher Wert bei welcher Kennzahl welchen Score erreicht, wurde verzichtet, da der nötige Aufwand nicht mit dem Ziel eines schnellen Überblicks über die Qualität verschiedener Aktien vereinbar ist. Die festgelegte Interpretation der Kennzahlen sieht fundamental kerngesunde,wachsende und große sowie günstig bis moderat bewertete Unternehmen, mit hoher Dividendenrendite bei geringem Payout-Ratio als Ideal an (Value-Investing). Die genauen Intervalle der Interpretation kann der beiliegenden CSV-Tabelle entnommen werden. Es ist zu beachten, dass momentan leider nur Aktien bewertet werden können, die am NewYorkStockExchange notieren.
Neben dem Score können grundlegende Informationen zu Unternehmen angezeigt werden. 

<b>Es ist zu beachten, dass das Ziel des Aktienbewerters, wie angedeutet, ist, eine Einschätzung zu treffen, ob es sich lohnt, eine tiefere Analyse anzugehen. Der errechnete Score sollte also nicht als volle Fundamentalanalyse angesehen werden, ist somit also auch keiner Anlageberatung, insbesondere keiner persönlichen Anlageberatung, gleichzusetzen.</b>

Eine Anleitung des Programms ist im Programm selbst zu finden.
<p>

<h3>Kurze Erklärung der verwendeten Kennzahlen:</h3><p>

<h4>KGV:</h4>
Kurs-Gewinn-Verhältnis, setzt den Kurs eines Unternehmens in Verhältnis zum Gewinn pro Aktie des vergangenen Geschäftsjahres.<br>

<h4>EBITDA-Marge:</h4> 
Verhältnis von EBITDA zum Umsatz. EBITDA sind die Gewinne vor Steuern, Zinsen und Abschreibungen.<br>

<h4>Handelsvolumen:</h4> 
Der Kurs einer Aktie multipliziert mit der am letzten Tag gehandelten Stückzahl dieser Aktien. Es gibt Auskunft über die Liquidität der jeweiligen Aktie.<br>

<h4>Dividendenrendite:</h4>
Gibt Auskunft über die jährlich ausgeschüttete Dividende im Verhältnis zum Aktienkurs.<br>

<h4>Umsatz:</h4>
Alle Einnahmen eines Unternehmens aus Verkäufen. Wird hier als Anhaltspunkt für die Größe eines Unternehmens benutzt.<br>

<h4>Eigenkapitalquote:</h4>
Setzt das Eigenkapital eines Unternehmens in Verhältnis zum Gesamtkapital. Es lässt sich eine Aussage zur finanziellen Lage des Unternehmens treffen. Vor allem bei Banken und Versicherungen ist die Eigenkapitalquote sehr niedrig, was allerdings per se nicht schlecht ist. Insbesondere die Eigenkapitalquote ist teilweise Branchenabhängig.<br>

<h4>Kurs-zu-discounted-Cashflow-Verhältnis:</h4>
DCF ist der während der gesamten Lebensdauer des Unternehmens zu erwartende erwirtschaftete Cashflow (inflationsbereinigt). Auf eine Aktie runtergerechnet und im Verhältnis mit dem jeweiligen Kurs ergibt sich eine Einstufung der Bewertung (overvalued, fair, undervalued) des Unternehmens.<br>

<h4>EBITDA-Wachstum (Gewinnwachstum):</h4>
Gibt hier die durchschnittliche Wachstumsrate der EBITDA pro Jahr der letzten drei Jahre an.<br>

<h4>Kurswachstum-zu-EBITDA-Wachstum-Verhältnis:</h4>
Setzt Kurswachstum und EBITDA-Wachstum ins Verhältnis. Es lässt sich ableiten, wie die Aktie im Vergleich zu den EBITDA des Unternehmens bewertet ist. Grundlage ist das Wachstum beider Kennzahlen über das vergangene Geschäftsjahr.<br>

<h4>Payout-Ratio:</h4>
Setzt gezahlte Dividende und Gewinne (nach Steuer; "Gewinn pro Aktie") des Unternehmens ins Verhältnis. Es lässt sich ableiten, wieviel Prozent des Gewinns das Unternehemen auszahlt und wieviel Kapital für eventuelle Rücklagen oder Investitionen verbleiben.<br>

<h4>Rating: undervalued, likely undervalued</h4>
Diese Einstufung stellt das Anlagevermögen eines Unternehmens (abzüglich der Schulden) seiner Marktkapitalisierung. Ist das Anlagevermögen abzüglich der Schulden höher als die Marktkapitalisierung, so wird dieses Unternehmen als "undervalued" eingestuft, weil es offensichtlich eine fundamentale Bewertungslücke gibt. Ist die Marktkapitalisierung zwar höher als das Anlagevermögen abzüglich der Schulden, überschreiet die Lücke aber nicht 10% der Marktkapitalisierung, so wird das Unternehmen als "likely undervalued" eingestuft. 
Es ist zu beachten, dass diese Einstufung auf simplen fundamentalen Kennzahlen beruht und noch keine zukünftigen Ereignisse eingepriesen sind. Das Rating macht lediglich auf eine Bewertungslücke (gemessen am Anlagevermögen) aufmerksam (undervalued) oder auf eine geringe Lücke zu dem Preis, bei dem die Bewertung durch das Anlagevermögen gedeckt ist (likely undervalued). Außerdem ist zu beachten, dass diese Art der Bewertung keinen Umkehrschluss auf Unternehmen mit gegenteiligen Tendenzen erlaubt, da die Deckung der Bewertung durch Anlagevermögen sektorabhängig ist.












