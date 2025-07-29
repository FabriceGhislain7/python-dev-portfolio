from marshmallow import Schema, fields, post_load
from gioco.strategy import StrategiaFactory

class StrategiaSchema(Schema):
    '''
    Classe per la serializzazione e deserializzazione delle strategie.
    Utilizza Marshmallow per convertire le istanze di Strategia in formato JSON
    e viceversa.
    '''
    nome = fields.Str(required=True)

    @post_load
    def make_strategia(self, data, **kwargs):
        return StrategiaFactory.usa_strategia(data['nome'])