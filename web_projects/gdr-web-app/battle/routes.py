from flask import render_template, session
from . import battle_bp
from gioco.personaggio import Personaggio
from gioco.inventario import Inventario
from gioco.ambiente import Ambiente,Foresta
from gioco.missione import Missione,GestoreMissioni
@battle_bp.route('/begin_battle')
def begin_battle():
    #if request.method == 'POST':

    #prendo i dati da sessione :
    personaggi=[]
    inventari=[]
    ambiente = Foresta()
    gestore_missioni = GestoreMissioni()
    missione_corrente = gestore_missioni.sorteggia()
    if 'ambiente' in session :
        #Recupero l'oggetto ambiente dalla sessione deserializzandolo
        ambiente = Ambiente.from_dict(session['ambiente'])
    if 'personaggi' in session and 'inventari' in session:
        pg_list = session.get('personaggi', [])
        inv_list = session.get('inventari',  [])
        #Deserializzo gli elementi delle liste
        for serialized in  pg_list :
            personaggi.append(Personaggio.from_dict(serialized))
        for serialized in inv_list:
            inventari.append(Inventario.from_dict(serialized))
        #Ora le liste personaggi e  inventari contengono i dati deserializzati

    return render_template('begin_battle.html', personaggi=personaggi, inventari=inventari, ambiente_corrente = ambiente, missione_corrente = missione_corrente)