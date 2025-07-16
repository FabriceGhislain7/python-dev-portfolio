import os
import json
import logging
from typing import List, Dict, Optional, Tuple
from gioco.oggetto import Oggetto
from gioco.inventario import Inventario
from gioco.schemas.oggetto import OggettoSchema
from gioco.schemas.inventario import InventarioSchema
from marshmallow import ValidationError
from config import DATA_DIR_INV

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Schema instances
oggetto_schema = OggettoSchema()
inventario_schema = InventarioSchema()

# ------------------------MAPPING OGGETTI-----------------------------------
def get_object_classes() -> Dict[str, type]:
    """
    Ottiene mapping dinamico di tutte le classi oggetto disponibili.
    
    Returns:
        Dict[str, type]: Dizionario {nome_oggetto: classe_python}
    """
    return {cls.__name__: cls for cls in Oggetto.__subclasses__()}

def validate_object_class(object_name: str) -> Tuple[bool, str]:
    """
    Valida che la classe oggetto sia supportata.
    
    Args:
        object_name (str): Nome oggetto da validare
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    available_objects = get_object_classes()
    
    if object_name not in available_objects:
        return False, f"Oggetto non valido. Disponibili: {', '.join(available_objects.keys())}"
    
    return True, ""

# ------------------------GESTIONE FILE JSON INVENTARI---------------------
def SaveInventoryJson(inventario: Inventario) -> bool:
    """
    Salva inventario su file JSON usando Marshmallow.
    
    Args:
        inventario (Inventario): Istanza inventario da salvare
        
    Returns:
        bool: True se salvato con successo
    """
    try:
        # Determina nome file basato su proprietario o ID inventario
        file_name = (
            f"{inventario.id_proprietario}.json"
            if inventario.id_proprietario else
            f"{inventario.id}.json"
        )
        file_path = os.path.join(DATA_DIR_INV, file_name)
        
        # Serializza con Marshmallow
        inventario_dict = inventario_schema.dump(inventario)
        
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(inventario_dict, file, indent=4)

        logger.info(f"Inventario salvato: {file_name}")
        return True
        
    except Exception as e:
        logger.error(f"Errore salvataggio inventario: {str(e)}")
        return False

def LoadInventoryJson(personaggio_id: str) -> Optional[Dict]:
    """
    Carica inventario da file JSON con validazione Marshmallow.
    
    Args:
        personaggio_id (str): ID del proprietario dell'inventario
        
    Returns:
        Optional[Dict]: Dati inventario validati o None se errore
    """
    # Prova caricamento diretto per ID proprietario
    file_name = os.path.join(DATA_DIR_INV, f"{personaggio_id}.json")
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Validazione con Marshmallow
            inventario_obj = inventario_schema.load(data)
            validated_dict = inventario_schema.dump(inventario_obj)
            
            logger.info(f"Inventario caricato direttamente: {personaggio_id}")
            return validated_dict
            
        except (json.JSONDecodeError, ValidationError) as e:
            logger.error(f"Errore caricamento inventario {file_name}: {e}")
            return None

    # Fallback: cerca in tutti i file per ID proprietario
    return _SearchInventoryByOwner(personaggio_id)

def _SearchInventoryByOwner(personaggio_id: str) -> Optional[Dict]:
    """
    Cerca inventario per ID proprietario in tutti i file (fallback).
    
    Args:
        personaggio_id (str): ID proprietario da cercare
        
    Returns:
        Optional[Dict]: Inventario trovato o None
    """
    try:
        for file in os.listdir(DATA_DIR_INV):
            if file.endswith('.json') and file != '.gitkeep':
                file_path = os.path.join(DATA_DIR_INV, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    if str(data.get('id_proprietario')) == str(personaggio_id):
                        # Validazione con Marshmallow
                        inventario_obj = inventario_schema.load(data)
                        validated_dict = inventario_schema.dump(inventario_obj)
                        
                        logger.info(f"Inventario trovato via fallback: {personaggio_id} in {file}")
                        return validated_dict
                        
                except (json.JSONDecodeError, ValidationError) as e:
                    logger.error(f"Errore fallback caricamento da {file}: {e}")
                    continue
    
    except Exception as e:
        logger.error(f"Errore durante ricerca fallback: {str(e)}")
    
    logger.warning(f"Inventario non trovato per personaggio {personaggio_id}")
    return None

def DeleteInventoryJson(personaggio_id: str) -> bool:
    """
    Elimina file JSON inventario del personaggio.
    
    Args:
        personaggio_id (str): ID del proprietario
        
    Returns:
        bool: True se eliminato con successo
    """
    try:
        file_path = os.path.join(DATA_DIR_INV, f"{personaggio_id}.json")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Inventario eliminato: {file_path}")
            return True
        else:
            logger.warning(f"File inventario non trovato: {file_path}")
            return False
            
    except Exception as e:
        logger.error(f"Errore eliminazione inventario {personaggio_id}: {str(e)}")
        return False

def GetAllInventoryFiles() -> List[str]:
    """
    Ottiene lista di tutti i file inventario esistenti.
    
    Returns:
        List[str]: Lista di IDs inventari trovati
    """
    try:
        files = os.listdir(DATA_DIR_INV)
        inventory_ids = []
        
        for file in files:
            if file.endswith('.json') and file != '.gitkeep':
                filename = os.path.splitext(file)[0]
                inventory_ids.append(filename)
        
        logger.info(f"Trovati {len(inventory_ids)} file inventario")
        return inventory_ids
        
    except Exception as e:
        logger.error(f"Errore lettura directory inventari: {str(e)}")
        return []

# ------------------------VALIDAZIONE OGGETTI-------------------------------
def validate_object_name(nome: str) -> Tuple[bool, str]:
    """
    Valida il nome dell'oggetto secondo regole del gioco.
    
    Args:
        nome (str): Nome da validare
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not nome or not isinstance(nome, str):
        return False, "Nome oggetto è obbligatorio"
    
    nome = nome.strip()
    
    if len(nome) < 2:
        return False, "Il nome deve essere almeno 2 caratteri"
    
    if len(nome) > 100:
        return False, "Il nome non può superare 100 caratteri"
    
    return True, ""

