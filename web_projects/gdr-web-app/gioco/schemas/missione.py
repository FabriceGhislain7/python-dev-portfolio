import json
import os
import uuid
from marshmallow import Schema, fields, post_load

from gioco.ambiente import AmbienteSchema
from gioco.missione import GestoreMissioni, Missione
from gioco.schemas.oggetto import OggettoSchema
from gioco.schemas.personaggio import PersonaggioSchema
from gioco.schemas.strategy import StrategiaSchema


class MissioniSchema(Schema):
    id = fields.UUID(load_default=lambda: uuid.uuid4())
    nome = fields.String(required=True)
    ambiente = fields.Nested(AmbienteSchema, required=True)
    nemici = fields.List(fields.Nested(PersonaggioSchema), required=True)
    premi = fields.List(fields.Nested(OggettoSchema), required=True)
    strategia_nemici = fields.Nested(StrategiaSchema, allow_none=True)
    completata = fields.Bool()
    attiva = fields.Bool()

    @post_load
    def make_Missioni(self, data, **kwargs) -> Missione:
        return Missione(**data)


class GestoreMissioniSchema(Schema):
    lista_missioni = fields.List(fields.Nested(MissioniSchema), required=True)

    @post_load
    def make_GestoreMissioni(self, data, **kwargs):
        gm = GestoreMissioni()
        gm.lista_missioni = data['lista_missioni']
        return gm

    def prendi_Missione_Da_Json(self):
        lista = []
        schema = MissioniSchema()
        routes = r"static\json\missions"
        for files in os.listdir(routes):
            if files.endswith(".json"):
                with open(os.path.join(routes, files), 'r') as file:
                    data = json.load(file)
                    missione = schema.load(data)
                    lista.append(missione)
        nuovo = GestoreMissioni()
        nuovo.lista_missioni = lista
        return nuovo