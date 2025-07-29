
# Obbiettivo finale

ora che abbiamo sistemato le i bug principali dovrei modificare test_battle in
modo da gestire quanto segue:

- avere una lista comune dei personaggi giocabili e degli npc, con posizioni randomiche per il turno.
- dopo di che mostrare di chi è il turno e se ha la proprieta npc=False permettere di:

  - opzionalmente usare un oggetto su uno dei bersagli presenti nella lista
  - eseguire un attacco su uno dei personaggi della lista precedente
  - salvare lo stato della sessione di gioco su un file json

- se invece è un npc si userà la stategia della missione per l'uso di oggetti e
  poi si eseguirà un attacco su uno dei bersagli npc = False presenti nella lista
- i personaggi con salute = 0 devono essere esclusi come bersagli validi per
  l'uso degli oggetti e degli attacchi
- finito il suo turno si deve poter passare al turno successivo purchè dotato
  di salute superiore a 0
- se tutti i personaggi npc sono sconfitti si ha finto
- se tutti i personaggi giocabili sono sconfitti si ha perso

## Punto di partenza

test_battle quindi deve poter mostare questi dati:

- npc e pc
- personaggio che sta eseguendo l'azione e se è pc mostrare il pulsante di uso
  oggetto e la lista dei personaggi su cui eseguire lazione e il pulsante di conferma
- poter mostrare in una sezione scorrevole sottostante i messaggi con i risultati
