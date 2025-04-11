# RUBRICA TELEFONICA (V 1.0)

## Argomenti

## Strutture di dati

- Dizionari per memorizzare dati (codice, nome, cognome, numero di telefono, email, data creazione contatto `datetime.now().strftime()`)
- Il codice deve essere formato dalle prime due lettere del nome le prime due del cognome e le ultime due cifre del numero di telefono (in maiuscolo)

## Gestione files
- Lettura e scrittura di file .txt
- Formattazione e parsing con split()
- Pulizia delle stringhe con strip()
- Backup del file dati principale (copiare il file in una catella backup con timestamp aggiunto al nome del file)

## Gestione di input utente
- Il programma non accetta nessun campo vuoto
- Implementazione di un menu principale con Backup Rubrica e Visualizza Rubrica
- Implementazione del sottomenu Visualizza Rubrica con le principali operazioni (Aggiungi, Modifica, Elimina, Cerca)
- Implementazione sottomenu cerca

## Gestione eccezioni
- Gestione delle eccezioni con isdigit o simili tipo che il nome deve essere di almeno 3 lettere
- Il numero di telefono deve evere 10 cifre
- La mail deve contenere il simbolo @
- I nomi ed i cognomi vengono modificati rispetto all inserimento dell utente in modo da avere le iniziali maiuscole
- Se un contatto esiste già, il programma deve chiedere se si vuole sovrascrivere

## Cerca contatti
- Permetti di cercare:
- parte del nome, dominio email, numeri che iniziano per, nomi che iniziano per

## Output
- Dopo ogni operazione, stampa a video lo stato della rubrica (numero contatti e riepilogo ultimi 3 aggiunti/modificati)
- Dopo che l utente effettua la ricerche, il programma deve stampare a video i risultati in modo ordinato e formattato usando \n \t
- Il programma deve stampare a video il numero di contatti presenti in rubrica

```python

```