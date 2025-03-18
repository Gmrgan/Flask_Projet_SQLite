from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Vérifie si un utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')

# Vérifie si l'utilisateur est un "utilisateur" (non admin)
def est_utilisateur():
    return session.get('role') == 'utilisateur'

# Vérifie si l'utilisateur est un administrateur
def est_admin():
    return session.get('role') == 'admin'

@app.route('/')
def home():
    return render_template('hello.html')

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, role, mot_de_passe FROM utilisateurs WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['authentifie'] = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[2]
            return redirect(url_for('dashboard'))
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return f"<h2>Bienvenue {session['username']}, vous êtes connecté en tant que {session['role']}.</h2>"

@app.route('/livres')
def liste_livres():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livres")
    livres = cursor.fetchall()
    conn.close()
    return render_template('liste_livres.html', livres=livres)

@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if not est_authentifie() or not est_admin():
        return "<h2>Accès interdit. Seuls les administrateurs peuvent ajouter des livres.</h2>", 403

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre = request.form['genre']
        annee = request.form['annee']
        isbn = request.form['isbn']
        quantite = request.form['quantite']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO livres (titre, auteur, genre, annee_publication, isbn) VALUES (?, ?, ?, ?, ?)",
                       (titre, auteur, genre, annee, isbn))
        cursor.execute("INSERT INTO stocks (livre_id, quantite) VALUES (last_insert_rowid(), ?)", (quantite,))
        conn.commit()
        conn.close()

        return redirect(url_for('liste_livres'))

    return render_template('formulaire_livre.html')

@app.route('/emprunter/<int:livre_id>')
def emprunter_livre(livre_id):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    user_id = session['user_id']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Vérifier la disponibilité du livre
    cursor.execute("SELECT quantite FROM stocks WHERE livre_id = ?", (livre_id,))
    stock = cursor.fetchone()

    if stock and stock[0] > 0:
        cursor.execute("INSERT INTO emprunts (utilisateur_id, livre_id, date_emprunt, date_retour_prevu) VALUES (?, ?, datetime('now'), datetime('now', '+14 days'))", 
                       (user_id, livre_id))
        cursor.execute("UPDATE stocks SET quantite = quantite - 1 WHERE livre_id = ?", (livre_id,))
        conn.commit()
    else:
        conn.close()
        return "<h2>Ce livre n'est plus disponible.</h2>", 400

    conn.close()
    return redirect(url_for('liste_livres'))

@app.route('/retourner/<int:emprunt_id>')
def retourner_livre(emprunt_id):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Récupérer le livre concerné
    cursor.execute("SELECT livre_id FROM emprunts WHERE id = ?", (emprunt_id,))
    emprunt = cursor.fetchone()

    if emprunt:
        cursor.execute("UPDATE emprunts SET date_retour_effectif = datetime('now') WHERE id = ?", (emprunt_id,))
        cursor.execute("UPDATE stocks SET quantite = quantite + 1 WHERE livre_id = ?", (emprunt[0],))
        conn.commit()

    conn.close()
    return redirect(url_for('mes_emprunts'))

@app.route('/mes_emprunts')
def mes_emprunts():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    user_id = session['user_id']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT e.id, l.titre, e.date_emprunt, e.date_retour_prevu, e.date_retour_effectif FROM emprunts e JOIN livres l ON e.livre_id = l.id WHERE e.utilisateur_id = ?", (user_id,))
    emprunts = cursor.fetchall()
    conn.close()

    return render_template('mes_emprunts.html', emprunts=emprunts)

if __name__ == "__main__":
    app.run(debug=True)
