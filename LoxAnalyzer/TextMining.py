# Author:   Koen Rademaker
# Date:     16/06/2017
# Version:  1.0
# Status:   Complete

from Bio import Entrez
Entrez.email = "koenrademaker@outlook.com"
# Connection to Entrez services, edit the Entrez.email to prevent connection issues with connecting to PubMed.

import cx_Oracle
dsnStr = cx_Oracle.makedsn("localhost", "1521", "orcl")
db = cx_Oracle.connect(user="hr", password="blaat1234", dsn=dsnStr)
cursor = db.cursor()
# Connection to the local database.

lox_synonym_list = [["3-LOX", ["3-lipoxygenase", "hydroperoxy icosatetraenoate dehydratase", "epidermal lipoxygenase-3", "hydroperoxy icosatetraenoate isomerase", "lipoxygenase-3", "soybean lipoxygenase-3"]],
                    ["5-LOX", ["5-lipoxygenase", "arachidonate 5-lipoxygenase", "5DELTA-lipoxygenase", "arachidonic 5-lipoxygenase", "arachidonic acid 5-lipoxygenase", "C-5-lipoxygenase", "DELTA5-lipoxygenase", "lipoxygenase 15", "lipoxygenase 5", "PMNL 5-lipoxygenase"]],
                    ["8-LOX", ["8-lipoxygenase", "arachidonate 8-lipoxygenase", "8(R)-lipoxygenase", "8R-lipoxygenase", "8S-lipoxygenase", "arachidonic acid C-8 lipoxygenase", "linoleate 8R-lipoxygenase"]],
                    ["9-LOX", ["9-lipoxygenase", "linoleate 9S-lipoxygenase", "9S-lipoxygenase", "linoleate 9-lipoxygenase", "9R-lipoxygenase", "linolenate 9R-lipoxygenase"]],
                    ["9/13-LOX", ["9/13-lipoxygenase", "linoleate 9/13-lipoxygenase", "13/9 lipoxygenase", "linoleate 9 S-lipoxygenase", "manganese 9S-lipoxygenase"]],
                    ["10-LOX", ["10-lipoxygenase", "10R-lipoxygenase", "10S-lipoxygenase"]],
                    ["11-LOX", ["11-lipoxygenase", "linoleate 11-lipoxygenase", "manganese lipoxygenase"]],
                    ["12-LOX", ["12-lipoxygenase", "arachidonate 12-lipoxygenase", "(12R)-lipoxygenase", "11R-lipoxygenase", "12(R)-lipoxygenase", "12(S)-lipoxygenase", "12DELTA-lipoxygenase", "12R-lipoxygenase", "12S-lipoxygenase", "2/15-lipoxygenase", "C-12 lipoxygenase", "DELTA 12-lipoxygenase", "epidermal-type lipoxygenase", "human platelet 12-lipoxygenase", "leukocyte-type 12-lipoxygenase", "leukocyte-type 12/15-lipoxygenase", "leukocyte-type lipoxygenase", "lipoxygenase 12", "platelet-type 12(S)-lipoxygenase", "platelet-type 12-human lipoxygenase", "platelet-type 12-lipoxygenase", "Platelet-type lipoxygenase 12"]],
                    ["12/15-LOX", ["12/15 lipoxygenase", "12/15-lipoxygenases", "12/15-lipoxygenase"]],
                    ["13-LOX", ["13-lipoxygenase", "linoleate 13S-lipoxygenase", "(13S)-lipoxygenase", "13S-lipoxygenase", "iron 13S-lipoxygenase", "linoleate 13-lipoxygenase"]],
                    ["15-LOX", ["15-lipoxygenase", "15(S)-lipoxygenase-1", "15-lipoxygenase 1", "15-lipoxygenase 2", "15-lipoxygenase type 1", "15-lipoxygenase type 2", "15-lipoxygenase type-1", "15-lipoxygenase-1", "15-lipoxygenase-2", "15-lipoxygenase-I", "15S-lipoxygenase", "arachidonate 15-lipoxygenase", "arachidonate 15-lipoxygenase-1", "arachidonic acid 15-lipoxygenase", "endothelial 15-lipoxygenase-1", "human prostate epithelial 15-lipoxygenase-2", "linoleic acid omega-6-lipoxygenase", "lipoxygenase L-1", "omega-6 lipoxygenase", "reticulocyte 15-lipoxygenase-1", "reticulocyte-type 15-human lipoxygenase", "reticulocyte-type 15-lipoxygenase", "soybean 15-lipoxygenase"]]]
