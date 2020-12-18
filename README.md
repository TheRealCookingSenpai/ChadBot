# ChadBot
Un chatbot sperimentale in Italiano, scritto in Python.

ChadBot è in esecuzione su http://chadbot.ml e su telegram tramite https://t.me/TG_ChadBot

## Cosa è ChadBot

Si tratta di un semplice chatbot scritto in Python completamente da zero, funzionante anche tramite Telegram.

L'obbiettivo è quello di ottenere un sistema di apprendimento semplice, leggero e privo di peso sulle risorse della macchina.

## Cosa non è ChadBot

Non è un chatbot avanzato che utilizza reti neurali o algoritmi di machine learning, e non è un esempio di intelligenza artificiale. Anche se, a lungo andare, può sembrare che lo sia.

## Come funziona ChadBot

Il funzionamento è molto semplice.
Inizialmente, ChadBot non sa nulla.
Ogni volta che un utente digita qualcosa che ChadBot non sa, il bot chiede all'utente che risposta dovrebbe dare e la memorizza in un database, standardizzandola (ovvero togliendo punteggiatura e simboli) e assegnando un grado di confidenza.
La ricerca nel database comprende, in caso non vi sia una corrispondenza esatta, una ricerca basata sulla similitudine secondo l'algoritmo chiamato Indice di Jaccard. Se una corrispondenza abbastanza simile viene trovata, essa viene scelta come risposta.
Attraverso i comandi !y (feedback positivo), !n (feedback negativo), !o (feedback offensivo) e !i (inserzione senza feedback), l'utente può far aumentare o meno la confidenza che ha il bot nell'utilizzare una certa risposta e può inserire risposte alternative. Durante la scelta della risposta, il bot valuterà cosa rispondere anche in base alla confidenza presente, attraverso una scelta pseudo casuale pesata.

N.B. I comandi !nn e !oo permettono di fornire un feedback senza inserire nuove risposte

# Come hostare la propria versione di ChadBot

## Versione web:

- Utilizza un qualsiasi stack apache+mysql su una qualsiasi distribuzione Linux
- Installa Python 3.6 o superiore, ed installa i moduli necessari contenuti in chatdef.py, oltre a mod_wsgi per apache
- Crea /var/www/chadbot inserendo il contenuto di src
- Crea il vhost relativo al wsgi presente in /var/www/chadbot , a seconda della distribuzione che stai usando
- Crea un database vuoto e modifica chatdef.py in modo da inserire le giuste credenziali
- Riavvia apache
- Collegati e divertiti!

## Versione Telegram:

- Crea un bot con BotFather
- Segna il tuo token e inseriscilo in telebot.py
- Avvia telebot.py e inizia a parlare con il bot su Telegram

### Le versioni web e Telegram sono compatibili e indipendenti
