from flask import Flask, render_template, request
import cx_Oracle

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/dbsearch', methods=['POST', 'GET'])
def search():
    resultslist = list()
    text = request.form["searchword"]

    db = cx_Oracle.connect('hr', 'blaat1234', 'localhost:1521/orcl')
    cursor = db.cursor()
    cursor.execute('''SELECT SOORT_LOX.NAAM, APPLICATIE.APPLICATIE_ID, PUBLICATIE.PMID, PUBLICATIE.JAAR, AUTEURS.AUTEUR_NAAM, KEYWORDS.KEYWORD, ORGANISME.NAAM, SEQUENTIE.ID_VERSION 
                      FROM SOORT_LOX, APPLICATIE, PUBLICATIE, AUTEURS, KEYWORDS, ORGANISME, SEQUENTIE, REL_KEYW_PUBL, REL_PUBL_STLOX, REL_AUT_PUBL, REL_APPL_STLOX
                      WHERE APPLICATIE.APPLICATIE_ID = REL_APPL_STLOX.APPLICATIE_APPLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = REL_APPL_STLOX.SOORT_LOX_SOORT_LOX_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_PUBL_STLOX.PUBLICATIE_PUBLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = REL_PUBL_STLOX.SOORT_LOX_SOORT_LOX_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_AUT_PUBL.PUBLICATIE_PUBLICATIE_ID AND AUTEURS.AUTEURS_ID = REL_AUT_PUBL.AUTEURS_AUTEURS_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_KEYW_PUBL.PUBLICATIE_PUBLICATIE_ID AND KEYWORDS.KEYWORDS_ID = REL_KEYW_PUBL.KEYWORDS_KEYWORDS_ID
                      AND ORGANISME.ORGANISME_ID = SEQUENTIE.ORGANISME_ORGANISME_ID
                      AND SEQUENTIE.SOORT_LOX_SOORT_LOX_ID = SOORT_LOX.SOORT_LOX_ID
                      ''')

    result = cursor.fetchall()
    result = [list(row) for row in result]

    for x in range(0, len(result)):
        print(result[x])

    demolijst = [('13-LOX', 'Bleken', '27403427', '2017', 'Gilissen D.', 'defense, herbivore, oxylipin', 'Kutkikker', 'AOM81152.1'),
                 ('15-LOX', 'Bleken', '27403427',  '2015', 'Rademaker K.', 'defense, herbivore, oxylipin', 'Ander beest',
                  'AOM81152.1')]

    return render_template('resultspage.html', resultlist = result)


@app.route('/Graph<text>/', methods=['POST', 'GET'])
def graph(text):
    # db = cx_Oracle.connect('owe7_pg2', 'blaat1234', 'cytosine.nl:1521/XE')
    # cursor = db.cursor()
    # cursor.execute('''
    #                 SELECT *
    #                 FROM APPLICATIE
    #                 WHERE ...''')
    #
    #

    graphlist = list()

    wordlist = ['Bleeching', 'Lipoxygenase', '13-LOX', 'Cancer stuff', 'improve grain qualities']
    countlist = ['500', '253', '120', '53', '15']
    edgelist = [['Bleeching','13-LOX'],['Lipoxygenase','13-LOX'],['Lipoxygenase','Cancer stuff'],['13-LOX','improve grain qualities'],['Cancer stuff','Bleeching']]
    graphlist.append(wordlist)
    graphlist.append(countlist)
    graphlist.append(edgelist)

    return render_template('Graphpage.html', lijst = graphlist)


if __name__ == '__main__':
    app.run()