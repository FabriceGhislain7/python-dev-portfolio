import os
import json
from datetime import datetime

# Creare una directory  
path_contatti = "contatti"  
os.makedirs(path_contatti, exist_ok=True)

menu = {"1": "Visualizza i contatti attivi",
        "2": "Aggiungi",
        "3": "Modifica o elimina un contatto",
        "0": "Exit."        
        }

while True:
    print(f"{'MENU':^40}\n{"-" * 40}")      # Visualizzazione del menu
    for number, option in menu.items():
        print(f"{number}: {option}")
    
    scelta_utente = input("Scegli l'operazione: ")      # Gestione della scelta dell'utente
    if not scelta_utente in menu.keys():
        print("Scelta non valida. Premi 0, 1, 2 oppure 3")
        continue

    match scelta_utente:
        case "1":       # Visualizzo i contatti attivi
            os.system('cls' if os.name == 'nt' else 'clear')
            if len(os.listdir(path_contatti)) == 0:
                print("Rubrica telefonica vuota.")
            else:
                for contatto in os.listdir(path_contatti):
                    path_contatto = os.path.join(path_contatti, contatto)
                    with open(path_contatto, "r", encoding='utf-8') as file:
                        obj = json.load(file)
                        if obj["attivo"]:
                            print(f"nome: {obj['nome']} \nCognome: {obj['cognome']}")
                            print(f"Tipo: {obj['telefono'][0]['tipo']}, Numero: {obj['telefono'][0]['numero']}")
                            print(f"Tipo: {obj['telefono'][1]['tipo']}, Numero: {obj['telefono'][1]['numero']}")
                            print(f"Attivo: {obj['attivo']}, Note: {obj['note']}")
                            print(f"Attività: {obj['attivita']}\n")
                        else:
                            pass
                    
        # Aggiungi un contatto
        case "2":        
            nuovo_nome = input("Inserisci il nome: ").strip().capitalize()
            while len(nuovo_nome) < 3:
                print("Il nome deve essere almeno di 3 caratteri.")
                nuovo_nome = input("Inserisci il nome: ").strip().capitalize()

            nuovo_cognome = input("Inserisci il cognome: ").strip().capitalize()
            while len(nuovo_cognome) < 3:
                print("Il cognome deve essere almeno di 3 caratteri.")
                nuovo_cognome = input("Inserisci il cognome: ").strip().capitalize()

            tel_tipo_casa = input("Numero telefono di casa: ").strip()
            while len(tel_tipo_casa) != 10 or not tel_tipo_casa.isdigit():
                print("Il numero di casa deve essere di 10 cifre numeriche")
                tel_tipo_casa = input("Numero telefono di casa: ").strip()

            tel_tipo_cel = input("Numero di cellulare: ").strip()
            while len(tel_tipo_cel) != 10 or not tel_tipo_cel.isdigit():
                print("Il numero di cellulare deve essere di 10 cifre numeriche")
                tel_tipo_cel = input("Numero di cellulare: ").strip()

            attivo_input = input("Sei attivo(a)? (si/no): ").strip().lower()
            while attivo_input not in ["si", "no"]:
                print("Rispondi con 'si' o 'no'")
                attivo_input = input("Sei attivo(a)? (si/no): ").strip().lower()
            attivo = True if attivo_input == "si" else False

            attivita_input = input("Inserisci la tua attività principale: ").strip().capitalize()
            attivita = [attivita_input] if attivita_input else []

            # Input note
            note = input("Inserisci una nota: ").strip()

            # Creazione struttura dati
            contatto = {
                "nome": nuovo_nome,
                "cognome": nuovo_cognome,
                "telefono": [
                    {
                        "tipo": "casa",
                        "numero": tel_tipo_casa
                    },
                    {
                        "tipo": "cellulare",
                        "numero": tel_tipo_cel
                    }
                ],
                "attivo": attivo,
                "attivita": attivita,
                "note": note
            }

            
            # Costruzione percorso completo per il salvataggio
            nome_file = f"{contatto['nome']}_{contatto['cognome']}.json".replace(" ", "_")
            percorso_completo = os.path.join(path_contatti, nome_file)

            # Salvataggio del contatto
            with open(percorso_completo, "w", encoding='utf-8') as file:
                json.dump(contatto, file, indent=4, ensure_ascii=False)  
            print(f"Contatto salvato in: {percorso_completo}")
            
        case "3": 

            while True:
                # Menu modifica/elimina
                suboption_user = input("1: Modifica contatto.\n2: Elimina contatto.\nScelta: ")
                if suboption_user not in ["1", "2"]:
                    print("Scelta non valida. Riprova.")
                    continue
                
                # Input ricerca contatto
                nome_cercato = input("Inserisci il nome da cercare: ").strip().capitalize()
                while len(nome_cercato) < 3:
                    print("Il nome deve essere almeno di 3 caratteri.")
                    nome_cercato = input("Inserisci il nome: ").strip().capitalize()

                cognome_cercato = input("Inserisci il cognome da cercare: ").strip().capitalize()
                while len(cognome_cercato) < 3:
                    print("Il cognome deve essere almeno di 3 caratteri.")
                    cognome_cercato = input("Inserisci il cognome: ").strip().capitalize()

                # Cerca il file
                nome_file = f"{nome_cercato}_{cognome_cercato}.json"
                percorso_file = os.path.join("contatti", nome_file)
                trovato = False

                if os.path.exists(percorso_file):
                    trovato = True
                    with open(percorso_file, "r", encoding='utf-8') as file:
                        contatto = json.load(file)
                else:
                    print("Contatto non trovato.")
                    continue

                if suboption_user == "1":
                    # MODIFICA CONTATTO
                    print("\nModifica contatto (lascia vuoto per mantenere il valore corrente):")
                    
                    # Nuovi valori con validazione
                    nuovo_nome = input(f"Nome [{contatto['nome']}]: ").strip().capitalize() or contatto['nome']
                    while len(nuovo_nome) < 3:
                        print("Il nome deve essere almeno di 3 caratteri.")
                        nuovo_nome = input(f"Nome [{contatto['nome']}]: ").strip().capitalize() or contatto['nome']

                    nuovo_cognome = input(f"Cognome [{contatto['cognome']}]: ").strip().capitalize() or contatto['cognome']
                    while len(nuovo_cognome) < 3:
                        print("Il cognome deve essere almeno di 3 caratteri.")
                        nuovo_cognome = input(f"Cognome [{contatto['cognome']}]: ").strip().capitalize() or contatto['cognome']

                    # Aggiorna il dizionario
                    contatto['nome'] = nuovo_nome
                    contatto['cognome'] = nuovo_cognome

                    # Salva le modifiche
                    nuovo_nome_file = f"{nuovo_nome}_{nuovo_cognome}.json"
                    nuovo_percorso = os.path.join("contatti", nuovo_nome_file)

                    # Se cambia nome/cognome, cancella il vecchio file
                    if nuovo_nome_file != nome_file:
                        os.remove(percorso_file)

                    with open(nuovo_percorso, "w", encoding='utf-8') as file:
                        json.dump(contatto, file, indent=4, ensure_ascii=False)

                    print("Contatto modificato con successo!")

                elif suboption_user == "2":
                    # ELIMINA CONTATTO
                    conferma = input(f"Sei sicuro di voler eliminare {nome_cercato} {cognome_cercato}? (si/no): ").lower()
                    if conferma == "si":
                        os.remove(percorso_file)
                        print("Contatto eliminato con successo!")
                    else:
                        print("Operazione annullata.")

                # Chiedi se vuoi fare altre operazioni
                altra_operazione = input("\nVuoi fare altre operazioni? (si/no): ").lower()
                if altra_operazione != "si":
                    break

        case "0":
            print("Hai deciso di uscire dalla rubrica")
            exit()

    

    