# Contains a list of synonyms for each LOX to expand the number of results for a PubMed query.
application_list = ["allergy", "antibiotics", "cancer", "hormone", "immune response", "inhibits", "interaction", "plant"]
# Contains a list of biological terms to use during text mining.

def text_mining_get_count(query):
    handle = Entrez.egquery(term=query)
    record = Entrez.read(handle)

    for row in record["eGQueryResult"]:
        if row["DbName"] == "pubmed":
            count = int(row["Count"])
    handle.close()

    return count
# Takes a search word as 'query', searches PubMed with 'query' and returns the number of results as 'count'.

def text_mining_esearch(query, count):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=count)
    record = Entrez.read(handle)
    temp_id_list = record["IdList"]
    handle.close()

    id_list = []
    for item in temp_id_list:
        id_list.append(int(item))

    return id_list
# Takes a search word as 'query' and a number of results to return as 'count', searches PubMed and returns the resulting PubMed IDs (PMIDs) in 'id_list'.

def text_mining_esummary(pmid):
    handle = Entrez.esummary(db="pubmed", id=pmid)
    record = Entrez.read(handle)
    publication_year = record[0]['PubDate'][0:4]
    temp_author_list = record[0]['AuthorList']
    handle.close()

    author_list = []
    for item in temp_author_list:
        author_list.append(str(item))

    return publication_year, author_list
# Takes a PMID as 'pmid', searches PubMed with 'pmid' and returns the year of publication as 'publication_year' and the list of authors as 'author_list'

def text_mining_efetch(pmid):
    keyword_list = []
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="pubmed")

    try:
        record = handle.read()
    except UnicodeDecodeError:
        print("DEBUG - Error reading XML file, skipped the item.")
        return keyword_list

    record_list = record.split("\n")
    handle.close()

    for line in record_list:
        if "</Keyword>" in line:
            temp_keyword = line[line.find(">") + 1:line.find("</Keyword>")]
            keyword_list.append(temp_keyword)

    return keyword_list
# Takes a PMID as 'pmid', searches PubMed with 'pmid' through the XML file to find keywords and the list of keywords as 'keyword_list'.

def combine_query(lox, application):
    if application == "":
        temporary_string = "("
        for synonym_item in range(0, len(lox_synonym_list)):
            temporary_lox = lox_synonym_list[synonym_item][0]
            if (lox == temporary_lox):
                temporary_string += '"' + lox + '"' + "*"
                for synonym in range(0, len(lox_synonym_list[synonym_item][1])):
                    temporary_synonym = '"' + lox_synonym_list[synonym_item][1][synonym] + '"'
                    temporary_string += temporary_synonym + "*"
        temporary_string = temporary_string.replace("*", ") OR (")
        temporary_string = temporary_string[:len(temporary_string) - 5]
        temporary_string = "(" + temporary_string + ")"
    # Forms a query if no application is given and only contains a LOX and it's synonyms.
    else:
        temporary_string = "("
        for synonym_item in range(0, len(lox_synonym_list)):
            temporary_lox = lox_synonym_list[synonym_item][0]
            if (lox == temporary_lox):
                temporary_string += '"' + lox + '"' + "*"
                for synonym in range(0, len(lox_synonym_list[synonym_item][1])):
                    temporary_synonym = '"' + lox_synonym_list[synonym_item][1][synonym] + '"'
                    temporary_string += temporary_synonym + "*"
        temporary_string = temporary_string.replace("*", ") OR (")
        temporary_string = temporary_string[:len(temporary_string) - 5]
        temporary_string = "(" + temporary_string + ")" + " AND " + application
    # Forms a query if an application is given and contains a LOX, it's synonyms and an application.

    return temporary_string
