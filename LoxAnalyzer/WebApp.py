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

    db = cx_Oracle.connect('owe7_pg2', 'blaat1234', 'cytosine.nl:1521/XE')
    cursor = db.cursor()
    # cursor.execute('''SELECT SOORT_LOX.NAAM, APPLICATIE.NAAM, PUBLICATIE.PUBMEDID, PUBLICATIE.DATUM, AUTEUR.NAAM, KEYWORDS.WOORD, ORGANISME.NAAM, SEQUENTIE.VERSION_ID
    #                FROM SOORT_LOX, APPLICATIE, PUBLICATIE, AUTEUR, KEYWORDS, ORGANISME, SEQUENTIE
    #
    #                ''')

    # cursor.execute(''' SELECT AUTEUR.NAAM
    #                    FROM RELATION_2, PUBLICATIE, AUTEUR
    #                    WHERE PUBLICATIE.PUBLICATIE_ID = PUBLICATIE_PUBLICATIE_ID AND AUTEUR.AUTEUR_ID = AUTEUR_AUTEUR_ID
    #                 ''')

    cursor.execute(''' SELECT SOORT_LOX.NAAM, APPLICATIE.NAAM
                       FROM RELATION_6, APPLICATIE, SOORT_LOX
                       WHERE APPLICATIE.APPLICATIE_ID = APPLICATIE_APPLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = SOORT_LOX_SOORT_LOX_ID
    ''')
    result = cursor.fetchall()
    for regel in result:
        print(regel)

    demolijst = [('13-LOX', 'Bleken', '27403427', '2017', 'Gilissen D.', 'defense, herbivore, oxylipin', 'Kutkikker', 'AOM81152.1'),
                 ('15-LOX', 'Bleken', '27403427',  '2015', 'Rademaker K.', 'defense, herbivore, oxylipin', 'Ander beest',
                  'AOM81152.1')]

    return render_template('resultspage.html', resultlist = demolijst)


def results(text):
    text = text + "abc"
    return text
    # return render_template('resultspage.html')


if __name__ == '__main__':
    app.run()