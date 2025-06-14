# Role Playing Game (RPG)
## Indice

- [**Obiettivo**](./README.md#obiettivo)
  - [Proposte didattiche per imparare OOP](./README.md#proposte-didattiche-per-imparare-oop)
---
- [**1. Ambienti**](./README.md#1-ambienti)
  - [Classe Ambiente](./README.md#classe-ambiente)
  - [Classe AmbienteFactory](./README.md#classe-ambientefactory)
  - [Classe Foresta(Ambiente)](./README.md#classe-forestaambiente)
  - [Classe Vulcano(Ambiente)](./README.md#classe-vulcanoambiente)
  - [Classe Palude(Ambiente)](./README.md#classe-paludeambiente)
---
- [**2. Missioni**](./README.md#2-missioni)
  - [Classe Missione](./README.md#classe-missione)
  - [Classe GestoreMissioni](./README.md#classe-gestoremissioni)
---
- [**3. Classe Giocatore (separata da Personaggio)** | In sviluppo](./README.md#3-classe-giocatore-separata-da-personaggio--in-sviluppo)
---
- [**4. Sistema Livello / Esperienza**](./README.md#4-sistema-livello--esperienza)
  - [Implementazione all'interno della Classe Personaggio](./README.md#implementazione-allinterno-della-classe-personaggio--enrico-t)
---
- [**5. Log**](./README.md#5-log)
  - [Classe Registro](./README.md#classe-registro)
---
- [**6. Salvataggio/Caricamento JSON** | In sviluppo](./README.md#6-salvataggiocaricamento-json--in-sviluppo)
---
- [**7. Patterns**](./README.md#7-patterns)
  - [Classe StrategiaAttacco](./README.md#classe-strategiaattacco--conrad)
  - [Classe Aggressiva](./README.md#classe-aggressiva--conrad)
  - [Classe Difensiva](./README.md#classe-difensiva--conrad)
  - [Classe Equilibrata](./README.md#classe-equilibrata--conrad)
  - [Classe StrategiaAttaccoFactory](./README.md#classe-strategiaattaccofactory--conrad)
---
- [**8. Effetti** | In sviluppo](./README.md#8-effetti--in-sviluppo)
---
- [**Classi base - Documentazione generale**](./README.md#classi-base---documentazione-generale)
  - [Classe Personaggio](./README.md#classe-personaggio)
  - [Classe Mago](./README.md#classe-mago)
  - [Classe Guerriero](./README.md#classe-guerriero)
  - [Classe Ladro](./README.md#classe-ladro)
  - [Classe Inventario](./README.md#classe-inventario)
  - [Classe Oggetto](./README.md#classe-oggetto)
  - [Classe PozioneCura](./README.md#classe-pozionecura)
  - [Classe BombaAcida](./README.md#classe-bombaacida)
  - [Classe Medaglione](./README.md#classe-medaglione)
  - [Classe InterfacciaUtente](./README.md#classe-interfacciautente)
---
- [**Teamwork**](./README.md#teamwork)
---
- [**Modalità di sviluppo**](./README.md#modalità-di-sviluppo)
---
- [**Implementazioni Team 1**](./README.md#team-1)
  - [Esecuzione Classe Ambiente](./README.md#1-esecuzione-classe-ambiente)
  - [Esecuzione Classe Strategia_attacco](./README.md#2-esecuzione-classe-strategiaattacco)
  - [Aggiunta della documentazione usando Sphinx](./README.md#3-aggiunta-della-documentazione-usando-sphinx)
---
- [**Implementazioni Team 2**](./README.md#team-2)
  - [Piccoli fix e semplificazioni d'uso](./README.md#1-piccoli-fix-e-semplificazioni-duso)
  - [Creazione classi Missioni e GestoreMissioni](./README.md#2-creazione-classi-missioni-e-gestoremissioni)
  - [Fix classe Missione e metodi aggiornati](./README.md#3-fix-classe-missione-e-metodi-aggiornati)
  - [Implementazioni alla classe GestoreMissioni](./README.md#4-implementazioni-alla-classe-gestoremissioni)
---

# Obiettivo
- espandere un progetto con nuove responsabilità, entità chiare e interazioni tra classi
- imparare le tecniche di versionamento e gestione del codice sorgente
- imparare a scrivere codice in ambiente condiviso in moduli, facilmente testabile e manutenibile, estendibile, riutilizzabile, chiaro e ben documentato
- imparare a creare un applicazione in modo modulare, con classi e metodi ben definiti con documentazione chiara e precisa
- imparare a usare GitHub per la gestione del codice sorgente e il versionamento
- imparare la gestione di un progetto in team, con responsabilità e ruoli definiti

**Approfondire i seguenti argomenti:**
- Incapsulamento
- Responsabilità delle classi
- Ereditarietà
- Polimorfismo
- Composizione

## Proposte didattiche per imparare OOP (Object Oriented Programming)
- Classe Ambiente – è semplice, utile, immediata
- Classe Missione – organizza tutto e ti abitua a gestire moduli
- Livello / Esperienza – cominci ad astrarre la crescita
- Log e salvataggio – utile per debugging e salvataggio futuro

---

# 1. Ambienti

### Questa classe serve ad alterare dei valori globali nel corso del gioco. Interagisce con Personaggio e Oggetto. influenza combattimento, oggetti, abilità
> Nelle classi derivate Foresta, Vulcano e Palude, si farà uso di `isinstance()`, che serve a verificare se un oggetto è un'istanza (o sottoclasse) di una o più classi specificate

```python

class Ambiente:
    def __init__(self, nome, modifica_attacco=0, modifica_cura=0):
        self.nome = nome
        self.modifica_attacco = modifica_attacco
        self.modifica_cura = modifica_cura

    def modifica_danno(self, attaccante: Personaggio, attaccato: Personaggio):
        raise NotImplementedError("Questo oggetto non ha effetto definito.")

    def modifica_effetto_oggetto(self, oggetto: Oggetto):
        raise NotImplementedError("Questo oggetto non ha effetto definito.")

    def mod_cura(self, soggetto: Personaggio):
        raise NotImplementedError("Questo oggetto non ha effetto definito.")

```

## Classe AmbienteFactory
### Questa classe gestisce la creazione degli ambienti

```python

class AmbienteFactory:
    @staticmethod
    def sorteggia_ambiente():
        ambienti_possibili = [Foresta(), Vulcano(), Palude()]
        ambiente = random.choice(ambienti_possibili)
        print(f"\nAmbiente Casuale Selezionato: {ambiente.nome}")
        return ambiente

    @staticmethod
    def seleziona_ambiente():
        opzioni = {
            "1" : Foresta(),
            "2" : Vulcano(),
            "3" : Palude()
        }
        print("\nScegli un ambiente: ")

        for numero, ambiente in opzioni.items():
            print(f"{numero}) {ambiente.nome}")

        scelta = input("Inserisci il numero dell'ambiente (1-3): ").strip()

        if scelta in opzioni:
            ambiente = opzioni[scelta]
            print(f"Hai scelto: {ambiente.nome}")
            return ambiente
        else:
            print("Sceglia non valida. Ambiente predefinito: Foresta.")
            return Foresta()

```

Metodo | Dettagli
--- | ---
sorteggia_ambiente() | Genera un ambiente casuale tra i 3 disponibili. Ritorna l'oggetto 'ambiente'
seleziona_ambiente() | Prende un input utente

### Classe figlia di Ambiente. Rappresenta un ambiente specifico con modificatori ad attacco dei guerrieri e alla cura di fine turno dei ladri.

```python

class Foresta(Ambiente):
    def __init__(self):
        super().__init__(nome="Foresta", modifica_attacco=5, modifica_cura=5)

    def modifica_attacco_max(self, attaccante: Personaggio, attaccato: Personaggio):
        if isinstance(attaccante, Guerriero):
            print(f"{attaccante.nome} guadagna {self.modifica_attacco} attacco nella {self.nome}!")
            return self.modifica_attacco
        else:
            return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto):
        return 0

    def mod_cura(self, soggetto: Personaggio):
        if isinstance(soggetto, Ladro):
            return self.modifica_cura
        else:
            return 0

```

Metodo | Dettagli
--- | ---
modifica_attacco_max() | Richiede 2 input (Attaccante e Attaccato). Entrambi devono essere type Personaggio. Aumenta attacco massimo dell'attaccante.
modifica_effetto_oggetto() | |
mod_cura() | Richiede 1 input (Attaccante e Attaccato). Altera la cura a fine turno del ladro

### Classe figlia di Ambiente. Rappresenta un ambiente specifico con modificatori ad attacco dei maghi e dei ladri, un incremento random dei danni delle bombe acide e incremento random per chiunque alla cura di fine turno

```python

class Vulcano(Ambiente):
    def __init__(self):
        super().__init__(nome="Vulcano", modifica_attacco=10, modifica_cura=-5)

    def modifica_attacco_max(self, attaccante: Personaggio, attaccato: Personaggio):
        if isinstance(attaccante, Mago):
            print(f"{attaccante.nome} guadagna {self.modifica_attacco} attacco nella {self.nome}!")
            return self.modifica_attacco
        elif isinstance(attaccante, Ladro):
            print(f"{attaccante.nome} perde {self.modifica_attacco} attacco nella {self.nome}!")
            malus = -self.modifica_attacco
            return malus
        else:
            return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto):
        if isinstance(oggetto, BombaAcida):
            variazione = random.randint(0, 15)
            print(f"{oggetto.nome} guadagna {variazione} danni nel {self.nome}!")
            return variazione
        else:
            return 0

    def mod_cura(self, soggetto: Personaggio):
        return self.modifica_cura

```

Metodo | Dettagli
--- | ---
modifica_attacco_max() | Aumenta l'attacco massimo del mago e diminuisce quello del ladro
modifica_effetto_oggetto() | Aumenta il danno della bomba acida (valore casuale 0-15)
mod_cura() | Aumenta l'ammontare della cura per tutte le classi

### Classe figlia di Ambiente. Rappresenta un ambiente specifico con modificatori ad attacco di gurerrieri e ladri. Viene inoltre diminuita l'efficienza delle pozioni curative

```python

class Palude(Ambiente):
    def __init__(self):
        super().__init__(nome="Palude", modifica_attacco=-5, modifica_cura=0.3)

    def modifica_attacco_max(self, attaccante: Personaggio):
        # Se l'attaccante è un Guerriero o un Ladro, applica il malus all'attacco
        if isinstance(attaccante, (Guerriero, Ladro)):
            print(f"{attaccante.nome} perde {-self.modifica_attacco} attacco nella {self.nome}!")
            # Applica il malus come un bonus negativo
            return self.modifica_attacco

        else:
            # Altri personaggi attaccano normalmente
            return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto):
        # Se l'oggetto è una Pozione Cura, riduce l'efetto del %30
        if isinstance(oggetto, PozioneCura):
            # Calcola la riduzione come %30 della quantita curata
            riduzione = int(oggetto.valore * self.modifica_cura)
            print(f"Nella {self.nome}, la pozione cura {riduzione} in meno! ")
            return -riduzione
        else:
            # Altri oggetti non subiscono modifiche
            return 0

    def mod_cura(self, soggetto: Personaggio):
        return 0


```

Metodo | Dettagli
--- | ---
modifica_attacco_max() | Diminuisce l'attacco massimo della classe Guerriero e Ladro
modifica_effetto_oggetto() | In Palude, diminuisce l'efficienza della pozione curativa del 30%
mod_cura() | Permette di recuperare salute

> argomenti didattici:
**l’uso della composizione e della configurabilità**

---

# 2. Missioni

### Questa classe gestisce l'esistenza e lo svolgimento di una missione

```python

class Missione:
    def __init__(self, nome, ambiente, nemici, premi):

        # inizializzazione attributi
        self.nome = nome
        self.ambiente = ambiente  # ereditato dal torneo corrente
        self.nemici = nemici  # lista dei nemici di tutti i tornei
        self.premi = premi  # supporta premio singolo o multiplo
        self.completata = False  # flag per premio in inventario

    def rimuovi_nemico(self, nemico):
        self.nemici.remove(nemico)

    def rimuovi_nemici_sonfitti(self):
        #Metto in una lista i nemici sconfitti che devo rinuovere
        lista_to_remove = []
        for nemico in self.nemici:
            if nemico.sconfitto():
                lista_to_remove.append(nemico)
        #Rimuovo i nemici sconfitti dalla proprietà nemici 
        for nemico in lista_to_remove:
            print(f"{nemico.nome} rimosso da {self.nome}")
            self.rimuovi_nemico(nemico)

    # controlla se la lista self.nemici è vuota e nel caso restituisce True
    def verifica_completamento(self):
        n_nemici_sconfitti = 0
        for nemico in self.nemici:
            if nemico.sconfitto():
                n_nemici_sconfitti += 1
            if n_nemici_sconfitti == len(self.nemici):
                self.completata = True
                print(f"Missione '{self.nome}' completata")
                return True
        return False

    # aggiunge premio all'inventario del giocatore se la missione è completata
    def assegna_premio(self, giocatore, inventario):
        for premio in self.premi:
            inventario.aggiungi(premio)
            print(f"Premio {premio.nome} aggiunto all'inventario di {giocatore.nome}")

    #QUESTO METODO E' PROVVISORIO
    def check_missione(self, giocatore_vincitore):
        self.rimuovi_nemici_sonfitti()
        if self.verifica_completamento():
            self.assegna_premio(giocatore_vincitore)

```

Metodo | Dettagli
--- | ---
rimuovi_nemico() | Rimuove il nemico designato dalla lista di nemici della missione
rimuovi_nemici_sconfitti() | Verifica se nella lista dei nemici ci sono nemici sconfitti e nel caso li rimuove tramite il metodo rimuovi_nemico()
verifica_completamento() | Serve per verifica sulla lista dei nemici: se vuota > True, altrimenti False
assegna_premio() | Assegna il premio (o i premi) all'inventario del giocatore
check_missione() | Metodo che viene utilizzato dopo ogni attacco del giocatore ai nemici. Tramite utilizzo dei metodi sopracitati, rimuove nemici sconfitti, verifica il completamento missione e assegna il premio

### Gestisce tramite i metodi sottocitati le istanze create a partire dalla classe Missioni

```python

class GestoreMissioni:
    def __init__(self):
        #La proprietà principale di Missioni sarà una lista di oggetti Missione
        self.lista_missioni = self.setup()

    def setup(self):
         #Istanzio le missioni
        imboscata = Missione("Imboscata", Foresta(), [Guerriero("Robin Hood"), Guerriero("Little Jhon")], [PozioneCura(),PozioneCura(),BombaAcida()])
        salva_principessa = Missione("Salva la principessa", Palude(),[Ladro("Megera furfante")],[Medaglione()])
        culto = Missione("Sgomina il culto di Graz'zt sul vulcano Gheemir", Vulcano(),[Mago("Cultista"), Mago("Cultista"), Mago("Cultista")],[PozioneCura(),Medaglione()])
        return [imboscata, salva_principessa, culto]

    def mostra(self):
        print("Missioni disponibili:")
        for missione in self.lista_missioni:
            print(f"-{missione.nome}")
        #print(f"-{indx}  {missione.nome}" for indx, missione in enumerate(self.lista_missioni, start=1) if not missione.completata)

    def finita(self):
        esito = True
        for missione in self.lista_missioni :
            if missione.completata == False :
                esito = False
        return esito

    def sorteggia(self):
        random.shuffle(self.lista_missioni)
        for missione in self.lista_missioni :
            if not missione.completata :
                return missione
        #Se non ci sono missioni che non siano state completate
        return False

```

Metodo | Dettagli
--- | ---
setup() | TODO (!)
mostra() | Serve a mostrare le missioni disponibili per essere giocate
finita() | Se ci sono ancora missioni non completate > ritorna False. Se sono state tutte completate > True
sorteggia() | Sorteggia missione a caso tra quelle non completate. In caso non ci fossero ritorna False

> argomenti didattici:
**l’aggregazione (missione = ambiente + nemici + oggetti) e a gestire scenari modulari**

---

# 3. Classe Giocatore (separata da Personaggio) | In sviluppo
Così puoi avere più giocatori che usano personaggi, scelgono oggetti, gestiscono punteggi ecc.

```python
class Giocatore:
    def __init__(self, nome, personaggio):
        self.nome = nome
        self.personaggio = personaggio
        self.punteggio = 0
```
> argomenti didattici:
**l’associazione tra oggetti e separazione tra “logica del giocatore” e “logica del combattente”**

---

# 4. Sistema Livello / Esperienza
Il sistema aggiunge punti esperienza al personaggio per ogni nemico sconfitto, facendolo salire di livello e migliorando le sue statistiche.

## Implementazione all'interno della Classe Personaggio

*dalla classe `Personaggio` ([vedi classe](./README.md#classe-personaggio))*
```python

    def migliora_statistiche(self) -> None:
        self.livello += 1
        self.attacco_max += 0.02 * self.attacco_max
        self.salute_max += 0.01 * self.salute_max
        print(f"{self.nome} è salito al livello {self.livello}!")

```

Metodo | Dettagli
--- | ---
migliora_statitiche() | aumenta il livello di 1. ogni aumento di livello garantisce un aumento dell'attacco massimo e della salute massima

> argomenti didattici:
**incapsulamento del comportamento e gestione dello stato interno**

---

# 5. Log

## Classe Registro
### La classe `Registro` è utile alla registrazione di ogni evento significativo che potrebbe accadere durante l'esecuzione del gioco. Ogni azione viene salvata in una lista o file: chi ha attaccato, quanto danno, quale oggetto usato…

```python

from datetime import datetime  # import di datetime per registrazione eventi
class Registro:
    @staticmethod
    def scrivi_log(messaggio):
        """
        Registra un messaggio con timestamp direttamente nel file log.txt.
        """
        with open("log.txt", "a", encoding="utf-8") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {messaggio}\n")
    @staticmethod
    def mostra_log():
        with open("log.txt", "r", encoding="utf-8") as file:
            print(file.read())

```

**Esempio di creazione del file log.txt (e sua cancellazione):**

```python

def setup(self):
        # elimina il file di log esistente
        with open("log.txt", "w", encoding="utf-8") as file:
            file.write("")

```

**Esempio di utilizzo:**

- Viene importato il modulo Registro dove viene utilizzato
- Viene inizializzato un oggetto Registro
```python
from utils.log import Log
```

- Viene registrato un evento quando il nemico viene sconfitto
```python
if self.nemico.sconfitto():
    evento = f"Hai vinto contro {self.nemico.nome}!"
    print(evento)
    Registro.scrivi_log(evento)
```

- Il messaggio verrà passato alla funzione scrivi_log
```python
    def scrivi_log(messaggio):
        with open("log.txt", "a", encoding="utf-8") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {messaggio}\n")
```

- Il file uscirà così:
```txt
2023-07-07 10:00:00 - Il nemico é stato sconfitto!
```

> argomenti didattici:
**Strumento per raccogliere eventi, essenziale in pressoché qualsiasi software, utile per debug, replay o salvataggi**

@staticmethod | Dettagli
--- | ---
scrivi_log() | imprint di un messaggio con timestamp su file log.txt
mostra_log() | legge il file e stampa gli eventi registrati

---

# 6. Salvataggio/Caricamento JSON | In sviluppo
Salvi Missioni, Giocatore, Inventari, ecc. in file .json e li ricarichi.
- Creazione di una classe con metodi statici per caricare e salvare oggetti
- Uso di json.dumps e json.loads per serializzare e deserializzare oggetti
- Esempio di classe per il salvataggio e il caricamento
```python
import json
class Json:
    @staticmethod
    def encoder(obj):
        """
        Input: obj (oggetto): L'oggetto da serializzare in JSON.
        Output: str: La rappresentazione JSON dell'oggetto.
        """
        if hasattr(obj, '__dict__'):
            return obj.__dict__.copy() 
        return str(obj)

    @staticmethod
    def scrivi_dati(file_path, dati_da_salvare, encoder=encoder):
        """
        Scrive i dati in un file JSON.
        input: file_path (str): Il percorso del file in cui salvare i dati.
               dati_da_salvare (dict): I dati da salvare nel file.
        output: Nessuno
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(dati_da_salvare, file, indent=4, default=encoder)
            print(f"Dati scritti con successo in {file_path}")
        except Exception as e:
            print(f"Errore nella scrittura del file JSON: {e}")

```
## Funzione di caricamento
```python
    @staticmethod
    def carica_dati(file_path):
        """
        Carica i dati da un file JSON specificato.

        Argomenti:
            file_path (str): Percorso del file da cui caricare i dati.

        Restituisce:
            dict: Dati caricati dal file JSON.
        """
        try:
            with open(file_path, 'r') as file:
                dati = json.load(file)
            return dati
        except Exception as e:
            print(f"Errore nella lettura del file JSON: {e}")
            return None
```
Quando si vuole salvare un oggetto, basta chiamare il metodo `scrivi_dati` e passargli il percorso del file e l'oggetto da salvare:
```python
Json.scrivi_dati(json_file_path, giocatore)
```
Quando si vuole caricare un oggetto, basta chiamare il metodo `carica_dati` e passargli il percorso del file:
```python
dati = Json.carica_dati(json_file_path)
```
> argomenti didattici:
**a usare i metodi statici, gestire oggetti serializzabili, salvare stati complessi**

---

# 7. Patterns

## Classe StrategiaAttacco
### Classe di base da cui viene derivata ogni strategia di attacco. Con questa classe si vogliono andare a modificare le decisioni dei personaggi durante il loro turno di gioco

```python

class StrategiaAttacco:
    def __init__(self, nome: str = "Strategia di attacco"):
        self.nome = nome

    @staticmethod
    def esegui_attacco(nemico: Personaggio, bersaglio: Personaggio):
        '''
        input: nemico: Personaggio, bersaglio: Personaggio
        output: None
        viene definito un metodo astratto che deve essere implementato
        dalle classi derivate.
        '''
        raise NotImplementedError(
            "Devi implementare il metodo esegui nella sottoclasse"
        )

```

@staticmethod | Dettagli
--- | ---
esegui_attacco() | Metodo astratto da derivare nelle classi figlie

## Classe Aggressiva
### La classe `Aggressiva` imposta un tipo di strategia in cui la priorità è sottrarre la maggior quantità possibile di salute dal nemico

```python

class Aggressiva(StrategiaAttacco):
    def __init__(self):
        super().__init__(nome="Aggressiva")

    @staticmethod
    def esegui_attacco(
        nemico: Personaggio,
        bersaglio: Personaggio,
        inventario: Inventario
    ):
        Log.scrivi_log(
            f"{nemico} attacca {bersaglio.nome} con un attacco aggressivo!"
        )
        if inventario.oggetti:
            for oggetto in inventario.oggetti:
                if oggetto.nome == "Bomba Acida":
                    inventario.usa_oggetto(
                        "Bomba Acida",
                        utilizzatore=nemico,
                        bersaglio=bersaglio
                    )
                    break
        nemico.attacca(bersaglio)

```

@staticmethod | Dettagli
--- | ---
esegui_attacco() | Permette l'esecuzione di un attacco di tipo aggressivo: se disponibili, verranno usati solamente oggetti di tipo BombaAcida (attualmente l'unico oggetto che danneggia la salute)

## Classe Difensiva
### La classe `Difensiva` imposta un tipo di strategia in cui, se la salute scende sotto i 60 punti, la priorità è curarsi.

```python

class Difensiva(StrategiaAttacco):
    def __init__(self):
        super().__init__(nome="Difensiva")

    @staticmethod
    def esegui_attacco(
        nemico: Personaggio,
        bersaglio: Personaggio,
        inventario: Inventario
    ):
        Log.scrivi_log(
            f"{nemico.nome} attacca {bersaglio.nome} con un attacco difensivo!"
        )

        if nemico.salute < 60 and inventario and inventario.oggetti:
            if next(
                (
                    ogg for ogg in inventario.oggetti
                    if ogg.nome == "Pozione Rossa"
                ),
                None
            ):
                if (random.randint(0, 1) == 0):
                    inventario.usa_oggetto("Pozione Rossa", nemico)
        nemico.attacca(bersaglio)

```

@staticmethod | Dettagli
--- | ---
esegui_attacco() | Esegue l'attacco difensivo: se la salute scende sotto i 60 punti, si ha la probabilità del 50% di usare un oggetto curativo, altrimenti si limita ad attaccare

## Classe Equilibrata
### La classe `Equilibrata` imposta un tipo di strategia bilanciato in cui si cerca di trovare un equilibrio tra utilizzo di oggetti curativi e offensivi

```python

class Equilibrata(StrategiaAttacco):
    def __init__(self):
        super().__init__(nome="Equilibrata")

    @staticmethod
    def esegui_attacco(
        nemico: Personaggio,
        bersaglio: Personaggio,
        inventario: Inventario
    ):
        Log.scrivi_log(
            f"{nemico.nome} attacca {bersaglio.nome} "
            "con un attacco equilibrato!"
        )
        if nemico.salute < 40:
            if inventario and inventario.oggetti:
                if next(
                    (
                        ogg for ogg in inventario.oggetti
                        if ogg.nome == "Pozione Rossa"
                    ),
                    None
                ):
                    if (random.randint(0, 2) == 0):
                        inventario.usa_oggetto("Pozione Rossa", nemico)
        elif inventario and inventario.oggetti:
            if next(
                (
                    ogg for ogg in inventario.oggetti
                    if ogg.nome == "Bomba Acida"
                ),
                None
            ):
                if (random.randint(0, 2) == 0):
                    inventario.usa_oggetto(
                        "Bomba Acida",
                        utilizzatore=nemico,
                        bersaglio=bersaglio
                    )
        nemico.attacca(bersaglio)

```

@staticmethod | Dettagli
--- | ---
esegui_attacco() | Se la salute risulta sotto i 40 punti, viene utilizzata un oggetto curativo (*Pozione Rossa*), altrimenti ci si focalizza sull'offensività utilizzando un oggetto offensivo (*Bomba Acida*). Gli oggetti vengono usati in modo randomico (probabilità 33% cad.)

## Classe StrategiaAttaccoFactory
### È una classe *factory* deputata a creare istanze di classi derivate da StrategiaAttacco in base alla richiesta

```python

class StrategiaAttaccoFactory:
    @staticmethod
    def strategia_random():
        random_choice = random.choice(
            ["aggressiva", "difensiva", "equilibrata"]
        )
        return StrategiaAttaccoFactory.usa_strategia(random_choice)

    @staticmethod
    def usa_strategia(tipo: str) -> StrategiaAttacco:
        tipo = tipo.lower()
        if tipo == "aggressiva":
            return Aggressiva()
        elif tipo == "difensiva":
            return Difensiva()
        elif tipo == "equilibrata":
            return Equilibrata()
        else:
            raise ValueError(f"Tipo di strategia sconosciuto: {tipo}")

```

@staticmethod | Dettagli
--- | ---
strategia_random() | Sceglie una strategia casuale
usa_strategia() | Restituisce l'istanza del tipo specificato come argomento

> argomenti didattici:
**il concetto di comportamento intercambiabile, un design pattern reale**

---

# 8. Effetti | In sviluppo
- classe incaricata di gestire effetti che modificano l'andamento dei turni o le dinamiche di gioco

- Esempio di classe per gestire effetti temporanei
```python
class Effetto:
    def __init__(self, nome, durata, effetto):
        self.nome = nome
        self.durata = durata
        self.effetto = effetto

    def applica(self, personaggio):
        # Applica l'effetto al personaggio
        pass

    def scade(self):
        # Gestisce la scadenza dell'effetto
        pass
```
> argomenti didattici:
**la gestione dello Stato: Gli effetti possono alterare temporaneamente lo stato dei personaggi o dell'ambiente, insegnandoti a gestire stati complessi e transitori nel tuo sistema**
**Composizione e Modularità: Separando gli effetti in una classe dedicata, promuovi la composizione rispetto all'ereditarietà**

---

# Classi base - Documentazione generale

## Classe Personaggio

```python

class Personaggio:
    def __init__(self, nome):
        self.nome = nome
        self.salute = 100
        self.salute_max = 200
        self.attacco_min = 5
        self.attacco_max = 80
        self.storico_danni_subiti = []

    def attacca(self, bersaglio, mod_ambiente=0):
        danno = random.randint(self.attacco_min, (self.attacco_max + mod_ambiente))
        print(f"{self.nome} attacca {bersaglio.nome} per {danno} punti!")
        bersaglio.subisci_danno(danno)

    def subisci_danno(self, danno):
        self.salute = max(0, self.salute - danno)
        self.storico_danni_subiti.append(danno)
        print(f"Salute di {self.nome}: {self.salute}\n")

    def sconfitto(self):
        return self.salute <= 0

    def recupera_salute(self, mod_ambiente=0):
        if self.salute == 100:
            print(f"{self.nome} ha già la salute piena.")
            return
        recupero = int(self.salute * 0.3) + mod_ambiente
        nuova_salute = min(self.salute + recupero, 100)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        print(f"\n{self.nome} recupera {effettivo} HP. Salute attuale: {self.salute}")

    def migliora_statistiche(self) -> None:
        self.livello += 1
        self.attacco_max += 0.02 * self.attacco_max
        self.salute_max += 0.01 * self.salute_max
        print(f"{self.nome} è salito al livello {self.livello}!")

```

Metodo | Dettagli
--- | ---
attacca() | Nella classi derivate da Personaggio viene fatto sempre l'override di questo metodo
subisci_danno() | Prende il danno come input e lo sottrae alla salute del personaggio colpito
sconfitto() | Controlla se il personaggio è stato sconfitto (ovvero ha salute minore o uguale a 0)
recupera_salute() | Utilizzato per incrementare la salute del personaggio (tramite pozioni, rigenerazione etc.)
migliora_statitiche() | aumenta il livello di 1. ogni aumento di livello garantisce un aumento dell'attacco massimo e della salute massima ([vedi Sistema Livello/Esperienza](./README.md#4-sistema-livello--esperienza))


## Classe Mago
### Estensione della classe Personaggio, salute modificata a `80` - override del metodo `attacca()` e `recupera_salute()`

```python

class Mago(Personaggio):
    def __init__(self, nome):
        super().__init__(nome)
        self.salute = 80

    def attacca(self, bersaglio):
        danno = random.randint(self.attacco_min - 5, self.attacco_max + 10)
        print(f"{self.nome} lancia un incantesimo su {bersaglio.nome} per {danno} danni!")
        bersaglio.subisci_danno(danno)

    def recupera_salute(self, mod_ambiente=0):
        recupero = int((self.salute + mod_ambiente)* 0.2)
        self.salute = min(self.salute + recupero, 80)
        print(f"\n{self.nome} medita e recupera {recupero} HP. Salute attuale: {self.salute}")

```

Metodo | Dettagli
--- | ---
attacca() | Il mago ha attacco minimo diminuito di 5 e un attacco massimo aumentato di 10
recupera_salute() | Il mago recupera il 20% di (salute + modificatore ambiente corrente) alla fine di ogni duello

## Classe Guerriero
### Estenzione della classe Personaggio, salute modificata a `120` - override del metodo `attacca()` e `recupera_salute()`

```python

class Guerriero(Personaggio):
    def __init__(self, nome):
        super().__init__(nome)
        self.salute = 120

    def attacca(self, bersaglio, mod_ambiente=0):
        danno = random.randint(self.attacco_min + 15, (self.attacco_max + mod_ambiente + 20))
        print(f"{self.nome} colpisce con la spada {bersaglio.nome} per {danno} danni!")
        bersaglio.subisci_danno(danno)

    def recupera_salute(self, mod_ambiente=0):
        recupero = 30 + mod_ambiente
        self.salute = min(self.salute + recupero, 120)
        print(f"\n{self.nome} si fascia le ferite e recupera {recupero} HP. Salute attuale: {self.salute}")

```

Metodo | Dettagli
--- | ---
attacca() | Il guerriero ha un attacco minimo aumentato di 15, un attacco massimo aumentato di 20 + il modificatore dell'ambiente corrente
recupera_salute() | Il guerriero recupera 30 punti salute alla fine di ogni duello

## Classe Ladro
### Estensione della classe Personaggio, salute modificata a `140` - override del metodo `attacca()` e `recupera_salute()`

```python

class Ladro(Personaggio):
    def __init__(self, nome):
        super().__init__(nome)
        self.salute = 140

    def attacca(self, bersaglio):
        danno = random.randint(self.attacco_min + 5, self.attacco_max + 5)
        print(f"{self.nome} colpisce furtivamente {bersaglio.nome} per {danno} danni!")
        bersaglio.subisci_danno(danno)

    def recupera_salute(self, mod_ambiente=0):
        recupero = random.randint(10, 40) + mod_ambiente
        self.salute = min(self.salute + recupero, 140)
        print(f"\n{self.nome} si cura rapidamente e recupera {recupero} HP. Salute attuale: {self.salute}")

```

Metodo | Dettagli
--- | ---
attacca() | Il ladro ha un attacco minimo aumentato di 5 e un attacco massimo aumentato di 5
recupera_salute() | Il ladro recupera un numero casuale di punti salute tra 10 e 40 + il modificatore dell'ambiente corrente

## Classe Inventario
### Gestisce la lista degli oggetti posseduti da ogni personaggio

```python

class Inventario:
    def __init__(self):
        self.oggetti = []

    def aggiungi(self, oggetto):
        self.oggetti.append(oggetto)

    def usa_oggetto(self, nome_oggetto, utilizzatore, bersaglio=None):
        for oggetto in self.oggetti:
            if oggetto.nome == nome_oggetto:
                oggetto.usa(utilizzatore, bersaglio)
                self.oggetti.remove(oggetto)
                return
        print(f"{utilizzatore.nome} non ha un oggetto chiamato {nome_oggetto}.")

    def mostra(self):
        print("Inventario :")
        for oggetto in self.oggetti :
            print(f"-{oggetto.nome}")

    def riversa(self, da_inventario, personaggio_utizzatore=None):
        if len(da_inventario.oggetti) != 0 :
            if personaggio_utizzatore == None:
                print(f"Inseriti nell'inventario : ")
            else:
                print(f"{personaggio_utizzatore.nome} raccoglie :")
            for oggetto in da_inventario.oggetti :
                print(f" - {oggetto.nome}")
                self.aggiungi(oggetto)
            da_inventario.oggetti.clear()
        else:
            print(f"{da_inventario.nome} è vuoto.")

```

Metodo | Dettagli
--- | ---
aggiungi() | Aggiunge uno specifico oggetto all'inventario
usa_oggetto() | Viene eseguito l'override di questo metodo da parte di ogni classe derivata da Oggetto
mostra() | Restituisce il contenuto dell'inventario
riversa() | Alla fine di un duello, il sopravvissuto si appopria dell'inventario del personaggio sconfitto aggiungendolo al suo. L'utilità del parametro `personaggio_utilizzatore` è limitata alla stampa

## Classe Oggetto
### Classe padre di tutti gli oggetti contenibili nell'inventario. L'oggetto essenziale deve avere un nome, un tipo e un'offensività (True/False)

```python

class Oggetto:
    def __init__(self, nome,tipo, offensivo = False):
        self.nome = nome
        self.tipo = tipo
        self.usato = False
        #La proprietà bersaglio specifica se l'oggetto va usato contro un nemico
        #o su se stesso (La bomba avrà bersaglio=True, la Pozione Rossa False)
        self.offensivo = offensivo

    def usa(self, utilizzatore, bersaglio=None, ambiente=None):
        raise NotImplementedError("Questo oggetto non ha effetto definito.")

```

Metodo | Dettagli
--- | ---
usa() | Viene implementato in ogni derivata di Oggetto

## Classe PozioneCura(Oggetto)
### Questo oggetto consente all'utilizzatore di recuperare eventuale salute persa in combattimento (ammontare salute da recuperare specificato in `valore`)

```python

class PozioneCura(Oggetto):
    def __init__(self, nome="Pozione Rossa", tipo="Cura", valore=30):
        super().__init__(nome,tipo)
        self.valore = valore

    def usa(self, utilizzatore, bersaglio=None, ambiente=None):
        target = bersaglio if bersaglio else utilizzatore
        target.salute = min(target.salute + self.valore, target.salute_max)
        print(f"{target.nome} usa {self.nome} e recupera {self.valore} salute!")
        self.usato = True

```

Metodo | Dettagli
--- | ---
usa() | Recupera salute

## Classe BombaAcida(Oggetto)
### Questo oggetto rimuove alla salute del bersaglio il `danno`. Il *keyword argument* offensivo=True nel costruttore specifica che questo oggetto non deve avere come bersaglio il personaggio che lo usa ma un avversario

```python

class BombaAcida(Oggetto):
    def __init__(self, nome="Bomba Acida",tipo="Esplosivo", danno=30):
        super().__init__(nome, tipo, offensivo=True)
        self.danno = danno

    def usa(self, utilizzatore, bersaglio=None, ambiente=None):
        if bersaglio is None:
            print(f"{utilizzatore.nome} cerca di usare {self.nome}, ma non ha un bersaglio!")
            return
        bersaglio.subisci_danno(self.danno)
        print(f"{utilizzatore.nome} lancia {self.nome} su {bersaglio.nome}, infliggendo {self.danno} danni!")
        self.usato = True

```

Metodo | Dettagli
--- | ---
usa() | Infligge danno

## Classe Medaglione(Oggetto)
### Questo oggetto aumenta `attacco_max` dell'utilizzatore

```python

class Medaglione(Oggetto):
    def __init__(self):
        super().__init__("Medaglione",tipo="Potenziamento")

    def usa(self, utilizzatore, bersaglio=None, ambiente=None):
        target = bersaglio if bersaglio else utilizzatore
        target.attacco_max += 10
        print(f"{target.nome} indossa {self.nome}, aumentando il suo attacco massimo!")
        self.usato = True

```

Metodo | Dettagli
--- | ---
usa() | Aumenta attacco massimo

## Classe InterfacciaUtente
### Questa classe gestisce gli input e l'intrfaccia che l'utente avrà con il programma

```python

class InterfacciaUtente:
    @staticmethod
    def chiedi_input(messaggio, opzioni=None):
        while True:
            risposta = input(messaggio).strip()
            if opzioni:
                if risposta.lower() in [o.lower() for o in opzioni]:
                    return risposta
                else:
                    print(f"Input non valido! Scelte valide: {', '.join(opzioni)}")
            else:
                return risposta

    @staticmethod
    def chiedi_numero(messaggio, minimo=None, massimo=None):
        while True:
            try:
                numero = int(input(messaggio))
                if minimo is not None and numero <= minimo:
                    print(f"Devi inserire un numero maggiore o uguale a {minimo}.")
                    continue  # uso continue in modo da tornare all inizio del ciclo
                if massimo is not None and numero >= massimo:
                    print(f"Devi inserire un numero minore o uguale a {massimo}.")
                    continue
                return numero

            except ValueError:
                print("Input non valido! Devi inserire un numero intero.")

    @staticmethod
    def conferma(messaggio):
        while True:
            risposta = input(messaggio + " (s/n): ").strip().lower()
            if risposta == 's':
                return True
            elif risposta == 'n':
                return False
            else:
                print("Rispondi con 's' o 'n'.")

```

@staticmethod | Dettagli
--- | ---
chiedi_input() | Chiede un input, con la possibilità di impostare delle opzioni prestabilite tra cui scegliere
chiedi_numero() | Chiede un numero, con la possibilità di impostare un minimo e un massimo prestabiliti
conferma() | Chiede una conferma tramite un input 's' o 'n'

---

# Teamwork

| Team          | Membri                       | Responsabilità                     |
| ------------- | -----------------------------| ---------------------------------- |
| **Team 1**    | membro1, membro2, membro3    | Ambiente, Strategy patterns        |
| **Team 2**    | persona1, persona2, persona3 | Missione, Json, Log, Stato         |
| **Opzionali** | Giocatore, Livelli           | Giocatore, Livelli                 |

---

# Modalità di sviluppo
Ogni team:
- ha accesso ad un repository GitHub dove può lavorare in parallelo
- deve documentare il proprio codice e per le funzionalità implementate
- deve organizzare le modifiche o le implementazioni in fasi piu piccole e gestibili
- deve fare commit frequenti e scrivere messaggi chiari per ogni modifica
- deve testare le modifiche prima di fare pull request
- ha un branch principale e può creare branch secondari per le funzionalità
- deve fare pull request per unire le modifiche al branch principale

---

# Team 1

## 1. Esecuzione Classe Ambiente

- **Punti discussi:**
1. Gli ambienti cambiano ad ogni nuovo turno
2. Gli ambienti hanno differenti effetti:
    - l'ambiente "Foresta" da un bonus fisso di +5 all'attacco massimo della classe guerriero e incrementa le cure a fine turno del ladro di un +5
    - l'ambiente "Vulcano" incrementa il danno di bomba acida di un valore random tra 0 e +15, riduce il danno del ladro di 5 e riduce possibil
    - l'ambiente "Palude" riduce cura del 30% a fine combattimento e quando si usa una pozione
3. Gli effetti di un ambiente sugli oggetti hanno effetto solo se sono usati mentre l'ambiente è attivo
4. Gli effetti di un ambiente sui personaggi hanno durata solo per il turno in cui sono presenti

La classe Ambiente deve contenere i seguenti campi:
- nome ambiente
- modifica_attacco
- modifica_cura

e le seguenti funzioni:
- una funzione per dare un bonus/malus sugli attacchi in base alla classe dell'attaccante/di chi è attacccato
- una funzione per dare un bonus o un malus agli effetti degli oggetti
- una funzione per incrementare o decrementare gli effetti delle cure a fine turno

Esempio:
```python
class Ambiente:
    def __init__(self, nome, modifica_attacco=0, modifica_cura=0):
        self.nome = nome
        self.modifica_attacco = modifica_attacco
        self.modifica_cura = modifica_cura

    def modifica_danno(self, attaccante, attaccato):
        pass

    def modifica_effetto_oggetto(self, oggetto):
        pass

    def modifica_cura(self, soggetto):
        pass

```

> argomenti didattici:
**l’uso della composizione (Ambiente dentro Turno), e della configurabilità**

## 2. Esecuzione Classe StrategiaAttacco

### Obiettivi:
La classe si occupa della gestione del comportamento degli avversari durante il combattimento
cercando di apportare un minimo di variazione del comportamento degli avversari con le sue classi derivate.
Inoltre è presente anche una classe factory per gestire la scelta del comportamento senza andare a comunicare direttamente con la classi sopra citate

> argomenti didattici:
**l’uso della composizione (Strategia_Attacco dentro Turno), e della configurabilità**

## 3. Aggiunta della documentazione usando Sphinx

### Obiettivi:
Lo scopo di questa parte è quello di usare lo strumento `sphinx` per generare in automatico la documentazione. `sphinx` può leggere i docstring in stile reStructuredText o Google/Numpy-style dai tuoi file .py e generare documentazione in HTML, PDF o altri formati.

### Implementazione
- **Per prima cosa creiamo l'ambiente virtuale**
```bash
python -m venv venv
source venv/bin/activate
# Windows: 'venv\Scripts\activate'
```

- **Dopodiché, installiamo Sphinx nelle librerie del `venv` appena creato**
```bash
pip install sphinx
```

- **Quickstart di Sphinx, creazione della cartella docs**

Nella cartella del progetto eseguieamo:
```bash
sphinx-quickstart docs
```

Dovrebbe essersi creata una cartella `docs` con la seguente struttura
```bash
├── docs/
│   ├── conf.py                      # File di configurazione Sphinx
│   ├── index.rst                    # Indice principale
│   ├── source/                      # File .rst generati per ciascun modulo
│   └── _build/                      # Output HTML
```

- **Configurazione di Sphinx**

Apriamo il file `docs/conf.py` e aggiungi il percorso del progetto

```python
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

extensions = [
    'sphinx.ext.autodoc',  # per generare doc dai docstrings
    'sphinx.ext.napoleon', # per supporto Google/Numpy style docstrings
    'sphinx_autodoc_typehints', # mostra i tipi come annotazioni
]

html_theme = 'sphinx_rtd_theme'
```

- **Creiamo i file .rst per i moduli del progetto**

Eseguibile automaticamente con:
```bash
sphinx-apidoc -o docs/source ../Gdr
```

Oppure manualmente eseguendo il comando per ogni cartella: `ambienti`, `inventario`, `missioni`, `oggetti`, `patterns`, `personaggi` e `utils`

- **Generiamo la documentazione**

Eseguendo:
```bash
cd docs
make html  # oppure 'make.bat html' su Windows
```
Dovremmo trovare la documentazione HTML in docs/_build/html/index.html

- **Pulizia della documentazione**

Se accadono problemi durante la generazione della documentazione, si può fare il comando seguente per pulire i predecenti file.html generati:
```bash
make.bat clear
```

> argomenti didattici:
**Uso dello strumento `sphinx` per la generazione della documentazione**

# Team 2

## 1. Piccoli fix e semplificazioni d'uso

- Ora è possibile usare un oggetto digitando il suo indice nell'inventario, invece che digitare il nome completo senza errori e case sensitive

Modifiche: Classe `Turno`, metodo `esegui()`


- Ora la stampa dei danni ai personaggi viene effettuata correttamente dopo la stampa dell'attacco e dei danni ricevuti

Modifiche: metodo `attacca()` in classe `Personaggio` e e i relativi override nelle altre classi


- **Bugfix:** Se si utilizzava una pozione essa veniva usata sul nemico curandolo, invece che curare il proprio personaggio. È stata quindi aggiunta una proprietà bersaglio (default=False) agli oggetti, se un oggetto deve essere usata su un bersaglio (nemico) va inizializzato a True, a False l'oggetto viene usato direttamente sul personaggio che lo usa

Modifiche: classe `Oggetto` , costruttore `BombaAcida`, metodo `esegui()` nella classe Turno`

## 2. Creazione classi `Missioni` e `GestoreMissioni`

- La classe Missione si occuperà di aggregare ambienti e nemici (personaggi) per costituire delle missioni il cui fine sarà ottenere delle ricompense (oggetti)
- La classe GestoreMissioni gestisce a sua volta le diverse missioni plausibili attraverso diversi metodi

## 3. Fix classe `Missione` e metodi aggiornati


- Le missioni adesso compendono istanze di classe `Ambiente` in modo da risultare coerenti con la missione

## 4. Implementazioni alla classe `GestoreMissioni`:

- Adesso, la classe `GestoreMissioni` contiene una lista di istanze di Missione
- La classe `GestoreMissioni` adesso possiede metodi per la gestione delle missioni