# Takes a LOX name as 'lox' and an application name as 'application', forms a query for PubMed that includes all LOX synonyms and the application and returns it as 'temporary_string'
# If no application is given a query is formed that only contains all the LOX synonyms.

def text_retrieval():
    print("DEBUG - START text_retrieval()")
    for synonym_item in range(0, len(lox_synonym_list)):
        lox = lox_synonym_list[synonym_item][0]
        query = combine_query(lox, "")
        print("DEBUG - Text retrieval for:", lox_synonym_list[synonym_item][0])
        print("DEBUG - Query used:", query)
        count = text_mining_get_count(query)

        if (count != 0):
            print("DEBUG - Number of results:", count)
            id_list = text_mining_esearch(query, count)

            for article_id in id_list:
                article_year, article_author_list = text_mining_esummary(article_id)
                article_year = int(article_year)

                try:
                    article_keyword_list = text_mining_efetch(article_id)
                    write_retrieval_to_database(article_id, article_year, article_author_list, article_keyword_list, lox)
                    print("DEBUG - Completed write_retrieval_to_database()")
                except UnicodeDecodeError:
                    write_retrieval_to_database(article_id, article_year, article_author_list, "", lox)
                print("DEBUG - Completed write_retrieval_to_database")
        else:
            print("DEBUG - No results found")
    print("DEBUG - COMPLETED text_retrieval()")
# Loops through all LOXs and synonyms from 'lox_synonym_list' and performs text retrieval with PubMed, returning a PMID, publication year, author list and keywords list.

def text_analysis():
    print("DEBUG - START text_analysis()")
    cursor.execute("""SELECT KEYWORD FROM KEYWORDS ORDER BY KEYWORD""")
    query_result = cursor.fetchall()

    for item in query_result:
        if item not in application_list:
            application_list.append((item[0]))

    for synonym_item in range(0, len(lox_synonym_list)):
        lox_keyword = lox_synonym_list[synonym_item][0]
        print("DEBUG - Text analysis for:", lox_keyword)

        for application in application_list:
            query = combine_query(lox_keyword, application)
            print("DEBUG - Query used:", query)
            count = text_mining_get_count(query)

            if count > 0:
                print("DEBUG -", count, "results found for application:", application)
                write_analysis_to_database(lox_keyword, application, count)
    print("DEBUG - COMPLETED text_analysis()")
# Performs text analysis, forming new querys with keywords from 'application_list' and LOXs and their synonyms from 'lox_synonym_list' to find new relation.
# Newly discovered relations are saved to the local database with write_analysis_to_database()

