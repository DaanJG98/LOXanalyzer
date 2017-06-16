# LOXanalyzer

LOXanalyzer is een webapplicatie die gebruik maakt van het Flask-framework om HTML te genereren.
Daarnaast maakt de applicatie connectie met een lokale database om de resultaten van zoekquery's te tonen in de browser.

Het project bestaat uit verschillende onderdelen;
- WebApp.py
- Textmining.py
- statics en templates
- lokale database

Door middel van Textmining.py wordt informatie van PubMed afgehaald, deze informatie wordt opgeslagen in een lokale database.
Textmining.py bestaat grofweg uit twee onderdelen, het zoeken van publicaties bij de verschillende soorten LOXs en het zoeken naar co-occurrence tussen LOXs en keywords.
WebApp.py is de basis van de webapplicatie, van hieruit worden verschillende html pagina's aangeroepen. Ook wordt vanuit dit script connectie gemaakt met de lokale database.

<-- statics bevat een .css file maar deze wordt niet gebruikt, om onbekende reden werkt de css niet of niet volledig. Hierdoor is er voor gekozen om de styles in de html pagina's te verwerken.-->

'De applicatie is eerst in een ander git-project gemaakt, maar door merge fouten is er overgeschakeld naar een ander project'
"https://github.com/DaanJG98/Owe8_projectInf"
