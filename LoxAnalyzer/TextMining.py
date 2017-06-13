# Author:   Koen Rademaker
# Date:     13/06/2017
# Version:  0.7
# Status:   In progress

# Complete commentary for all functions
    # Add commentary for write_analysis_to_database
    # Add commentary for main
    # Add commentary for the exact processes within functions
# Check for adequate use of variable names
# Complete debug commentary

from Bio import Entrez
Entrez.email = "koenrademaker@outlook.com"
# Connection to Entrez services, edit the email address to prevent connection issues with connecting to PubMed.

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
# Contains a list of biological processes and terms to use during text mining.

relation_list = []
# Contains all relations between LOXs and a application based on the results of text mining.
# The LOX and application are stored as separate string items within a list.
count_list = []
# Contains the number of matches found for a relation stored in relation_list.
# The index used matches the one used in relation_list and both values are used together for visualization.

def text_mining_get_count(query):
    handle = Entrez.egquery(term=query)
    record = Entrez.read(handle)

    for row in record["eGQueryResult"]:
        if row["DbName"] == "pubmed":
            count = int(row["Count"])
    handle.close()
    return count
# Takes a term as query and returns the number, as an integer, of results for a PubMed query.

def text_mining_esearch(query, count):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=count)
    record = Entrez.read(handle)
    temp_id_list = record["IdList"]
    handle.close()

    id_list = []
    for item in temp_id_list:
        id_list.append(int(item))

    return id_list
# Takes a term as query and a number of items to return as count, returns a list of the PMIDs for the PubMed query.

def text_mining_esummary(PMID):
    handle = Entrez.esummary(db="pubmed", id=PMID)
    record = Entrez.read(handle)
    publication_year = record[0]['PubDate'][0:4]
    temp_author_list = record[0]['AuthorList']
    handle.close()

    author_list = []
    for item in temp_author_list:
        author_list.append(str(item))

    return publication_year, author_list
# Takes a PMID and returns the publication year, as an integer, and list of authors, as string items, for a PubMed article.

def text_mining_efetch(PMID):
    temp_keyword_list = []
    handle = Entrez.efetch(db="pubmed", id=PMID, rettype="pubmed")
    try:
        record = handle.read()
    except UnicodeDecodeError:
        print("DEBUG - Error reading XML file, skipped the item.")
        return temp_keyword_list
    record_list = record.split("\n")
    handle.close()

    for line in record_list:
        if "</Keyword>" in line:
            temp_keyword = line[line.find(">") + 1:line.find("</Keyword>")]
            temp_keyword_list.append(temp_keyword)

    return temp_keyword_list
# Takes a PMID and returns a list of keywords, as string items, for a PubMed article.

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
    # Forms a query that combines a LOX with it's synonyms while excluding an application from the query.
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
    # Forms a query that combines a LOX and it's synonyms with an application.
    return temporary_string
# Forms a query that formats multiple terms (LOXs, synonyms and applications) for a PubMed query.

def text_retrieval():
    for synonym_item in range(3, 10,6):
        print("DEBUG - Text retrieval for:", lox_synonym_list[synonym_item][0])
        keyword = lox_synonym_list[synonym_item][0]
        query = combine_query(keyword, "")
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
                    write_retrieval_to_database(article_id, article_year, article_author_list, article_keyword_list, keyword)
                    print("DEBUG - Completed write_retrieval_to_database")
                    for article_keyword in article_keyword_list:
                        if article_keyword not in application_list:
                            application_list.append(article_keyword.lower())
                    print("DEBUG - Article keywords added to application_list")
                except UnicodeDecodeError:
                    write_retrieval_to_database(article_id, article_year, article_author_list, "", keyword)
                print("DEBUG - Completed write_retrieval_to_database")
    print("DEBUG - COMPLETED text retrieval")
# Loops through all LOXs and associated synonyms and performs text retrieval, returning data such as PubMed ID, a list of authors, year of publication and all keywords found in the article.

def text_analysis():
    for synonym_item in range(0, len(lox_synonym_list)):
        print("DEBUG - Text analysis for:", lox_synonym_list[synonym_item][0])
        lox_keyword = lox_synonym_list[synonym_item][0]
        for application in application_list:
            query = combine_query(lox_keyword, application)
            print("DEBUG - Query used:", query)
            count = text_mining_get_count(query)
            if count > 0:
                print("DEBUG - Number of results:", count, "for", lox_keyword, "with", application)
                relation_list.append([lox_keyword, application])
                count_list.append(count)
    print("DEBUG - COMPLETED text analysis")
# Loops through all LOXs and associated synonyms and all known applications and performs text analysis, returning relations found between LOXs and applications and the number of relations.

