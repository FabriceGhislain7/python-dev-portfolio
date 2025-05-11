
Il programma deve essere in grado di gestire una rubrica telefonica deve  dove ogni conttato è rapresentato da un file json separato.
Ogni file json si chiamerà con `'nome_cognome.json'` e deve contenere le seguenti informazioni:
```json
{
    "nome": "Nome1",
    "cognome": "Cognome1",
    "telefono": [
        {
            "tipo": "casa",
            "numero": "2478382394"
        },
        {
            "tipo": "cellulare",
            "numero": "351838000"
        }
    ],
    "attivo": true,
    "attivita": ["programatore", "web deseign", "Custumer care"],
    "note": "Note1"
}
``` 
Deve essere presente una cartella chiamata `contatti` nella quale deve essere inserite i file json.
- Gli utenti devono poter:
    . aggiungere un conttato.
    - Modificare un contatto
    - Eliminare un contatto
    - Visualizzare i contatti attivi

Devono essere gestite gli errori comuni con `try except` e devono essere stampati messaggi di errore chiari e comprensibili. 

Devono essere presente il file `README.md` con la descrizione del progetto e le indicazioni delle procedure usate.