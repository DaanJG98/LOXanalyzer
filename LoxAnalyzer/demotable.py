import cx_Oracle
import collections

def search():
    text = "13-LOX"
    db = cx_Oracle.connect('hr', 'blaat1234', 'localhost:1521/orcl')
    cursor = db.cursor()
    cursor.execute("""SELECT SOORT_LOX.NAAM, SOORT_LOX.SOORT_LOX_ID, PUBLICATIE.PMID, PUBLICATIE.JAAR, AUTEURS.AUTEUR_NAAM, KEYWORDS.KEYWORD
                      FROM SOORT_LOX, APPLICATIE, PUBLICATIE, AUTEURS, KEYWORDS, REL_KEYW_PUBL, REL_PUBL_STLOX, REL_AUT_PUBL, REL_APPL_STLOX
                      WHERE SOORT_LOX.NAAM LIKE '"""+text+"""'
                      AND APPLICATIE.APPLICATIE_ID = REL_APPL_STLOX.APPLICATIE_APPLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = REL_APPL_STLOX.SOORT_LOX_SOORT_LOX_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_PUBL_STLOX.PUBLICATIE_PUBLICATIE_ID AND SOORT_LOX.SOORT_LOX_ID = REL_PUBL_STLOX.SOORT_LOX_SOORT_LOX_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_AUT_PUBL.PUBLICATIE_PUBLICATIE_ID AND AUTEURS.AUTEURS_ID = REL_AUT_PUBL.AUTEURS_AUTEURS_ID
                      AND PUBLICATIE.PUBLICATIE_ID = REL_KEYW_PUBL.PUBLICATIE_PUBLICATIE_ID AND KEYWORDS.KEYWORDS_ID = REL_KEYW_PUBL.KEYWORDS_KEYWORDS_ID
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
            graphid = resultlist[i][1]
            print(graphid)
            pubgroup = list(resultlist[i][2:5])
            print(pubgroup)
            keyw = resultlist[i][5]
            print(keyw)

            resultdict[resultlist[i][0]] = graphid,pubgroup,keyw

        else:
            for x in range(1, len(resultlist[i][1:]) + 1):
                print(resultlist[i][2])
                print(resultdict[resultlist[i][0]][1][0])
                print(resultdict[resultlist[i][0]][1][1])
                if x == 2 and resultlist[i][x] not in resultdict[resultlist[i][0]][1][0]:
                    resultdict[resultlist[i][0]][1][0] += ', ' + (resultlist[i][x])
                if x == 3 and resultlist[i][x] not in resultdict[resultlist[i][0]][1][1]:
                    resultdict[resultlist[i][0]][1][0] += ', ' + (resultlist[i][x])
                # if x == 4 and resultlist[i][x] not in resultdict[resultlist[i][0]][1][2]:
                #     resultdict[resultlist[i][0]][1][0] += ', ' + (resultlist[i][x])
        #         else:
        #             if resultlist[i][x] not in resultdict[resultlist[i][0]][x - 1]:
        #                 resultdict[resultlist[i][0]][x - 1] += ', ' + (resultlist[i][x])



    print(resultdict[resultlist[i][0]])

search()