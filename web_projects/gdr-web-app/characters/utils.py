import os
import json
import logging
from typing import List, Dict, Optional, Tuple
from gioco.personaggio import Personaggio
from gioco.schemas.personaggio import PersonaggioSchema
from config import DATA_DIR_PGS
from auth.credits import credits_to_create, credits_to_refund

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Schema instance
schema = PersonaggioSchema()

# ------------------------MAPPING CLASSI PERSONAGGI------------------------
def get_character_classes() -> Dict[str, type]:
    """
    Ottiene mapping dinamico di tutte le classi personaggio disponibili.
    
    Returns:
        Dict[str, type]: Dizionario {nome_classe: classe_python}
    """
    return {cls.__name__: cls for cls in Personaggio.__subclasses__()}

# ------------------------VALIDAZIONE INPUT PERSONAGGI---------------------
def validate_character_name(nome: str) -> Tuple[bool, str]:
    """
    Valida il nome del personaggio secondo regole del gioco.

    Args:
        nome (str): Nome da validare

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not nome or not isinstance(nome, str):
        return False, "Nome è obbligatorio"

    nome = nome.strip()

    if len(nome) < 3:
        return False, "Il nome deve essere almeno 3 caratteri"

    if len(nome) > 50:
        return False, "Il nome non può superare 50 caratteri"

    if not nome.replace(' ', '').isalnum():
        return False, "Il nome può contenere solo lettere e numeri"

    return True, ""

def validate_character_class(classe: str) -> Tuple[bool, str]:
    """
    Valida che la classe personaggio sia supportata.

    Args:
        classe (str): Nome classe da validare

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    available_classes = get_character_classes()

    if classe not in available_classes:
        return False, f"Classe non valida. Disponibili: {', '.join(available_classes.keys())}"

    return True, ""

# ------------------------GESTIONE FILE JSON PERSONAGGI--------------------
def SaveCharacterJson(character_dict: Dict) -> bool:
    """
    Salva dizionario personaggio su file JSON.
    
    Args:
        character_dict (Dict): Dati personaggio serializzati
        
    Returns:
        bool: True se salvato con successo
    """
    try:
        name_file = f"{character_dict['id']}.json"
        path = os.path.join(DATA_DIR_PGS, name_file)
        
        with open(path, "w", encoding="utf-8") as file:
            json.dump(character_dict, file, indent=4)
        
        logger.info(f"Personaggio salvato: {name_file}")
        return True
        
    except Exception as e:
        logger.error(f"Errore salvataggio personaggio: {str(e)}")
        return False

def LoadCharacterJson(char_id: str) -> Optional[Dict]:
    """
    Carica personaggio da file JSON e lo valida.
    
    Args:
        char_id (str): ID del personaggio da caricare
        
    Returns:
        Optional[Dict]: Dati personaggio o None se errore
    """
    try:
        path = os.path.join(DATA_DIR_PGS, f"{char_id}.json")
        
        if not os.path.exists(path):
            logger.warning(f"File personaggio non trovato: {char_id}")
            return None
        
        with open(path, "r", encoding='utf-8') as file:
            char_dict = json.load(file)
        
        # Validazione con Marshmallow
        character = schema.load(char_dict)
        validated_dict = schema.dump(character)
        
        return validated_dict
        
    except Exception as e:
        logger.error(f"Errore caricamento personaggio {char_id}: {str(e)}")
        return None

def DeleteCharacterJson(char_id: str) -> bool:
    """
    Elimina file JSON del personaggio.
    
    Args:
        char_id (str): ID del personaggio da eliminare
        
    Returns:
        bool: True se eliminato con successo
    """
    try:
        file_path = os.path.join(DATA_DIR_PGS, f"{char_id}.json")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File personaggio eliminato: {file_path}")
            return True
        else:
            logger.warning(f"File personaggio non trovato: {file_path}")
            return False
            
    except Exception as e:
        logger.error(f"Errore eliminazione file personaggio {char_id}: {str(e)}")
        return False

# ------------------------GESTIONE IDS UTENTE-------------------------------
def get_user_character_files() -> List[str]:
    """
    Ottiene lista di tutti i file personaggio esistenti.
    
    Returns:
        List[str]: Lista di IDs dei file trovati
    """
    try:
        files = os.listdir(DATA_DIR_PGS)
        char_ids = []
        
        for file in files:
            if file.endswith('.json') and file != '.gitkeep':
                filename = os.path.splitext(file)[0]
                char_ids.append(filename)
        
        return char_ids
        
    except Exception as e:
        logger.error(f"Errore lettura directory personaggi: {str(e)}")
        return []

