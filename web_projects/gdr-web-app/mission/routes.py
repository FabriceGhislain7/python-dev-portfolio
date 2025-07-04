from . import mission_bp
from flask import render_template, request, session, redirect, url_for
from gioco.missione import GestoreMissioni

@mission_bp.route('/select_mission', methods=['GET', 'POST'])
def select_mission():
    missioni = GestoreMissioni.lista_missioni()
    if request.method == 'POST':
        missione_id = request.form['missione_id']
        lista_missioni = session.get('missioni', [])
        for missione in lista_missioni:
            if missione_id == missione.id:
                missione_sel = missione
                break
        return redirect(url_for('gioco.menu', missione_sel=missione_sel))

    return render_template('select_mission.html', missioni=missioni)

@mission_bp.route('/missioni')
def mostra_missioni():
    missioni = GestoreMissioni.lista_missioni
    return render_template('missioni.html', missioni=missioni)


@mission_bp.route('/missione/attiva')
def missione_attiva():
    missione = GestoreMissioni.sorteggia()
    if missione:
        return render_template('missione_attiva.html', missione=missione)
    return "Non ci sono missioni attive o disponibili."


@mission_bp.route('/missioni/stato')
def stato_missioni():
    complete = GestoreMissioni.finita()
    return f"Tutte le missioni completate: {complete}"
