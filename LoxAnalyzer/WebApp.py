# Author: Daan Gilissen
# Date: 16-6-2017
# Versie: 2.0
# Status: Complete
# Known bugs: Slechte query zorgt voor een onoverzichtelijke tabel in de webpagina, hierdoor is ervoor gekozen om per kolom alleen de unieke waardes te tonen.
#             Dit om duizenden rijen van de tabel te voorkomen, deze actie wordt uitgevoerd nadat de query resultaten zijn opgehaald.

from flask import Flask, render_template, request
import cx_Oracle
import collections

app = Flask(__name__)


# basic methode, retourneert render_template met daarin het de html-pagina van de homepage.
@app.route('/')
def index():
    return render_template('homepage.html')


# Methode die aan de hand van geselecteerd soort LOX de database doorzoekt
# Methode retourneert een lijst die wordt gebruikt voor de visualisatie van een tabel in 'resultspage.html'
@app.route('/dbsearch', methods=['POST', 'GET'])
def search():
    # Invoer van gebruiker afkomstig van 'homepage.html' of 'resultpage.html' bevat een soort LOX waarop gezocht wordt.
    loxrequest = request.form["dropdown"]

    # maakt connectie met lokale database, 'gebruiker', 'wachtwoord', 'locatie:poort/database'
    db = cx_Oracle.connect('hr', 'blaat1234', 'localhost:1521/orcl')
    cursor = db.cursor()
    cursor.execute("""SELECT SOORT_LOX.NAAM, SOORT_LOX.SOORT_LOX_ID, PUBLICATIE.PMID, PUBLICATIE.JAAR, AUTEURS.AUTEUR_NAAM, KEYWORDS.KEYWORD
                      FROM SOORT_LOX, APPLICATIE, PUBLICATIE, AUTEURS, KEYWORDS, REL_KEYW_PUBL, REL_PUBL_STLOX, REL_AUT_PUBL, REL_APPL_STLOX
                      WHERE SOORT_LOX.NAAM LIKE '"""+loxrequest+"""'
                      AND APPLICATIE.APPLICATIE_ID = REL_APPL_STLOX.APPLICATIE_APPLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = REL_APPL_STLOX.SOORT_LOX_SOORT_LOX_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_PUBL_STLOX.PUBLICATIE_PUBLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = REL_PUBL_STLOX.SOORT_LOX_SOORT_LOX_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_AUT_PUBL.PUBLICATIE_PUBLICATIE_ID AND AUTEURS.AUTEURS_ID = REL_AUT_PUBL.AUTEURS_AUTEURS_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_KEYW_PUBL.PUBLICATIE_PUBLICATIE_ID AND KEYWORDS.KEYWORDS_ID = REL_KEYW_PUBL.KEYWORDS_KEYWORDS_ID
                      """)

    # haalt alle gevonden resultaten op
    queryresult = cursor.fetchall()

    # zet de data uit de zoekquery, een tuple, om in een nested list met daarin strings
    querylist = list()
    for rij in queryresult:
        queryrowitemlist = list()
        for item in rij:
            queryrowitemlist.append(str(item))
        querylist.append(queryrowitemlist)

    # Geordende dictionairy wordt gemaakt waarbij soort LOXs als keys worden gebruikt, values zijn list met alleen unieke waardes.
    querydict = collections.OrderedDict()
    for i in range(0, len(querylist)):
        if querylist[i][0] not in querydict.keys():
            querydict[querylist[i][0]] = querylist[i][1:]
        else:
            for x in range(1, len(querylist[i][1:])+1):
                if querylist[i][x] not in querydict[querylist[i][0]][x-1]:
                    querydict[querylist[i][0]][x-1]+=', '+(querylist[i][x])

    # Gegevens uit de geordende dictionairy worden opgehaald en verwerkt zodat het in de tabel in html kan worden weergegeven.
    tabellijst = list()
    for keyvalueitem in querydict:
        dictitemslist = list()
        dictitemslist.append(keyvalueitem)
        for i in querydict[keyvalueitem]:
            dictitemslist.append(i)
        tabellijst.append(dictitemslist)

    # Roept html pagina met resultatentabel aan, lijst met rijen die moeten worden weergegeven in de tabel wordt meegegeven.
    return render_template('resultspage.html', resultlist = tabellijst)


# Methode die applicatiegegevens uit de database haalt en retourneerd waarmee een graaf mee wordt gemaakt.
@app.route('/Graph<LOX_ID>/', methods=['POST', 'GET'])
def graph(LOX_ID):
    # connectie met de database
    db = cx_Oracle.connect('hr', 'blaat1234', 'localhost:1521/orcl')
    cursor = db.cursor()

    # SQL query
    cursor.execute("""
                     SELECT APPLICATIE.WOORD1, APPLICATIE.WOORD2, APPLICATIE.RELATION_COUNT
                     FROM APPLICATIE, REL_APPL_STLOX
                     WHERE REL_APPL_STLOX.SOORT_LOX_SOORT_LOX_ID = """+LOX_ID+"""
                     AND REL_APPL_STLOX.APPLICATIE_APPLICATIE_ID = APPLICATIE.APPLICATIE_ID
                     AND APPLICATIE.RELATION_COUNT > 10
                     """)

    applicaties = cursor.fetchall()
    applicaties = [list(row) for row in applicaties]

    # lijsten voor het opslaan van de juiste gegevens uit de database
    graphlist = list()
    woordlijst = [] # bevat alle keywords uit de database, en bijbehorend LOX
    countlijst = [] # bevat de aantallen van de relaties tussen de keywords en soort LOX
    edgelijst = []  # bevat lijsten met daarin twee woorden die een relatie met elkaar hebben

    for row in applicaties:
        if row[0] not in woordlijst:
            woordlijst.append(row[0])
        if row[1] not in woordlijst:
            woordlijst.append(row[1])
        edgelijst.append(row[:2])
        countlijst.append(row[2])

    # graphlist is een nested list die de lijsten met alle woorden, count gegevens en edge gegevens bevat.
    graphlist.append(woordlijst)
    graphlist.append(countlijst)
    graphlist.append(edgelijst)

    return render_template('Graphpage.html', graaflijst = graphlist)


if __name__ == '__main__':
    app.run()
