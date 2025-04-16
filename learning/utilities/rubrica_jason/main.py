import os
import json
from datetime import datetime

# Creare la directory contatti se non esiste
path_contatti = "contatti"
os.makedirs(path_contatti, exist_ok=True)

menu = {
    "1": "Visualizza i contatti attivi",
    "2": "Aggiungi",
    "3": "Modifica o elimina un contatto",
    "0": "Exit"
}

while True:
    # Visualizzazione del menu
    print(f"{'MENU':^40}")
    print("-" * 40)
    for number, option in menu.items():
        print(f"{number}: {option}")
    
    # Gestione della scelta dell'utente
    scelta_utente = input("Scegli l'operazione: ")
    if scelta_utente not in menu.keys():
        print("Scelta non valida. Premi 0, 1, 2 oppure 3")
        continue

    if scelta_utente == "1":  # Visualizza i contatti attivi
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            if len(os.listdir(path_contatti)) == 0:
                print("Rubrica telefonica vuota.")
            else:
                for contatto_file in os.listdir(path_contatti):
                    try:
                        path_contatto = os.path.join(path_contatti, contatto_file)
                        with open(path_contatto, "r", encoding='utf-8') as file:
                            obj = json.load(file)
                            if obj["attivo"]:
                                print(f"\nNome: {obj['nome']}")
                                print(f"Cognome: {obj['cognome']}")
                                for tel in obj['telefono']:
                                    print(f"Tipo: {tel['tipo']}, Numero: {tel['numero']}")
                                print(f"Attività: {', '.join(obj['attivita'])}")
                                print(f"Note: {obj['note']}")
                                print("-" * 40)
                    except Exception as e:
                        print(f"Errore leggendo il file {contatto_file}: {str(e)}")
        except Exception as e:
            print(f"Errore durante la visualizzazione: {str(e)}")

    elif scelta_utente == "2":  # Aggiungi un contatto
        try:
            # Input nome
            nuovo_nome = input("Inserisci il nome: ").strip().capitalize()
            while len(nuovo_nome) < 3:
                print("Il nome deve essere almeno di 3 caratteri.")
                nuovo_nome = input("Inserisci il nome: ").strip().capitalize()

            # Input cognome
            nuovo_cognome = input("Inserisci il cognome: ").strip().capitalize()
            while len(nuovo_cognome) < 3:
                print("Il cognome deve essere almeno di 3 caratteri.")
                nuovo_cognome = input("Inserisci il cognome: ").strip().capitalize()

            # Input telefono casa
            tel_tipo_casa = input("Numero telefono di casa: ").strip()
            while len(tel_tipo_casa) != 10 or not tel_tipo_casa.isdigit():
                print("Il numero di casa deve essere di 10 cifre numeriche")
                tel_tipo_casa = input("Numero telefono di casa: ").strip()

            # Input telefono cellulare
            tel_tipo_cel = input("Numero di cellulare: ").strip()
            while len(tel_tipo_cel) != 10 or not tel_tipo_cel.isdigit():
                print("Il numero di cellulare deve essere di 10 cifre numeriche")
                tel_tipo_cel = input("Numero di cellulare: ").strip()

            # Input stato attivo
            attivo_input = input("Sei attivo(a)? (si/no): ").strip().lower()
            while attivo_input not in ["si", "no"]:
                print("Rispondi con 'si' o 'no'")
                attivo_input = input("Sei attivo(a)? (si/no): ").strip().lower()
            attivo = attivo_input == "si"

            # Input attività
            attivita = []
            print("Inserisci le attività (lascia vuoto per terminare):")
            while True:
                att = input("Attività: ").strip().capitalize()
                if not att:
                    break
                attivita.append(att)

            # Input note
            note = input("Inserisci una nota: ").strip()

            # Creazione struttura dati
            contatto = {
                "nome": nuovo_nome,
                "cognome": nuovo_cognome,
                "telefono": [
                    {"tipo": "casa", "numero": tel_tipo_casa},
                    {"tipo": "cellulare", "numero": tel_tipo_cel}
                ],
                "attivo": attivo,
                "attivita": attivita,
                "note": note
            }

            # Salvataggio
            nome_file = f"{nuovo_nome}_{nuovo_cognome}.json".replace(" ", "_")
            percorso_completo = os.path.join(path_contatti, nome_file)
            
            with open(percorso_completo, "w", encoding='utf-8') as file:
                json.dump(contatto, file, indent=4, ensure_ascii=False)
            
            print(f"Contatto {nuovo_nome} {nuovo_cognome} salvato con successo!")
            
        except Exception as e:
            print(f"Errore durante l'aggiunta del contatto: {str(e)}")

    elif scelta_utente == "3":  # Modifica o elimina
        while True:
            try:
                # Menu modifica/elimina
                print("\nSottomenu:")
                print("1: Modifica contatto")
                print("2: Elimina contatto")
                print("0: Torna al menu principale")
                
                suboption = input("Scelta: ")
                if suboption == "0":
                    break
                if suboption not in ["1", "2"]:
                    print("Scelta non valida")
                    continue

                # Input ricerca
                nome_cercato = input("Inserisci il nome: ").strip().capitalize()
                while len(nome_cercato) < 3:
                    print("Il nome deve essere almeno di 3 caratteri.")
                    nome_cercato = input("Inserisci il nome: ").strip().capitalize()

                cognome_cercato = input("Inserisci il cognome: ").strip().capitalize()
                while len(cognome_cercato) < 3:
                    print("Il cognome deve essere almeno di 3 caratteri.")
                    cognome_cercato = input("Inserisci il cognome: ").strip().capitalize()

                # Verifica esistenza file
                nome_file = f"{nome_cercato}_{cognome_cercato}.json"
                percorso_file = os.path.join(path_contatti, nome_file)
                
                if not os.path.exists(percorso_file):
                    print("Contatto non trovato")
                    continue

                with open(percorso_file, "r", encoding='utf-8') as file:
                    contatto = json.load(file)

                if suboption == "1":  # Modifica
                    print("\nModifica contatto (lascia vuoto per mantenere il valore attuale):")
                    
                    # Modifica nome
                    nuovo_nome = input(f"Nome [{contatto['nome']}]: ").strip().capitalize() or contatto['nome']
                    while len(nuovo_nome) < 3:
                        print("Il nome deve essere almeno di 3 caratteri.")
                        nuovo_nome = input(f"Nome [{contatto['nome']}]: ").strip().capitalize() or contatto['nome']

                    # Modifica cognome
                    nuovo_cognome = input(f"Cognome [{contatto['cognome']}]: ").strip().capitalize() or contatto['cognome']
                    while len(nuovo_cognome) < 3:
                        print("Il cognome deve essere almeno di 3 caratteri.")
                        nuovo_cognome = input(f"Cognome [{contatto['cognome']}]: ").strip().capitalize() or contatto['cognome']

                    # Aggiorna dati
                    contatto['nome'] = nuovo_nome
                    contatto['cognome'] = nuovo_cognome

                    # Salva modifiche
                    nuovo_nome_file = f"{nuovo_nome}_{nuovo_cognome}.json"
                    nuovo_percorso = os.path.join(path_contatti, nuovo_nome_file)

                    if nuovo_nome_file != nome_file:
                        os.remove(percorso_file)

                    with open(nuovo_percorso, "w", encoding='utf-8') as file:
                        json.dump(contatto, file, indent=4, ensure_ascii=False)

                    print("Contatto modificato con successo!")

                elif suboption == "2":  # Elimina
                    conferma = input(f"Sei sicuro di voler eliminare {nome_cercato} {cognome_cercato}? (si/no): ").lower()
                    if conferma == "si":
                        os.remove(percorso_file)
                        print("Contatto eliminato con successo!")
                    else:
                        print("Operazione annullata")

            except Exception as e:
                print(f"Errore durante l'operazione: {str(e)}")

    elif scelta_utente == "0":  # Uscita
        print("Grazie per aver usato la rubrica telefonica!")
        break