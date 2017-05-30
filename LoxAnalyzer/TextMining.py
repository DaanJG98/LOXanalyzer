from Bio import Entrez
Entrez.email = "koenrademaker@outlook.com"
keyword_list = ["lipoxygenase", "LOX", "soybean LOX", "microbial LOX", "fungal LOX", "plant LOX", "9-LOX", "13-LOX", "animal LOX", "5-LOX", "8-LOX", "12-LOX", "15-LOX", "10-LOX", "11-LOX"]

def text_mining_get_count(query):
    handle = Entrez.egquery(term=query)
    record = Entrez.read(handle)

    for row in record["eGQueryResult"]:
        if row["DbName"] == "pubmed":
            count = int(row["Count"])
    handle.close()
    return count

def text_mining_esearch(query, count):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=count)
    record = Entrez.read(handle)
    temp_id_list = record["IdList"]

    id_list = []
    for item in temp_id_list:
        id_list.append(int(item))

    return id_list

def text_mining_esummary(identifier):
    handle = Entrez.esummary(db="pubmed", id=identifier)
    record = Entrez.read(handle)

    publication_year = record[0]['PubDate'][0:4]
    temp_author_list = record[0]['AuthorList']

    author_list = []
    for item in temp_author_list:
        author_list.append(str(item))

    return publication_year, author_list

def text_mining_efetch(identifier):
    temp_keyword_list = []

    handle = Entrez.efetch(db="pubmed", id=identifier, rettype="pubmed")
    record = handle.read()
    record_list = record.split("\n")

    for line in record_list:
        if "</Keyword>" in line:
            temp_keyword = line[line.find(">") + 1:line.find("</Keyword>")]
            temp_keyword_list.append(temp_keyword)

    return temp_keyword_list

def save_data_to_database(publicatie_pmid, publicatie_jaar, auteur_naam, keywords_keyword):
    print("DEBUG")
    # CONNECTIE MET DATABASE OPENEN
    #
    # publicatie_id = (SELECT MAX(PUBLICATIE_ID) FROM PUBLICATIE)+1
    # INSERT INTO PUBLICATIE VALUES (publicatie_pmid, publicatie_jaar, publicatie_id)
    #
    # for auteur in auteur_naam:
        # auteurs_id = (SELECT MAX(AUTEURS_ID) FROM AUTEURS)+1
        # INSERT INTO AUTEURS VALUES (auteur, auteurs_id)
        # INSERT INTO RELATION_15 VALUES (publicatie_id, auteurs_id)
    #
    # for keyword in keywords_keyword:
        # keyword_id = (SELECT MAX(KEYWORDS_ID) FROM KEYWORDS)+1
        # INSERT INTO KEYWORDS VALUES (keyword, keyword_id)
        # INSERT INTO RELATION_14 VALUES (keyword_id, publicatie_id)
    #
    # CONNECTIE MET DATABASE SLUITEN

def save_data_to_database_2(publicatie_pmid, publicatie_jaar, auteur_naam):
    print("DEBUG")
    # CONNECTIE MET DATABASE OPENEN
    #
    # publicatie_id = (SELECT MAX(PUBLICATIE_ID) FROM PUBLICATIE)+1
    # INSERT INTO PUBLICATIE VALUES (publicatie_pmid, publicatie_jaar, publicatie_id)
    #
    # for auteur in auteur_naam:
        # auteurs_id = (SELECT MAX(AUTEURS_ID) FROM AUTEURS)+1
        # INSERT INTO AUTEURS VALUES (auteur, auteurs_id)
        # INSERT INTO RELATION_15 VALUES (publicatie_id, auteurs_id)
    #
    # CONNECTIE MET DATABASE SLUITEN


def main():
    for keyword in keyword_list:
        count = text_mining_get_count(keyword)
        if count != 0:
            print("--DEBUG-- Results found: YES")
            id_list = text_mining_esearch(keyword, count)
            for article_id in id_list:
                article_publ_year, article_auth_list = text_mining_esummary(article_id)
                print("--DEBUG-- PMID: ", article_id)
                print("--DEBUG-- YEAR: ", article_publ_year)
                print("--DEBUG-- Authors: ", article_auth_list)
                try:
                    article_keyw_list = text_mining_efetch(article_id)
                    print("--DEBUG-- Keywords found: YES")
                    print("--DEBUG-- Keywords: ", article_keyw_list)
                except UnicodeDecodeError:
                    print("--DEBUG-- Keywords found: NO")
                print("--DEBUG-- END OF RESULT\n")
        else:
            print("--DEBUG-- Results found: NO")

main()