def validate_object_value(valore: int) -> Tuple[bool, str]:
    """
    Valida il valore dell'oggetto.
    
    Args:
        valore (int): Valore da validare
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if valore < 0:
        return False, "Il valore non può essere negativo"
    
    if valore > 999999:
        return False, "Valore massimo: 999,999"
    
    return True, ""

# ------------------------CREAZIONE OGGETTI E INVENTARI--------------------
def create_object_instance(object_type: str) -> Oggetto:
    """
    Crea istanza oggetto della classe specificata.
    
    Args:
        object_type (str): Tipo di oggetto da creare
        
    Returns:
        Oggetto: Istanza dell'oggetto creato
        
    Raises:
        ValueError: Se tipo oggetto non valido
    """
    oggetti = get_object_classes()
    
    if object_type not in oggetti:
        raise ValueError(f"Tipo oggetto '{object_type}' non valido")
    
    oggetto = oggetti[object_type]()
    
    logger.info(f"Istanza oggetto creata: {object_type}")
    return oggetto

def create_custom_object(object_type: str, nome: str, valore: int = 0) -> Oggetto:
    """
    Crea oggetto personalizzato con parametri specifici.
    
    Args:
        object_type (str): Tipo di oggetto
        nome (str): Nome personalizzato
        valore (int): Valore personalizzato
        
    Returns:
        Oggetto: Oggetto configurato
    """
    oggetto = create_object_instance(object_type)
    oggetto.nome = nome
    oggetto.valore = valore
    
    logger.info(f"Oggetto personalizzato creato: {nome} ({object_type})")
    return oggetto

def create_character_inventory(char_id: str, initial_object: Oggetto) -> Inventario:
    """
    Crea inventario iniziale per il personaggio.
    
    Args:
        char_id (str): ID del personaggio proprietario
        initial_object (Oggetto): Oggetto iniziale da aggiungere
        
    Returns:
        Inventario: Inventario creato e configurato
    """
    inv = Inventario(id_proprietario=char_id)
    inv.aggiungi_oggetto(initial_object)
    
    logger.info(f"Inventario creato per personaggio {char_id}")
    return inv

# ------------------------OPERAZIONI INVENTARIO-----------------------------
def add_object_to_inventory(inventario_data: Dict, nuovo_oggetto: Oggetto) -> Tuple[bool, str]:
    """
    Aggiunge oggetto all'inventario con validazione.
    
    Args:
        inventario_data (Dict): Dati inventario serializzati
        nuovo_oggetto (Oggetto): Oggetto da aggiungere
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        # Deserializza inventario
        inventario_obj = inventario_schema.load(inventario_data)
        
        # Aggiunge oggetto
        inventario_obj.aggiungi_oggetto(nuovo_oggetto)
        
        # Salva su file
        if SaveInventoryJson(inventario_obj):
            logger.info(f"Oggetto '{nuovo_oggetto.nome}' aggiunto all'inventario")
            return True, f"Oggetto '{nuovo_oggetto.nome}' aggiunto con successo"
        else:
            return False, "Errore salvataggio inventario"
            
    except ValidationError as e:
        logger.error(f"Errore validazione inventario: {e}")
        return False, "Errore validazione inventario"
    except Exception as e:
        logger.error(f"Errore aggiunta oggetto: {str(e)}")
        return False, "Errore durante l'aggiunta dell'oggetto"

