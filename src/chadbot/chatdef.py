# -*- coding: latin-1 -*-
#|=======================================================|
#|================== CODED BY ===========================|
#|===============TheCookingSenpai========================|
#|                                                       |
#| Per far funzionare il programma, è necessario creare  |
#| un database e settare i parametri nella funzione      |
#| mysql.connector.connect() posta sotto agli import.    |
#| Il programma necessita anche della cartella ./session |
#| ed è progettato per funzionare con flask.             |
#|                                                       |
#|=======================================================|

# TODO: implementare un sistema di 'mi aspetto questa o quest'altra risposta in base a qualcosa'
# TODO: vedi se è il caso di seguire anche questo https://github.com/luozhouyang/python-string-similarity
# TODO: capire le domande
# TODO: Allenare sui dialoghi dei film https://anjaqantina.jimdofree.com

import random
import mysql.connector
import os
import unidecode
import sys

db = mysql.connector.connect(host="localhost", user="chatuser", password="CHAT20db!", database="chatdb")
cursor = db.cursor()

# Funzione che calcola la similarità di più frasi con l'algoritmo di Jaccard (utilizzata in caso non ci siano match precisi)
def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def digest(msg, cookie):
        # Definizione della sessione in base al cookie
        if not os.path.isdir("/var/www/chadbot/chadbot/session/" + cookie):
                os.system("mkdir /var/www/chadbot/chadbot/session/" + cookie)
        sessiondir = "/var/www/chadbot/chadbot/session/" + cookie

        # Per i messaggi telegram, toglie gli apici
        if msg.startswith("'") and msg.endswith("'"):
                msg = msg[1:-1]

        # Check di controllo per i comandi (partono con !)
        if msg.startswith("!"):
                cmd = msg.split("!")[1].strip()
                # Cookie check
                if cmd=="cookie":
                    return "Numero sessione: " + cookie
                if cmd=="n" or cmd=="o" or cmd=="nn" or cmd=="oo":
                        diminuizione = 1
                        # Se il messaggio è segnato come offensivo, il feedback cala notevolmente
                        if cmd=="o" or cmd=="oo":
                                diminuizione = 5
                        # Diminuire confidenza
                        try:
                                with open(sessiondir + "/ultimoinput") as feedbackbuffer:
                                        ultimo_input = feedbackbuffer.read().strip()
                                with open(sessiondir + "/ultimarisposta") as feedbackbuffer:
                                        ultimo_output = feedbackbuffer.read().strip()
                                # Prova a creare la tabella così da risolvere il problema in caso di similitudini (tabella non esistente)
                                try:
                                    query = "CREATE TABLE `" + ultimo_input + "` (output varchar(255), confidenza int)"
                                    cursor.execute(query)
                                    db.commit()
                                    print("Tabella creata (" + ultimo_input + ")")
                                except:
                                    print("Tabella già presente (" + ultimo_input + ")")
                                query = "UPDATE `" + ultimo_input + "` SET confidenza = confidenza - " + str(diminuizione) + " WHERE output LIKE '" + ultimo_output + "'"
                                cursor.execute(query)
                                db.commit()
                                # Apprendimento da feedback negativo se richiesto (in caso di nn o di oo, non apprende nuove parole)
                                if cmd=="n" or cmd=="o":
                                        with open(sessiondir + "/previous", "w") as previous:
                                                previous.write(ultimo_input)
                                                previous.flush()
                                                return "Come pensi che dovrei rispondere? (Per favore, scrivi solamente la frase che useresti per rispondere al tuo messaggio, senza aggiunte o perifrasi varie)"
                                else:
                                        return "Il tuo feedback è stato registrato."
                        # In caso di errore, messaggio di cortesia
                        except Exception as exc:
                                print("Non sono riuscito a diminuire la confidenza.")
                                print(exc)
                                return "Mi spiace, migliorero'."
                elif cmd=="y":
                        # Aumentare confidenza
                        try:
                                with open(sessiondir + "/ultimoinput") as feedbackbuffer:
                                        ultimo_input = feedbackbuffer.read().strip()
                                with open(sessiondir + "/ultimarisposta") as feedbackbuffer:
                                        ultimo_output = feedbackbuffer.read().strip()
                                # Prova a creare la tabella così da risolvere il problema in caso di similitudini (tabella non esistente)
                                try:
                                    query = "CREATE TABLE `" + ultimo_input + "` (output varchar(255), confidenza int)"
                                    cursor.execute(query)
                                    db.commit()
                                    query = "INSERT INTO `" + ultimo_input + "` VALUES ('" + ultimo_output + "', 100)"
                                    cursor.execute(query)
                                    db.commit()
                                    print("Tabella creata (" + ultimo_input + ").")
                                except:
                                    print("Tabella già esistente (" + ultimo_input + ")")
                                query = "UPDATE `" + ultimo_input + "` SET confidenza = confidenza + 1 WHERE output LIKE '" + ultimo_output + "'"
                                cursor.execute(query)
                                db.commit()
                                print(query)
                        except Exception as exc:
                                print("Non sono riuscito ad aumentare la confidenza.")
                                print(exc)
                        return "Grazie per il tuo feedback! Chadbot e' felice!"
                elif cmd=="i":
                        # Inserimento nuova risposta senza feedback di confidenza
                        try:
                                with open(sessiondir + "/ultimoinput") as feedbackbuffer:
                                        ultimo_input = feedbackbuffer.read().strip()
                                with open(sessiondir + "/previous", "w") as previous:
                                        previous.write(ultimo_input)
                                        previous.flush()
                                return "Inserisci una nuova risposta per questa frase (Per favore, scrivi solamente la frase che useresti per rispondere al tuo messaggio, senza aggiunte o perifrasi varie)"
                        except:
                                return "Scusa. Colpa mia. Ho avuto un piccolo blackout cerebrale e mi sono incartato. Il comando non ha avuto succeso."
                elif cmd=="programmer":
                        return ">> Il programmatore e' TCS <<"
                elif cmd=="help":
                        return ">> Per leggere il manuale, premi il pulsante azzurro in fondo alla pagina. <<"
                elif cmd=="cmd":
                        return ">> !cmd - Lista dei comandi\n !help - manuale\n !programmer - Chi ha programmato ChadBot? <<"
                else:
                        return ">> Comando non riconosciuto. Scrivi !help per le istruzioni o !cmd per la lista dei comandi. <<"

        #Il messaggio viene trasformato in minuscolo, vengono tolti segni di punteggiatura e simili e vengono normalizzati gli accenti
        # TODO: usare nltk per normalizzarlo ancora di più
        msg = msg.lower().strip()
        msg = msg[:254] + (msg[254:] and '..')
        badchar = ",?!-._*\"'.;{}[]"
        for c in badchar:
                msg = msg.replace(c, "")
        # Ulteriore protezione (grezza) da eventuali SQL injection
        msg = msg.replace("select", "")
        msg = msg.replace("delete", "")
        msg = msg.replace("drop", "")
        msg = msg.replace("from", "")
        msg = msg.replace("join", "")
        orig = msg
        # Rimozione accentate
        msg = unidecode.unidecode(msg)
        # Salvataggio messaggio utente nella conversazione
        print("Salvata la conversazione")
        with open(sessiondir + "/conversazione", "a+") as conversazione:
            conversazione.write("Utente: " + msg + "\n")
            conversazione.flush()

        # Blocco apprendimento
        if os.path.isfile(sessiondir + "/previous"):
                with open(sessiondir + "/previous", "r+") as previous:
                        inputmsg = previous.read()
                os.remove(sessiondir + "/previous")
                try:
                        cursor.execute("CREATE TABLE `" + inputmsg + "` (output varchar(255), confidenza int)")
                        db.commit()
                except:
                        print("Non son riuscito a creare la tabella (magari esiste già?)")
                # Controllo per evitare ridondanze
                dupli_query = "SELECT * FROM `" + inputmsg + "` WHERE output LIKE '" + msg + "'"
                print(dupli_query)
                cursor.execute(dupli_query)
                dupli_result = cursor.fetchall()
                if not dupli_result:
                        # Inserimento risposta nuova
                        print("Inserisco la nuova risposta")
                        print("INSERT INTO `" + inputmsg + "` VALUES ('" + msg + "', 100)")
                        cursor.execute("INSERT INTO `" + inputmsg + "` VALUES ('" + msg + "', 100)")
                        db.commit()
                else:
                        # Aumento confidenza se la risposta esiste già
                        try:
                                print("Risposta già esistente, aumento la confidenza.")
                                dupli_query = "UPDATE `" + inputmsg + "` SET confidenza = confidenza + 1 WHERE output LIKE '" + msg + "'"
                                cursor.execute(dupli_query)
                                db.commit()
                        except:
                                print("Non sono riuscito ad aumentare la confidenza della risposta '" + msg + "'")
                return "Me lo sono segnato, grazie."
        else:
                # Salvataggio ultimo input
                with open(sessiondir + "/ultimoinput", "w") as bufferinput:
                        bufferinput.write(msg)
                        bufferinput.flush()

        # Blocco di ricerca e risposta
        try:
                cursor.execute("SELECT output FROM `" + msg + "` ORDER BY confidenza DESC")
                result = cursor.fetchall()
                cursor.execute("SELECT confidenza FROM `" + msg + "` ORDER BY confidenza DESC")
                confidenze = cursor.fetchall()
                print(confidenze)
                print(result)
        except:
                result = False
        if not result:
                # Sperimentale: valuta la similarità con altre frasi
                query_similar = "SHOW TABLES"
                cursor.execute(query_similar)
                all_tables = cursor.fetchall()
                candidati = []
                similitudine = []
                for table in all_tables:
                    similarity = get_jaccard_sim(msg, table[0])
                    if similarity > 0.25:
                        candidati.append(table[0])
                        similitudine.append(similarity)
                print("La ricerca di similitudini ha trovato " + str(len(candidati)) + " candidati")
                if len(candidati) > 0:
                    # Per ora emette solo un candidato random 
                    # TODO: inserire pesi anche per i candidati
                    candidato_scelto = random.choice(candidati)
                    print("E' stato scelto " + candidato_scelto + " come miglior candidato")
                    cursor.execute("SELECT output FROM `" + candidato_scelto + "` ORDER BY confidenza DESC")
                    result = cursor.fetchall()
                    cursor.execute("SELECT confidenza FROM `" + candidato_scelto + "` ORDER BY confidenza DESC")
                    confidenze = cursor.fetchall()
                    print(confidenze)
                    print(result)
                else:
                    # Se proprio non trova niente, chiede
                    with open(sessiondir + "/previous", "w") as previous:
                            previous.write(msg)
                            previous.flush()
                    return "Non conosco questa frase. Come pensi che dovrei rispondere? (Per favore, scrivi solamente la frase che useresti per rispondere al tuo messaggio, senza aggiunte o perifrasi varie)"
        # Non uso l'else in modo da permettere all'eventuale similitudine di rientrare in questo if ugualmente. Eventuali not result non gestiti vengono nel prossimo else
        if result:
                # TODO: Far si che i pesi tengano conto del punteggio e non solo dell'ordine
                # ad esempio: il peso potrebbe derivare dai valori di punteggio /10
                # utilizzare la lista confidenze nel for per assegnare ad ogni frase
                # il peso confidenza/10 (le confidenze vengono passate con il for visto che sono nello
                # stesso ordine e numero
                resultweights = []
                resultstrings = []
                biggestweight = (len(result) + 1)*4
                totalweight = biggestweight
                for resvar in result:
                        resultweights.append(biggestweight)
                        biggestweight = biggestweight - (totalweight/len(result)) + 1
                        resultstrings.append(str(resvar))
                        print("Currentweight for " + str(resvar) + " is " + str(biggestweight))
                risposta = "".join(random.choices(resultstrings,weights=resultweights,k=1))
                risposta = risposta[2:-3]
                #risposta = "".join(random.choice(result))
                # Salvataggio ultimarisposta
                with open(sessiondir + "/ultimarisposta", "w") as ultimarisposta:
                        ultimarisposta.write(risposta)
                        ultimarisposta.flush()
                # Aggiornamento conversazione
                with open(sessiondir + "/conversazione", "a+") as conversazione:
                    conversazione.write("Bot: " + risposta + "\n")
                    conversazione.flush()
                return risposta
        else:
            return "Mi spiace, ho riscontrato un errore. Puoi riprovare?"

# Debugging
if __name__ == "__main__":
        if len(sys.argv) < 3:
                print("Devi specificare un parametro.")
        elif len(sys.argv) > 3:
                print("Devi specificare solamente un parametro.")
        else:
                print("Parametro: " + str(sys.argv[1]))
                print("ID : " + str(sys.argv[2]))
                print(digest(str(sys.argv[1]), str(sys.argv[2])))
