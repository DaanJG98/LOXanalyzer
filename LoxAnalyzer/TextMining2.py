from Bio import Entrez
Entrez.email = "koenrademaker@outlook.com"

keywords = ["5-LOX", "8-LOX", "9-LOX", "9/13-LOX", "10-LOX", "11-LOX", "12-LOX", "13-LOX", "15-LOX"]
applications = ["bleaching", "effect", "application", "pathway", "role", "production", "inhibits", "exhibits"]
synonym_list = [[["3-LOX"], ["hydroperoxy icosatetraenoate dehydratase", "epidermal lipoxygenase-3", "hydroperoxy icosatetraenoate isomerase", "epidermal lipoxygenase-3", "soybean lipoxygenase-3"]]
,[["5-LOX"], ["arachidonate 5-lipoxygenase", "5-lipoxygenase", "5DELTA-lipoxygenase", "arachidonate 5-lipoxygenase", "arachidonic 5-lipoxygenase", "arachidonic acid 5-lipoxygenase", "C-5-lipoxygenase", "DELTA5-lipoxygenase", "lipoxygenase 15", "lipoxygenase 5", "lipoxygenase-1", "PMNL 5-lipoxygenase"]]
,[["8-LOX"], ["arachidonate 8-lipoxygenase", "8(R)-lipoxygenase", "8-lipoxygenase", "8R-lipoxygenase", "8S-lipoxygenase", "arachidonate 8-lipoxygenase", "arachidonic acid C-8 lipoxygenase", "linoleate 8R-lipoxygenase", "linoleate 8R-lipoxygenase"]]
,[["9-LOX"], ["linoleate 9S-lipoxygenase", "9-lipoxygenase", "9S-lipoxygenase", "epidermal lipoxygenase-3", "linoleate 9-lipoxygenase", "linoleate 9S-lipoxygenase", "linolenate 9R-lipoxygenase", "9R-lipoxygenase", "linolenate 9R-lipoxygenase"]]
,[["9/13-LOX"], ["linoleate 9/13-lipoxygenase", "13/9 lipoxygenase", "9-lipoxygenase", "9/13-lipoxygenase", "linoleate 9 S-lipoxygenase", "linoleate 9/13-lipoxygenase", "manganese 9S-lipoxygenase"]]
,[["10-LOX"], ["linoleate 10R-lipoxygenase", "linoleate 10R-lipoxygenase", "oleate 10S-lipoxygenase", "oleate 10S-lipoxygenase"]]
,[["11-LOX"], ["linoleate 11-lipoxygenase", "linoleate 11-lipoxygenase", "manganese lipoxygenase"], ["12-LOX"], ["arachidonate 12-lipoxygenase", "(12R)-lipoxygenase", "11R-lipoxygenase", "12(R)-lipoxygenase", "12(S)-lipoxygenase", "12-lipoxygenase", "12/15 lipoxygenase", "12/15-lipoxygenase", "12/15-lipoxygenases", "12DELTA-lipoxygenase", "12R-lipoxygenase", "12S-lipoxygenase", "2/15-lipoxygenase", "arachidonate 12-lipoxygenase", "C-12 lipoxygenase", "DELTA 12-lipoxygenase", "epidermal-type lipoxygenase", "human platelet 12-lipoxygenase", "leukocyte-type 12-lipoxygenase", "leukocyte-type 12/15-lipoxygenase", "leukocyte-type lipoxygenase", "lipoxygenase 12", "platelet-type 12(S)-lipoxygenase", "platelet-type 12-human lipoxygenase", "platelet-type 12-lipoxygenase", "Platelet-type lipoxygenase 12"]]
,[["12-LOX"], ["arachidonate 12-lipoxygenase", "(12R)-lipoxygenase", "11R-lipoxygenase", "12(R)-lipoxygenase", "12(S)-lipoxygenase", "12-lipoxygenase", "12/15 lipoxygenase", "12/15-lipoxygenase", "12/15-lipoxygenases", "12DELTA-lipoxygenase", "12R-lipoxygenase", "12S-lipoxygenase", "2/15-lipoxygenase", "arachidonate 12-lipoxygenase", "C-12 lipoxygenase", "DELTA 12-lipoxygenase", "epidermal-type lipoxygenase", "human platelet 12-lipoxygenase", "leukocyte-type 12-lipoxygenase", "leukocyte-type 12/15-lipoxygenase", "leukocyte-type lipoxygenase", "lipoxygenase 12", "platelet-type 12(S)-lipoxygenase", "platelet-type 12-human lipoxygenase", "platelet-type 12-lipoxygenase", "Platelet-type lipoxygenase 12"]]
,[["13-LOX"], ["linoleate 13S-lipoxygenase", "(13S)-lipoxygenase", "13-lipoxygenase", "13S-lipoxygenase", "15-lipoxygenase-1", "iron 13S-lipoxygenase", "linoleate 13-lipoxygenase", "linoleate 13S-lipoxygenase", "lipoxygenase 2", "lipoxygenase-1", "lipoxygenase-2", "lipoxygenase-3", "lipoxygenase-4", "lipoxygenase-6", "soybean lipoxygenase-1"]]
, [["15-LOX"], ["12/15 lipoxygenase", "12/15-lipoxygenase", "15(S)-lipoxygenase-1", "15-lipoxygenase", "15-lipoxygenase 1", "15-lipoxygenase 2", "15-lipoxygenase type 1", "15-lipoxygenase type 2", "15-lipoxygenase type-1", "15-lipoxygenase-1", "15-lipoxygenase-2", "15-lipoxygenase-I", "15S-lipoxygenase", "arachidonate 15-lipoxygenase", "arachidonate 15-lipoxygenase-1", "arachidonic acid 15-lipoxygenase", "endothelial 15-lipoxygenase-1", "human prostate epithelial 15-lipoxygenase-2", "linoleic acid omega-6-lipoxygenase", "lipoxygenase L-1", "lipoxygenase-1", "omega-6 lipoxygenase", "reticulocyte 15-lipoxygenase-1", "reticulocyte-type 15-human lipoxygenase", "reticulocyte-type 15-lipoxygenase", "soybean 15-lipoxygenase", "soybean lipoxygenase-3"]]]
relations = []
relation_count = []


