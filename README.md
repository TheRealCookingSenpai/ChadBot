# ChadBot
Un chatbot sperimentale in Italiano, scritto in Python

## Cosa è ChadBot

Si tratta di un semplice chatbot scritto in Python completamente da zero.

L'obbiettivo è quello di ottenere un sistema di apprendimento semplice, leggero e privo di peso sulle risorse della macchina.

## Cosa non è ChadBot

Non è un chatbot avanzato che utilizza reti neurali o algoritmi di machine learning, e non è un esempio di intelligenza artificiale. Anche se, a lungo andare, può sembrare che lo sia.

## Come funziona ChadBot

TODO

# Come hostare la propria versione di ChadBot

- Utilizza un qualsiasi stack apache+mysql su una qualsiasi distribuzione Linux
- Installa Python 3.6 o superiore, ed installa i moduli necessari contenuti in chatdef.py, oltre a mod_wsgi per apache
- Crea /var/www/chadbot inserendo il contenuto di src
- Crea il vhost relativo al wsgi presente in /var/www/chadbot , a seconda della distribuzione che stai usando
- Crea un database vuoto e modifica chatdef.py in modo da inserire le giuste credenziali
- Riavvia apache
- Collegati e divertiti!