def filter_owned_characters(user_char_ids: List[str]) -> List[str]:
    """
    Filtra personaggi dell'utente che esistono realmente su file.
    
    Args:
        user_char_ids (List[str]): IDs personaggi nel database utente
        
    Returns:
        List[str]: IDs personaggi effettivamente posseduti e esistenti
    """
    if not user_char_ids:
        return []
    
    all_files = get_user_character_files()
    owned_chars = [char_id for char_id in user_char_ids if char_id in all_files]
    
    logger.info(f"Filtrati {len(owned_chars)} personaggi posseduti da {len(user_char_ids)} totali")
    return owned_chars

def update_user_character_ids(current_ids: List[str], char_id: str, operation: str) -> List[str]:
    """
    Aggiorna lista IDs personaggi dell'utente.
    
    Args:
        current_ids (List[str]): IDs attuali
        char_id (str): ID da aggiungere/rimuovere
        operation (str): 'add' o 'remove'
        
    Returns:
        List[str]: Lista aggiornata
    """
    if current_ids is None:
        current_ids = []
    
    # Assicura tutti stringhe
    current_ids = [str(cid) for cid in current_ids]
    char_id = str(char_id)
    
    if operation == 'add' and char_id not in current_ids:
        current_ids.append(char_id)
    elif operation == 'remove' and char_id in current_ids:
        current_ids.remove(char_id)
    
    return current_ids

# ------------------------CREAZIONE PERSONAGGI------------------------------
def create_character_instance(nome: str, classe: str) -> Personaggio:
    """
    Crea istanza personaggio della classe specificata.
    
    Args:
        nome (str): Nome del personaggio
        classe (str): Nome della classe
        
    Returns:
        Personaggio: Istanza del personaggio creato
        
    Raises:
        ValueError: Se classe non valida
    """
    classi = get_character_classes()
    
    if classe not in classi:
        raise ValueError(f"Classe '{classe}' non valida")
    
    pg = classi[classe]()
    pg.nome = nome
    pg.npc = False
    pg.classe = classe
    
    logger.info(f"Istanza personaggio creata: {nome} ({classe})")
    return pg

# ------------------------STATISTICHE PERSONAGGI---------------------------
def GetUserCharacterCount(user_char_ids: List[str]) -> int:
    """
    Ottiene numero totale di personaggi dell'utente.
    
    Args:
        user_char_ids (List[str]): Lista IDs personaggi utente
        
    Returns:
        int: Numero totale personaggi posseduti
    """
    if not user_char_ids:
        return 0
    
    owned_chars = filter_owned_characters(user_char_ids)
    count = len(owned_chars)
    
    logger.info(f"Conteggio personaggi utente: {count}")
    return count

def GetUserCharacterStatsByClass(user_char_ids: List[str]) -> Dict[str, int]:
    """
    Ottiene statistiche personaggi per classe dell'utente.
    
    Args:
        user_char_ids (List[str]): Lista IDs personaggi utente
        
    Returns:
        Dict[str, int]: Dizionario {classe: numero_personaggi}
    """
    if not user_char_ids:
        return {"Mago": 0, "Guerriero": 0, "Ladro": 0, "Totale": 0}
    
    # Carica tutti i personaggi dell'utente
    owned_chars = filter_owned_characters(user_char_ids)
    characters = LoadMultipleCharactersJson(owned_chars)
    
    # Conteggio per classe
    stats = {"Mago": 0, "Guerriero": 0, "Ladro": 0}
    
    for char in characters:
        classe = char.get('classe', 'Unknown')
        if classe in stats:
            stats[classe] += 1
    
    # Aggiungi totale
    stats["Totale"] = sum(stats.values())
    
    logger.info(f"Statistiche personaggi per classe: {stats}")
    return stats

def GetMostPlayedClass(user_char_ids: List[str]) -> Tuple[str, int]:
    """
    Ottiene la classe più giocata dall'utente.
    
    Args:
        user_char_ids (List[str]): Lista IDs personaggi utente
        
    Returns:
        Tuple[str, int]: (classe_più_giocata, numero_personaggi)
    """
    stats = GetUserCharacterStatsByClass(user_char_ids)
    
    # Rimuovi totale dal conteggio
    class_stats = {k: v for k, v in stats.items() if k != "Totale"}
    
    if not class_stats or all(count == 0 for count in class_stats.values()):
        return "Nessuna", 0
    
    most_played = max(class_stats.items(), key=lambda x: x[1])
    
    logger.info(f"Classe più giocata: {most_played[0]} ({most_played[1]} personaggi)")
    return most_played

def GetCharacterDistribution(user_char_ids: List[str]) -> Dict[str, float]:
    """
    Ottiene distribuzione percentuale delle classi.
    
    Args:
        user_char_ids (List[str]): Lista IDs personaggi utente
        
    Returns:
        Dict[str, float]: Dizionario {classe: percentuale}
    """
    stats = GetUserCharacterStatsByClass(user_char_ids)
    total = stats.get("Totale", 0)
    
    if total == 0:
        return {"Mago": 0.0, "Guerriero": 0.0, "Ladro": 0.0}
    
    distribution = {}
    for classe in ["Mago", "Guerriero", "Ladro"]:
        percentage = (stats[classe] / total) * 100
        distribution[classe] = round(percentage, 1)
    
    logger.info(f"Distribuzione classi: {distribution}")
    return distribution

