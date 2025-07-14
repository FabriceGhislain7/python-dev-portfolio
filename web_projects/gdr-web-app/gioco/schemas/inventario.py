import uuid
from marshmallow import Schema, fields, post_load, EXCLUDE
from gioco.inventario import Inventario
from gioco.schemas.oggetto import OggettoSchema


class InventarioSchema(Schema):
    """
    Schema per la serializzazione/deserializzazione degli inventari.
    Utilizza Marshmallow per definire i campi e le loro proprietà.
    """
    class Meta:
        unknown = EXCLUDE

    id = fields.UUID(required=True)
    id_proprietario = fields.UUID(allow_none=True)
    oggetti = fields.List(fields.Nested(OggettoSchema), load_default=list)

    @post_load
    def make_inventario(self, data, **kwargs):
        return Inventario(**data)