def write_retrieval_to_database(pmid, year, author_list, keyword_list, soort_lox):
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
        print("DEBUG - Values inserted on publicatie_id", publicatie_id)
        db.commit()
    except cx_Oracle.IntegrityError:
        cursor.execute("""SELECT PUBLICATIE_ID FROM PUBLICATIE WHERE PMID = :publ_pmid""",
                          publ_pmid=pmid
                      )
        query_result = cursor.fetchall()
        query_result = query_result[0][0]
        publicatie_id = query_result
        print("DEBUG - PMID exists, current publicatie_id is:", publicatie_id)
    # Attempt to insert a PubMed article into the database. If the article already exists, it's ID will be copied for later use.

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
            print("DEBUG - Values inserted on auteurs_id", auteurs_id)
        except cx_Oracle.IntegrityError:
            cursor.execute("""SELECT AUTEURS_ID FROM AUTEURS WHERE AUTEUR_NAAM = :aut_naam""",
                              aut_naam=author
                           )
            query_result = cursor.fetchall()
            query_result = query_result[0][0]
            auteurs_id = query_result
            print("DEBUG - Author exists, current auteurs_id is:", auteurs_id)
        except UnicodeEncodeError:
            print("DEBUG - Error with encoding of author name", author)
        # Attempt to insert an author for a PubMed article into the database. If the author already exists, it's ID will be copied for later use.

        try:
            cursor.execute("""INSERT INTO REL_AUT_PUBL VALUES (:aut_id , :publ_id)""",
                              aut_id=auteurs_id,
                              publ_id=publicatie_id
                           )
            db.commit()
            print("DEBUG - Relation inserted on auteurs_id", auteurs_id, "and publicatie_id", publicatie_id)
        except cx_Oracle.IntegrityError:
            print("DEBUG - Relation exists, current auteurs_id is", auteurs_id, "and publicatie_id", publicatie_id)
        # Attempt to insert a PubMed article - author relationship into the database. Already existing relationships will be ignored and the ID won't be copied.
    # Goes through all the authors for a PubMed article and attempts to save the data to the database.

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
                print("DEBUG - Values inserted on keywords_id", keywords_id)
            except cx_Oracle.IntegrityError:
                cursor.execute("""SELECT KEYWORDS_ID FROM KEYWORDS WHERE KEYWORD = :keyw""",
                               keyw=keyword.lower()
                               )
                query_result = cursor.fetchall()
                query_result = query_result[0][0]
                keywords_id = query_result
                print("DEBUG - Keyword already exists, current keywords_id is", keywords_id)
            # Attempt to insert a keyword for a PubMed article into the database. If the keyword already exists, it's ID will be copied for later use.
            except UnicodeEncodeError:
                print("DEBUG - Error with encoding of author name", keyword)

            try:
                cursor.execute("""INSERT INTO REL_KEYW_PUBL VALUES (:keyw_id , :publ_id)""",
                               keyw_id=keywords_id,
                               publ_id=publicatie_id
                               )
                db.commit()
                print("DEBUG - Relation inserted on keywords_id", keywords_id, "and publicatie_id", publicatie_id)
            except cx_Oracle.IntegrityError:
                print("DEBUG - Relation exists, current keywords_id is", keywords_id, "and publicatie_id", publicatie_id)
            # Attempt to insert a PubMed article - keyword relationship into the database. Already existing relationships will be ignored and the ID won't be copied.
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
        print("DEBUG - Relation inserted on soort_lox_id", soort_lox_id, "and publicatie_id", publicatie_id)
    except cx_Oracle.IntegrityError:
        print("DEBUG - Relation exists, current soort_lox_id is", soort_lox_id, "and publicatie_id", publicatie_id)
    # Attempt to insert a PubMed article - type of LOX relationship into the database. Already existing relationships will be ignored and the ID won't be copied.
# Saves the data from text_retrieval() to a local database, including PubMed articles, authors, keywords and the type of LOX.

def write_analysis_to_database():
    for i in range(0, len(relation_list)):
        soort_lox = relation_list[i][0]
        application = relation_list[i][1]
        count = count_list[i]

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
            print("DEBUG - Values inserted on applicatie_id", applicatie_id)
            db.commit()
        except cx_Oracle.IntegrityError:
            cursor.execute("""SELECT APPLICATIE_ID FROM APPLICATIE WHERE WOORD1 = :st_lox AND WOORD2 = :appl""",
                           soort_lox = soort_lox,
                           appl = application)
            query_result = cursor.fetchall()
            query_result = query_result[0][0]
            applicatie_id = query_result

        try:
            cursor.execute("""INSERT INTO REL_APPL_STLOX VALUES (:appl_id , :st_lox_id)""",
                           appl_id = applicatie_id,
                           st_lox_id = soort_lox_id
                           )
            print("DEBUG - Relation inserted on soort_lox_id", soort_lox_id, "and applicatie_id", applicatie_id)
            db.commit()
        except cx_Oracle.IntegrityError:
            print("DEBUG - Relation exists, current soort_lox_id is", soort_lox_id, "and applicatie_id", applicatie_id)
# *Requires commentary*

def main():
    text_retrieval()
    text_analysis()
    write_analysis_to_database()

main()