def remove_object_from_inventory(inventario_data: Dict, oggetto_id: str) -> Tuple[bool, str, Optional[Oggetto]]:
    """
    Rimuove oggetto dall'inventario.
    
    Args:
        inventario_data (Dict): Dati inventario serializzati
        oggetto_id (str): ID oggetto da rimuovere
        
    Returns:
        Tuple[bool, str, Optional[Oggetto]]: (success, message, oggetto_rimosso)
    """
    try:
        # Deserializza inventario
        inventario_obj = inventario_schema.load(inventario_data)
        
        # Rimuove oggetto
        oggetto_rimosso = inventario_obj.rimuovi_oggetto(oggetto_id)
        
        if oggetto_rimosso:
            # Salva su file
            if SaveInventoryJson(inventario_obj):
                logger.info(f"Oggetto ID {oggetto_id} rimosso dall'inventario")
                return True, "Oggetto rimosso con successo", oggetto_rimosso
            else:
                return False, "Errore salvataggio inventario", None
        else:
            return False, "Oggetto non trovato nell'inventario", None
            
    except ValidationError as e:
        logger.error(f"Errore validazione inventario: {e}")
        return False, "Errore validazione inventario", None
    except Exception as e:
        logger.error(f"Errore rimozione oggetto: {str(e)}")
        return False, "Errore durante la rimozione", None

