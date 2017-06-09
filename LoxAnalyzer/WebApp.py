from flask import Flask, render_template, request
import cx_Oracle
import collections

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/dbsearch', methods=['POST', 'GET'])
def search():
    text = request.form["searchword"]
    db = cx_Oracle.connect('hr', 'blaat1234', 'localhost:1521/orcl')
    cursor = db.cursor()
    cursor.execute("""SELECT SOORT_LOX.NAAM, SOORT_LOX.SOORT_LOX_ID, PUBLICATIE.PMID, PUBLICATIE.JAAR, AUTEURS.AUTEUR_NAAM, KEYWORDS.KEYWORD, ORGANISME.NAAM, SEQUENTIE.ID_VERSION
                      FROM SOORT_LOX, APPLICATIE, PUBLICATIE, AUTEURS, KEYWORDS, ORGANISME, SEQUENTIE, REL_KEYW_PUBL, REL_PUBL_STLOX, REL_AUT_PUBL, REL_APPL_STLOX
                      WHERE SOORT_LOX.NAAM like '%"""+text+"""%'
                      AND APPLICATIE.APPLICATIE_ID = REL_APPL_STLOX.APPLICATIE_APPLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = REL_APPL_STLOX.SOORT_LOX_SOORT_LOX_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_PUBL_STLOX.PUBLICATIE_PUBLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = REL_PUBL_STLOX.SOORT_LOX_SOORT_LOX_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_AUT_PUBL.PUBLICATIE_PUBLICATIE_ID AND AUTEURS.AUTEURS_ID = REL_AUT_PUBL.AUTEURS_AUTEURS_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_KEYW_PUBL.PUBLICATIE_PUBLICATIE_ID AND KEYWORDS.KEYWORDS_ID = REL_KEYW_PUBL.KEYWORDS_KEYWORDS_ID
                      AND ORGANISME.ORGANISME_ID = SEQUENTIE.ORGANISME_ORGANISME_ID
                      AND SEQUENTIE.SOORT_LOX_SOORT_LOX_ID = SOORT_LOX.SOORT_LOX_ID
                      
                      """)

    queryresult = cursor.fetchall()
    resultlist = list()
    for rij in queryresult:
        L = list()
        for item in rij:
            L.append(str(item))
        resultlist.append(L)

    resultdict = collections.OrderedDict()
    for i in range(0, len(resultlist)):
        if resultlist[i][0] not in resultdict.keys():
            resultdict[resultlist[i][0]] = resultlist[i][1:]
        else:
            for x in range(1, len(resultlist[i][1:])+1):
                if resultlist[i][x] not in resultdict[resultlist[i][0]][x-1]:
                    resultdict[resultlist[i][0]][x-1]+=', '+(resultlist[i][x])

    resultlist2 = list()
    for x in resultdict:
        rtstr = list()
        rtstr.append(x)
        for i in resultdict[x]:
            rtstr.append(i)
        resultlist2.append(rtstr)

    return render_template('resultspage.html', resultlist = resultlist2)


@app.route('/Graph<LOX_ID>/', methods=['POST', 'GET'])
def graph(LOX_ID):
    db = cx_Oracle.connect('hr', 'blaat1234', 'localhost:1521/orcl')
    cursor = db.cursor()

    cursor.execute("""
                     SELECT APPLICATIE.NAAM_SOORT_LOX, APPLICATIE.NAAM_APPLICATIE, APPLICATIE.RELATION_COUNT
                     FROM APPLICATIE, REL_APPL_STLOX
                     WHERE REL_APPL_STLOX.SOORT_LOX_SOORT_LOX_ID = """+LOX_ID+"""
                     AND REL_APPL_STLOX.APPLICATIE_APPLICATIE_ID = APPLICATIE.APPLICATIE_ID
                     """)

    applicaties = cursor.fetchall()
    applicaties = [list(row) for row in applicaties]

    graphlist = list()
    woordlijst = []
    countlijst = []
    edgelijst = []

    for row in applicaties:
        if row[0] not in woordlijst:
            woordlijst.append(row[0])
        if row[1] not in woordlijst:
            woordlijst.append(row[1])
        edgelijst.append(row[:2])
        countlijst.append(row[2])

    graphlist.append(woordlijst)
    graphlist.append(countlijst)
    graphlist.append(edgelijst)

    return render_template('Graphpage.html', lijst = graphlist)


if __name__ == '__main__':
    app.run()