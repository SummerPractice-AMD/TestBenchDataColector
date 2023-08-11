# TestBenchDataColector
~Componenta DataColector

##Colectarea si incarcarea datelor in MongoDB

-Scriptul **DBCollector** se utilizeaza pentru a colecta datele si de a le incarca intr-o baza de date MongoDB. Acesta se foloseste de scripturile **generatejson.py** si **introducereDB.py** pentru a genera datele in format JSON si pentru a le incarca in baza de date.

###Functionare

-Scriptul **DBCollector** primeste argumente de la linia de comanda pentru a specifica directorul care contine fisierele cu datele de intrare. Pentru a rula scriptul, se deschide terminalul si se navigheaza la directorul in care se afla acesta. Apoi se foloseste urmatoarea comanda pentru a colecta si incarca datele in baza de date: 

             python DBCollector.py --dir=/calea_catre_director/

-Este necesara instalarea modulelor Python: pymongo, argparse, json si yaml