def use_object_in_inventory(inventario_data: Dict, oggetto_nome: str, utilizzatore, bersaglio) -> Tuple[bool, str]:
    """
    Usa oggetto dall'inventario su un bersaglio.
    
    Args:
        inventario_data (Dict): Dati inventario serializzati
        oggetto_nome (str): Nome oggetto da usare
        utilizzatore: Personaggio che usa l'oggetto
        bersaglio: Bersaglio dell'oggetto
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        # Deserializza inventario
        inventario_obj = inventario_schema.load(inventario_data)
        
        # Trova oggetto per nome
        oggetto = next((o for o in inventario_obj.oggetti if o.nome == oggetto_nome), None)
        
        if not oggetto:
            return False, f"Oggetto '{oggetto_nome}' non trovato nell'inventario"
        
        # Usa oggetto
        result = inventario_obj.usa_oggetto(oggetto, utilizzatore=utilizzatore, bersaglio=bersaglio)
        
        # Salva inventario aggiornato
        if SaveInventoryJson(inventario_obj):
            logger.info(f"Oggetto '{oggetto_nome}' usato da {utilizzatore.nome} su {bersaglio.nome}")
            return True, f"Oggetto '{oggetto_nome}' utilizzato con successo"
        else:
            return False, "Errore salvataggio dopo utilizzo"
            
    except ValidationError as e:
        logger.error(f"Errore validazione inventario: {e}")
        return False, "Errore validazione inventario"
    except Exception as e:
        logger.error(f"Errore utilizzo oggetto: {str(e)}")
        return False, "Errore durante l'utilizzo dell'oggetto"

# ------------------------STATISTICHE INVENTARI-----------------------------
def GetInventoryItemCount(inventario_data: Dict) -> int:
    """
    Conta il numero di oggetti in un inventario.
    
    Args:
        inventario_data (Dict): Dati inventario serializzati
        
    Returns:
        int: Numero di oggetti nell'inventario
    """
    try:
        oggetti = inventario_data.get('oggetti', [])
        count = len(oggetti)
        logger.info(f"Conteggio oggetti inventario: {count}")
        return count
    except Exception as e:
        logger.error(f"Errore conteggio oggetti: {str(e)}")
        return 0

def GetInventoryValueTotal(inventario_data: Dict) -> int:
    """
    Calcola valore totale di tutti gli oggetti nell'inventario.
    
    Args:
        inventario_data (Dict): Dati inventario serializzati
        
    Returns:
        int: Valore totale dell'inventario
    """
    try:
        oggetti = inventario_data.get('oggetti', [])
        valore_totale = sum(obj.get('valore', 0) for obj in oggetti)
        logger.info(f"Valore totale inventario: {valore_totale}")
        return valore_totale
    except Exception as e:
        logger.error(f"Errore calcolo valore inventario: {str(e)}")
        return 0

def GetInventoryStatsByType(inventario_data: Dict) -> Dict[str, int]:
    """
    Ottiene statistiche oggetti per tipo nell'inventario.
    
    Args:
        inventario_data (Dict): Dati inventario serializzati
        
    Returns:
        Dict[str, int]: Dizionario {tipo_oggetto: quantità}
    """
    try:
        oggetti = inventario_data.get('oggetti', [])
        stats = {}
        
        for obj in oggetti:
            tipo = obj.get('classe', 'Unknown')
            stats[tipo] = stats.get(tipo, 0) + 1
        
        # Aggiungi totale
        stats['Totale'] = sum(stats.values())
        
        logger.info(f"Statistiche inventario per tipo: {stats}")
        return stats
        
    except Exception as e:
        logger.error(f"Errore statistiche inventario: {str(e)}")
        return {'Totale': 0}

def FindObjectsInInventory(inventario_data: Dict, criteria: Dict) -> List[Dict]:
    """
    Cerca oggetti nell'inventario secondo criteri specifici.
    
    Args:
        inventario_data (Dict): Dati inventario serializzati
        criteria (Dict): Criteri di ricerca (nome, tipo, valore_min, etc.)
        
    Returns:
        List[Dict]: Lista oggetti che corrispondono ai criteri
    """
    try:
        oggetti = inventario_data.get('oggetti', [])
        risultati = []
        
        for obj in oggetti:
            match = True
            
            # Controllo nome (parziale, case-insensitive)
            if 'nome' in criteria:
                if criteria['nome'].lower() not in obj.get('nome', '').lower():
                    match = False
            
            # Controllo tipo esatto
            if 'tipo' in criteria:
                if criteria['tipo'] != obj.get('classe', ''):
                    match = False
            
            # Controllo valore minimo
            if 'valore_min' in criteria:
                if obj.get('valore', 0) < criteria['valore_min']:
                    match = False
            
            # Controllo valore massimo
            if 'valore_max' in criteria:
                if obj.get('valore', 0) > criteria['valore_max']:
                    match = False
            
            if match:
                risultati.append(obj)
        
        logger.info(f"Ricerca inventario: trovati {len(risultati)} oggetti")
        return risultati
        
    except Exception as e:
        logger.error(f"Errore ricerca inventario: {str(e)}")
        return []

# ------------------------LOGGING E DEBUG-----------------------------------
def log_inventory_operation(operation: str, inventory_data: Dict, user_email: str, **extra_data):
    """
    Log standardizzato per operazioni sugli inventari.
    
    Args:
        operation (str): Tipo operazione (created, updated, object_added, etc.)
        inventory_data (Dict): Dati dell'inventario
        user_email (str): Email dell'utente
        **extra_data: Dati aggiuntivi da loggare
    """
    owner_id = inventory_data.get('id_proprietario', 'Unknown')
    inventory_id = inventory_data.get('id', 'Unknown')
    item_count = len(inventory_data.get('oggetti', []))
    
    log_message = f"Inventory {operation} - User: {user_email}, Owner: {owner_id}, ID: {inventory_id}, Items: {item_count}"
    
    if extra_data:
        extra_info = ", ".join([f"{k}: {v}" for k, v in extra_data.items()])
        log_message += f", {extra_info}"
    
    logger.info(log_message)

def get_inventory_debug_info(inventario_data: Dict) -> Dict:
    """
    Ottiene informazioni di debug per un inventario.
    
    Args:
        inventario_data (Dict): Dati inventario
        
    Returns:
        Dict: Informazioni di debug
    """
    try:
        return {
            'id_inventario': inventario_data.get('id', 'N/A'),
            'id_proprietario': inventario_data.get('id_proprietario', 'N/A'),
            'numero_oggetti': len(inventario_data.get('oggetti', [])),
            'valore_totale': GetInventoryValueTotal(inventario_data),
            'tipi_oggetti': list(GetInventoryStatsByType(inventario_data).keys()),
            'oggetti_dettagli': [
                {
                    'nome': obj.get('nome', 'N/A'),
                    'tipo': obj.get('classe', 'N/A'),
                    'valore': obj.get('valore', 0),
                    'usato': obj.get('usato', False)
                }
                for obj in inventario_data.get('oggetti', [])
            ]
        }
    except Exception as e:
        logger.error(f"Errore debug info inventario: {str(e)}")
        return {'error': str(e)}