def text_mining_get_count(query):
    handle = Entrez.egquery(term=query)
    record = Entrez.read(handle)

    for row in record["eGQueryResult"]:
        if row["DbName"] == "pubmed":
            count = int(row["Count"])
    handle.close()

    return count
# Retourneert het aantal hits op basis van de PubMed-query.

def combine(keyword, application):
    temp_string = "("
    for item in synonym_list:
        if(keyword == item[0][0]):
            temp_string += item[0][0]+"*"
            for synonym in item[1]:
                temp_string += synonym+"*"

    temp_string = temp_string.replace("*", ") OR (")
    temp_string = temp_string[:len(temp_string)-5]
    temp_string = "("+temp_string+")"+" AND "+application

    print("--DEBUG-- Query being used:", temp_string)
    return temp_string
# Zet de keywords en applicaties om naar een geschikte query.

def cross_reference(keyword, application):
    count = text_mining_get_count(combine(keyword, application))

    if count > 0:
        relations.append([keyword, application])
        relation_count.append(count)
        print("--DEBUG-- Results found for", keyword, "with", application)
    else:
        print("--DEBUG-- No results found for", keyword, "with", application)
# Voert de vergelijking uit tussen keyword en applicatie.

for keyword in keywords:
    for application in applications:
        cross_reference(keyword, application)
# Resultaten zijn opgeslagen in de lijsten -relations en -relation_count, de id's zijn hetzelfde voor elke record, dus -relations[0] hoort bij -relation_count[0] enz.
