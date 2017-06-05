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

    # db = cx_Oracle.connect('owe7_pg2', 'blaat1234', 'cytosine.nl:1521/XE')
    # cursor = db.cursor()
    # cursor.execute('''
    #                 SELECT SOORT_LOX.NAAM, APPLICATIE.NAAM, PUBLICATIE.PUBMEDID, PUBLICATIE.DATUM, AUTEUR.NAAM, KEYWORDS.WOORD, ORGANISME.NAAM, SEQUENTIE.VERSION_ID
    #                 FROM SOORT_LOX, APPLICATIE, PUBLICATIE, AUTEUR, KEYWORDS, ORGANISME, SEQUENTIE, RELATION_2, RELATION_3, RELATION_6, RELATION_7
    #                 WHERE APPLICATIE.APPLICATIE_ID = RELATION_6.APPLICATIE_APPLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = RELATION_6.SOORT_LOX_SOORT_LOX_ID
    #                 AND PUBLICATIE.PUBLICATIE_ID = RELATION_7.PUBLICATIE_PUBLICATIE_ID AND APPLICATIE.APPLICATIE_ID = RELATION_7.APPLICATIE_APPLICATIE_ID
    #                 AND PUBLICATIE.PUBLICATIE_ID = RELATION_2.PUBLICATIE_PUBLICATIE_ID AND AUTEUR.AUTEUR_ID = RELATION_2.AUTEUR_AUTEUR_ID
    #                 AND KEYWORDS.KEYWORDS_ID = RELATION_3.KEYWORDS_KEYWORDS_ID AND PUBLICATIE.PUBLICATIE_ID = RELATION_3.PUBLICATIE_PUBLICATIE_ID
    #                 AND ORGANISME.ORGANISME_ID = SEQUENTIE.ORGANISME_ORGANISME_ID
    #                 AND SEQUENTIE.SOORT_LOX_SOORT_LOX_ID = SOORT_LOX.SOORT_LOX_ID
    #                 ''')
    #
    # result = cursor.fetchall()
    # result = [list(row) for row in result]
    #
    # for x in range(0, len(result)):
    #     print(result[x])

    demolijst = [('13-LOX', 'Bleken', '27403427', '2017', 'Gilissen D.', 'defense, herbivore, oxylipin', 'Kutkikker', 'AOM81152.1'),
                 ('15-LOX', 'Bleken', '27403427',  '2015', 'Rademaker K.', 'defense, herbivore, oxylipin', 'Ander beest',
                  'AOM81152.1')]

    return render_template('resultspage.html', resultlist = demolijst)


@app.route('/Graph', methods=['POST', 'GET'])
def Graph():
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
    countlist = ['500', '253', '120', '53']
    edgelist = [[0,2],[1,2],[1,3],[2,4]]
    graphlist.append(wordlist)
    graphlist.append(countlist)
    graphlist.append(edgelist)

    return render_template('Graphpage.html', lijst = graphlist)


if __name__ == '__main__':
    app.run()