# LOXanalyzer

LOXanalyzer is een webapplicatie die gebruik maakt van het flask framework om html te genereren.
Het project bestaat uit verschillende onderdelen;
- WebApp.py
- Textmining.py
- statics en templates
- lokale database

Door middel van Textmining.py wordt informatie van PubMed afgehaald, deze informatie wordt opgeslagen in een lokale database.
Textmining.py bestaat grofweg uit twee onderdelen, het zoeken van publicaties bij de verschillende soorten LOXs en het zoeken naar co-occurrence
tussen LOXs en keywords.
WebApp.py is de basis van de webapplicatie, van hieruit worden verschillende html pagina's aangeroepen. Ook wordt vanuit dit script connectie gemaakt
met de lokale database.

<-- statics bevat een .css file maar deze wordt niet gebruikt, om onbekende reden werkt de css niet of niet volledig. Hierdoor is er voor gekozen om de styles in de html pagina's te verwerken.-->

