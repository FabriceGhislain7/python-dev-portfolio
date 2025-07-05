from gioco.personaggio import Personaggio
from gioco.classi import Mago, Guerriero, Ladro

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
    if classe == "Mago":
        return 20
    elif classe == "Guerriero":
        return 25
    elif classe == "Ladro":
        return 50
    else:
        raise ValueError("Classe del personaggio {personaggio.nome} non riconosciuta.")


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
    if classe == "Mago":
        return 20
    elif classe == "Guerriero":
        return 25
    elif classe == "Ladro":
        return 50
    else:
        raise ValueError("Classe del personaggio '{personaggio.nome}' non riconosciuta.")