def write_retrieval_to_database(pmid, year, author_list, keyword_list, soort_lox):
    print("DEBUG - START write_retrieval_to_database()")
    cursor.execute("""SELECT MAX(PUBLICATIE_ID) FROM PUBLICATIE""")
    query_result = cursor.fetchall()
    query_result = query_result[0][0]
    publicatie_id = query_result + 1

    try:
        cursor.execute("""INSERT INTO PUBLICATIE VALUES (:publ_pmid , :publ_year, :publ_id)""",
                          publ_pmid = pmid,
                          publ_year = year,
                          publ_id = publicatie_id
                       )
        print("DEBUG - Values inserted to table PUBLICATIE on PUBLICATIE_ID", publicatie_id)
        db.commit()
    except cx_Oracle.IntegrityError:
        cursor.execute("""SELECT PUBLICATIE_ID FROM PUBLICATIE WHERE PMID = :publ_pmid""",
                          publ_pmid=pmid
                      )
        query_result = cursor.fetchall()
        query_result = query_result[0][0]
        publicatie_id = query_result
        print("DEBUG - PMID is not unique, current PUBLICATIE_ID is:", publicatie_id)
    # Attempt to insert a PubMed article into the local database. If it already exists, the PMID will be copied for later use.

    for author in author_list:
        cursor.execute("""SELECT MAX(AUTEURS_ID) FROM AUTEURS""")
        query_result = cursor.fetchall()
        query_result = query_result[0][0]
        auteurs_id = query_result + 1

        try:
            cursor.execute("""INSERT INTO AUTEURS VALUES (:aut_naam , :aut_id)""",
                              aut_naam=author,
                              aut_id=auteurs_id
                           )
            db.commit()
            print("DEBUG - Values inserted to tabel AUTUERS on AUTEURS_ID", auteurs_id)
        except cx_Oracle.IntegrityError:
            cursor.execute("""SELECT AUTEURS_ID FROM AUTEURS WHERE AUTEUR_NAAM = :aut_naam""",
                              aut_naam=author
                           )
            query_result = cursor.fetchall()
            query_result = query_result[0][0]
            auteurs_id = query_result
            print("DEBUG - Author is not unique, current AUTEURS_ID is:", auteurs_id)
        except UnicodeEncodeError:
            print("DEBUG - Error with encoding of author name", author)
        # Attempt to insert an author for a PubMed article into the local database. If the author already exists, the ID will be copied for later use.

        try:
            cursor.execute("""INSERT INTO REL_AUT_PUBL VALUES (:aut_id , :publ_id)""",
                              aut_id=auteurs_id,
                              publ_id=publicatie_id
                           )
            db.commit()
            print("DEBUG - Relation inserted to table REL_AUT_PUBL on AUTEURS_ID", auteurs_id, "and PUBLICATIE_ID", publicatie_id)
        except cx_Oracle.IntegrityError:
            print("DEBUG - Relation exists, current AUTEURS_ID is", auteurs_id, "and PUBLICATIE_ID", publicatie_id)
        # Attempt to insert a relationship between PubMed article and author into the local database. If the relationship already exists, it will be ignored.
    # Loops through all the authors for a PubMed article and attempts to save the data to the local database.

    if keyword_list != []:
        print("DEBUG - Keywords found")
        for keyword in keyword_list:
            cursor.execute("""SELECT MAX(KEYWORDS_ID) FROM KEYWORDS""")
            query_result = cursor.fetchall()
            query_result = query_result[0][0]
            keywords_id = query_result + 1

            try:
                cursor.execute("""INSERT INTO KEYWORDS VALUES (:keyw , :keyw_id)""",
                               keyw=keyword.lower(),
                               keyw_id=keywords_id
                               )
                db.commit()
                print("DEBUG - Values inserted to table KEYWORDS on KEYWORDS_ID", keywords_id)
            except cx_Oracle.IntegrityError:
                cursor.execute("""SELECT KEYWORDS_ID FROM KEYWORDS WHERE KEYWORD = :keyw""",
                               keyw=keyword.lower()
                               )
                query_result = cursor.fetchall()
                query_result = query_result[0][0]
                keywords_id = query_result
                print("DEBUG - Keyword already exists, current KEYWORDS_ID is", keywords_id)
            # Attempt to insert a keyword for a PubMed article into the database. If the keyword already exists, it's ID will be copied for later use.
            except UnicodeEncodeError:
                print("DEBUG - Error with encoding of author name", keyword)

            try:
                cursor.execute("""INSERT INTO REL_KEYW_PUBL VALUES (:keyw_id , :publ_id)""",
                               keyw_id=keywords_id,
                               publ_id=publicatie_id
                               )
                db.commit()
                print("DEBUG - Relation inserted to table REL_KEYW_PUBL on KEYWORDS_ID", keywords_id, "and PUBLICATIE_ID", publicatie_id)
            except cx_Oracle.IntegrityError:
                print("DEBUG - Relation already exists, current KEYWORDS_ID is", keywords_id, "and PUBLICATIE_ID", publicatie_id)
            # Attempt to insert a relationship between PubMed article and keyword into the local database. If the relationship already exists, it will be ignored.
    # Goes through all the keywords for a PubMed article and attempts to save the data to the database.

    cursor.execute("""SELECT SOORT_LOX_ID FROM SOORT_LOX WHERE NAAM = :lox""",
                       lox=soort_lox
                       )
    query_result = cursor.fetchall()
    query_result = query_result[0][0]
    soort_lox_id = query_result

    try:
        cursor.execute("""INSERT INTO REL_PUBL_STLOX VALUES (:publ_id , :stlox_id)""",
                       publ_id=publicatie_id,
                       stlox_id=soort_lox_id
                       )
        db.commit()
        print("DEBUG - Relation inserted to table REL_PUBL_STLOX on SOORT_LOX_ID", soort_lox_id, "and PUBLICATIE_ID", publicatie_id)
    except cx_Oracle.IntegrityError:
        print("DEBUG - Relation already exists, current SOORT_LOX_ID is", soort_lox_id, "and PUBLICATIE_ID", publicatie_id)
    # Attempt to insert a relationship between PubMed article and type of LOX into the local database. If the relationship already exists, it will be ignored.
