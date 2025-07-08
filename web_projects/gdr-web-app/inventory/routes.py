from . import inventory_bp
from flask import render_template, request, session, redirect, url_for, flash
from gioco.oggetto import BombaAcida, Medaglione, Oggetto, PozioneCura
from gioco.personaggio import Personaggio
from gioco.classi import Ladro, Mago, Guerriero
from gioco.inventario import Inventario
from utils.messaggi import Messaggi
from utils.log import Log

@inventory_bp.route('/inventory', methods=['GET', 'POST'])
def mostra_inventario():
    # Recupera i dati dalla sessione
    personaggi = session.get('personaggi', [])
    inventari_raw = session.get('inventari', [])

    # Ricostruisce gli oggetti Inventario da dizionari
    inventari = [Inventario.from_dict(inv) for inv in inventari_raw ]

    # Mappa id → nome personaggio
    nome_per_id = {p['id']: p['nome'] for p in personaggi}

    # Recupera l'id del personaggio selezionato (GET o POST)
    id_personaggio = (
        request.form.get('personaggio_id')
        if request.method == 'POST'
        else request.args.get('personaggio_id')
    )

    personaggio = next((p for p in personaggi if p['id'] == id_personaggio), None)
    inventario = next((inv for inv in inventari if str(inv.id_proprietario) == id_personaggio), None)

    if id_personaggio and personaggio and inventario:
        Log.scrivi_log(f"Inventario di {nome_per_id[id_personaggio]} selezionato.")

    return render_template(
        'inventory.html',
        personaggi=personaggi,
        nome_per_id=nome_per_id,
        id_personaggio=id_personaggio,
        personaggio=personaggio,
        inventario=inventario
    )