# ------------------------CARICAMENTO BATCH---------------------------------
def LoadMultipleCharactersJson(char_ids: List[str]) -> List[Dict]:
    """
    Carica multipli personaggi da file JSON e li valida.
    
    Args:
        char_ids (List[str]): Lista di IDs da caricare
        
    Returns:
        List[Dict]: Lista personaggi caricati con successo
    """
    characters = []
    
    for char_id in char_ids:
        char_data = LoadCharacterJson(char_id)
        if char_data:
            characters.append(char_data)
    
    logger.info(f"Caricati {len(characters)} personaggi da {len(char_ids)} richiesti")
    return characters

def find_character_by_id(characters: List[Dict], char_id: str) -> Optional[Dict]:
    """
    Trova personaggio specifico in una lista.
    
    Args:
        characters (List[Dict]): Lista personaggi
        char_id (str): ID da cercare
        
    Returns:
        Optional[Dict]: Personaggio trovato o None
    """
    for char in characters:
        if str(char.get('id')) == str(char_id):
            return char
    return None

# ------------------------CREDITI E VALIDAZIONE-----------------------------
def calculate_character_cost(character: Personaggio) -> int:
    """
    Calcola costo in crediti per un personaggio.
    
    Args:
        character (Personaggio): Personaggio di cui calcolare il costo
        
    Returns:
        int: Costo in crediti
    """
    return credits_to_create(character)

def calculate_character_refund(character: Personaggio) -> int:
    """
    Calcola rimborso in crediti per un personaggio.
    
    Args:
        character (Personaggio): Personaggio di cui calcolare il rimborso
        
    Returns:
        int: Rimborso in crediti
    """
    return credits_to_refund(character)

def validate_user_can_afford(user_credits: float, required_credits: int) -> Tuple[bool, str]:
    """
    Verifica se l'utente può permettersi l'operazione.
    
    Args:
        user_credits (float): Crediti disponibili utente
        required_credits (int): Crediti richiesti
        
    Returns:
        Tuple[bool, str]: (can_afford, error_message)
    """
    if user_credits >= required_credits:
        return True, ""
    else:
        return False, f"Crediti insufficienti. Servono {required_credits}, hai {int(user_credits)}"

# ------------------------COMBATTIMENTO-------------------------------------
def execute_combat_turn(attacker: Personaggio, defender: Personaggio) -> Tuple[bool, int, str]:
    """
    Esegue un singolo turno di combattimento.
    
    Args:
        attacker (Personaggio): Personaggio attaccante
        defender (Personaggio): Personaggio difensore
        
    Returns:
        Tuple[bool, int, str]: (successo, danno_inflitto, messaggio)
    """
    successo = attacker.esegui_azione()
    
    if successo:
        danno = attacker.attacca()
        defender.subisci_danno(danno)
        messaggio = f"{attacker.nome} infligge {danno} danni a {defender.nome} (Salute residua: {defender.salute})"
        return True, danno, messaggio
    else:
        messaggio = f"{attacker.nome} ha fallito l'attacco!"
        return False, 0, messaggio

def determine_combat_winner(pg1: Personaggio, pg2: Personaggio) -> str:
    """
    Determina il vincitore del combattimento.
    
    Args:
        pg1 (Personaggio): Primo combattente
        pg2 (Personaggio): Secondo combattente
        
    Returns:
        str: Messaggio del risultato
    """
    if pg1.salute <= 0 and pg2.salute <= 0:
        return "Pareggio! Entrambi i combattenti sono stati sconfitti"
    elif pg1.salute <= 0:
        return f"Vittoria di {pg2.nome}!"
    elif pg2.salute <= 0:
        return f"Vittoria di {pg1.nome}!"
    else:
        return "Combattimento in corso..."

# ------------------------LOGGING E DEBUG-----------------------------------
def log_character_operation(operation: str, char_data: Dict, user_email: str, **extra_data):
    """
    Log standardizzato per operazioni sui personaggi.
    
    Args:
        operation (str): Tipo operazione (created, updated, deleted, etc.)
        char_data (Dict): Dati del personaggio
        user_email (str): Email dell'utente
        **extra_data: Dati aggiuntivi da loggare
    """
    char_name = char_data.get('nome', 'Unknown')
    char_id = char_data.get('id', 'Unknown')
    char_class = char_data.get('classe', 'Unknown')
    
    log_message = f"Character {operation} - User: {user_email}, Name: {char_name}, Class: {char_class}, ID: {char_id}"
    
    if extra_data:
        extra_info = ", ".join([f"{k}: {v}" for k, v in extra_data.items()])
        log_message += f", {extra_info}"
    
    logger.info(log_message)