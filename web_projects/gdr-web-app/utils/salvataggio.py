import json
from typing import Any
import logging
from config import LOG_JSON_PATH


class Json:

    @staticmethod
    def scrivi_dati(file_path: str, dati_da_salvare: dict) -> None:
        """
        Scrive i dati in un file JSON.

        Args:
            file_path (str): Percorso del file in cui salvare i dati.
            dati_da_salvare (dict): Dati da salvare nel file JSON.
            encoder (function): Funzione di codifica per convertire oggetti in JSON.

        Return:
            None
        """

        try:
            with open(file_path, 'w') as file:
                json.dump(dati_da_salvare, file, indent=4)
            print(f"Dati scritti con successo in {file_path}")
        except Exception as e:
            print(f"Errore nella scrittura del file JSON: {e}")

    def carica_dati(file_path: str) -> dict:
        """
        Carica i dati da un file JSON specificato.

        Args:
            file_path (str): Percorso del file da cui caricare i dati.

        Returns:
            dict: Dati caricati dal file JSON.
        """

        try:
            with open(file_path, 'r') as file:
                dati = json.load(file)
            return dati
        except Exception as e:
            print(f"Errore nella lettura del file JSON: {e}")
            return None

    @staticmethod
    def applica_patch(patch_element: dict) -> None:
        """
        Applica un aggiornamento a tutti gli oggetti nel salvataggio che combaciano
        con __class__ e nome dell'oggetto dato come patch (non strutturata).

        Args:
            salvataggio (dict): Il dizionario del salvataggio da aggiornare.
            patch_element (dict): Un oggetto da aggiornare, con chiavi come '__class__', 'nome', etc.
        """
        def match(e1: dict, e2: dict) -> bool:
            """
                Controlla se due dict rappresentano lo stesso oggetto logico,
                confrontando '__class__' e 'nome'.

                Args:
                    e1 (dict): Dizionario presente nel salvataggio.
                    e2 (dict): Patch da applicare.

                Returns:
                    bool: True se entrambi sono dict e hanno stesse '__class__' e 'nome'.
            """
            return (
                isinstance(e1, dict) and
                all(e1.get(k) == e2.get(k) for k in ("__class__", "nome"))
            )

        def aggiorna(dizionario: dict, aggiornamento: dict) -> None:
            """
                Unisce i campi da 'aggiornamento' dentro 'dizionario',
                ricorsivamente per dict annidati.

                Args:
                    dizionario (dict): Dizionario originale da modificare.
                    aggiornamento (dict): Dizionario con nuovi valori.

                Returns:
                    None
            """
            for k, v in aggiornamento.items():
                if isinstance(v, dict) and isinstance(dizionario.get(k), dict):
                    aggiorna(dizionario[k], v)
                else:
                    dizionario[k] = v

        def cerca_e_aggiorna(obj) -> None:
            """
                Cerca ricorsivamente nell’oggetto (dict o list),
                applicando la patch se trova una corrispondenza.

                Args:
                    obj (Union[dict, list]): Oggetto da esplorare.

                Returns:
                    None
            """
            if isinstance(obj, dict):
                if match(obj, patch_element):
                    aggiorna(obj, patch_element)
                for v in obj.values():
                    cerca_e_aggiorna(v)
            elif isinstance(obj, list):
                for item in obj:
                    cerca_e_aggiorna(item)
        salvataggio = Json.carica_dati("data/salvataggio.json")
        cerca_e_aggiorna(salvataggio)
        return salvataggio

class JsonLogHandler(logging.Handler):
    """
    Handler per scrivere i log in un file JSON.
    I messaggi sono salvati come lista sotto la chiave "messaggio".
    """
    def emit(self, record):
        log_path = LOG_JSON_PATH
        messaggio = self.format(record)
        print(f"Log ----------------->: {messaggio}")

        try:
            dati = Json.carica_dati(log_path)

            if not dati or not isinstance(dati, dict):
                dati = {"log": []}
            elif "log" not in dati or not isinstance(dati["log"], list):
                dati["log"] = []

            dati["log"].append(messaggio)
            Json.scrivi_dati(log_path, dati)

        except Exception as e:
            logging.error(f"Errore durante la scrittura del log in JSON: {e}")

def setup_logger():
    """
    Configura il logger per scrivere i messaggi in un file JSON.
    la funzione viene chiamata all'avvio dell'applicazione.

    """
    logger = logging.getLogger('json_logger')
    logger.setLevel(logging.INFO)

    if not any(isinstance(handler, JsonLogHandler) for handler in logger.handlers):
        json_handler = JsonLogHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        json_handler.setFormatter(formatter)
        logger.addHandler(json_handler)