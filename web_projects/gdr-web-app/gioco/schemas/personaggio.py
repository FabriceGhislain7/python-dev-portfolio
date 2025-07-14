from marshmallow import Schema, fields, post_load
import uuid

from gioco.personaggio import Personaggio


def get_all_subclasses(cls):
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        # subclasses.update(get_all_subclasses(subclass))
        # nel caso di sottoclassi indirette
    return subclasses


class PersonaggioSchema(Schema):
    """
    Schema per la serializzazione/deserializzazione dei personaggi.
    Utilizza Marshmallow per definire i campi e le loro proprietà.
    """
    classe = fields.String(required=True)
    id = fields.UUID(load_default=lambda: uuid.uuid4())
    nome = fields.String(required=True)
    npc = fields.Boolean(load_default=True)
    salute_max = fields.Integer()
    salute = fields.Integer()
    attacco_min = fields.Integer()
    attacco_max = fields.Integer()
    livello = fields.Integer(load_default=1)
    destrezza = fields.Integer(load_default=15)
    storico_danni_subiti = fields.List(fields.Integer(), load_default=list)

    @post_load
    def make_personaggio(self, data, **_kwargs):
        print(f"\nimport: \n{data}\n")
        # Crea la mappa dinamica: nome classe -> classe Python
        classe_nome = data.get("classe")
        classe_map = {
            subcls.__name__: subcls
            for subcls in get_all_subclasses(Personaggio)
        }

        personaggio_cls = classe_map[classe_nome]
        return personaggio_cls(**data)


class MagoSchema(PersonaggioSchema):
    """
    Schema specifico per la classe Mago.
    Estende PersonaggioSchema e aggiunge il campo 'mana'.
    """


class LadroSchema(PersonaggioSchema):
    """
    Schema specifico per la classe Ladro.
    Estende PersonaggioSchema e aggiunge il campo 'destrezza'.
    """
    pass


class GuerrieroSchema(PersonaggioSchema):
    """
    Schema specifico per la classe Guerriero.
    Estende PersonaggioSchema e aggiunge il campo 'forza'.
    """
    pass