# Saves data from text_retrieval() to the local database, including PubMed publications, authors, keywords and type of LOX.

def write_analysis_to_database(soort_lox, application, count):
    cursor.execute("""SELECT SOORT_LOX_ID FROM SOORT_LOX WHERE NAAM = :st_lox""",
                   st_lox=soort_lox)
    query_result = cursor.fetchall()
    query_result = query_result[0][0]
    soort_lox_id = query_result

    cursor.execute("""SELECT MAX(APPLICATIE_ID) FROM APPLICATIE""")
    query_result = cursor.fetchall()
    query_result = query_result[0][0]
    applicatie_id = query_result + 1

    try:
        cursor.execute("""INSERT INTO APPLICATIE VALUES (:woord1 , :woord2 , :relation_count , :appl_id)""",
                       woord1 = soort_lox,
                       woord2 = application,
                       relation_count = count,
                       appl_id = applicatie_id)
        print("DEBUG - Values inserted to table APPLICATIE on APPLICATIE_ID", applicatie_id)
        db.commit()
    except cx_Oracle.IntegrityError:
        cursor.execute("""SELECT APPLICATIE_ID FROM APPLICATIE WHERE WOORD1 = :st_lox AND WOORD2 = :appl""",
                       soort_lox = soort_lox,
                       appl = application)
        query_result = cursor.fetchall()
        query_result = query_result[0][0]
        applicatie_id = query_result
        print("DEBUG - Combination of WOORD1 and WOORD2 is not unique, current APPLICATIE_ID is:", applicatie_id)

    try:
        cursor.execute("""INSERT INTO REL_APPL_STLOX VALUES (:appl_id , :st_lox_id)""",
                       appl_id = applicatie_id,
                       st_lox_id = soort_lox_id
                       )
        print("DEBUG - Relation inserted to table REL_APPL_STLOX on SOORT_LOX_ID", soort_lox_id, "and APPLICATIE_ID", applicatie_id)
        db.commit()
    except cx_Oracle.IntegrityError:
        print("DEBUG - Relation already exists, current SOORT_LOX_ID is", soort_lox_id, "and APPLICATIE_ID", applicatie_id)
# Saves data from text_analysis() to the local database, including applications.

def main():
    text_retrieval()
    text_analysis()
# Runs the two main functions, text_retrieval() and text_analysis() of the applications.

main()
