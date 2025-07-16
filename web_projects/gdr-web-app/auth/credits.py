from gioco.personaggio import Personaggio
import logging

# Setup logger per transazioni crediti
credits_logger = logging.getLogger('credits')
credits_logger.setLevel(logging.INFO)

class CreditsManager:
    """
    Gestore centralizzato per operazioni sui crediti del gioco.
    
    Versione semplificata che mantiene la logica originale ma centralizza
    la configurazione per facilitare modifiche future.
    """
    
    # Configurazione centralizzata dei costi
    COSTS = {
        "Mago": {"create": 20, "refund": 20},
        "Guerriero": {"create": 25, "refund": 25}, 
        "Ladro": {"create": 50, "refund": 50}
    }
    
    @staticmethod
    def credits_to_create(personaggio: Personaggio) -> int:
        """
        Restituisce il numero di crediti necessari per creare un personaggio.
        I costi cambiano a secondo della classe del personaggio che si vuole creare.
        ("Mago" costa 20 crediti, "Guerriero" 25 crediti, "Ladro" 50 crediti)
        
        Args:
            personaggio (Personaggio): oggetto della classe Personaggio
        Returns:
            int: crediti necessari alla creazione del personaggio
        """
        classe = personaggio.__class__.__name__
        
        if classe in CreditsManager.COSTS:
            cost = CreditsManager.COSTS[classe]["create"]
            credits_logger.info(f"Costo creazione {classe}: {cost} crediti")
            return cost
        else:
            raise ValueError(f"Classe del personaggio '{classe}' non riconosciuta.")
    
    @staticmethod
    def credits_to_refund(personaggio: Personaggio) -> int:
        """
        Restituisce il numero di crediti rimborsati all'utente in caso di cancellazione
        del personaggio. Il rimborso è un valore fisso in base alla classe del personaggio.
        ("Mago" rimborsa 20 crediti, "Guerriero" 25 crediti, "Ladro" 50 crediti)
        
        Args:
            personaggio (Personaggio): oggetto della classe Personaggio
        Returns:
            int: crediti rimborsati all'utente
        """
        classe = personaggio.__class__.__name__
        
        if classe in CreditsManager.COSTS:
            refund = CreditsManager.COSTS[classe]["refund"]
            credits_logger.info(f"Rimborso {classe}: {refund} crediti")
            return refund
        else:
            raise ValueError(f"Classe del personaggio '{classe}' non riconosciuta.")
    
    @staticmethod
    def validate_user_credits(user_credits: float, required_credits: int) -> bool:
        """
        Verifica se un utente ha crediti sufficienti.
        
        Args:
            user_credits (float): Crediti attuali dell'utente
            required_credits (int): Crediti richiesti
        Returns:
            bool: True se ha crediti sufficienti
        """
        return user_credits >= required_credits


# Backwards compatibility - mantieni le funzioni originali
def credits_to_create(personaggio: Personaggio) -> int:
    """Wrapper per compatibilità con codice esistente"""
    return CreditsManager.credits_to_create(personaggio)

def credits_to_refund(personaggio: Personaggio) -> int:
    """Wrapper per compatibilità con codice esistente"""
    return CreditsManager.credits_to_refund(personaggio)