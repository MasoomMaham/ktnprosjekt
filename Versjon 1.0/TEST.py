__author__ = 'henrikmm'
import json


liste2 = []

dictafon2 = {"TEST": "NEI", "ARRAY": "KUKK"}
dictafon = {"TEST": "JA", "LISTE": "LOL"}
liste2.append(dictafon)
liste2.append(dictafon2)
for i in liste2:

    jsonobj = json.dumps(i)

    backto = json.loads(jsonobj)
    liste = backto["TEST"]
    str(liste)
    print(str(liste)+" TYPE OF ELEMENT: "+str(type(liste[0])))
