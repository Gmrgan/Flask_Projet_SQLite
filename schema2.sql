-- Suppression des tables si elles existent
DROP TABLE IF EXISTS emprunts;
DROP TABLE IF EXISTS stocks;
DROP TABLE IF EXISTS livres;
DROP TABLE IF EXISTS utilisateurs;

-- Table des utilisateurs (anciennement clients)
CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    adresse TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'utilisateur')) NOT NULL DEFAULT 'utilisateur'
);

-- Table des livres
CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    genre TEXT NOT NULL,
    annee_publication INTEGER,
    isbn TEXT UNIQUE NOT NULL
);

-- Table de gestion des stocks
CREATE TABLE stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livre_id INTEGER NOT NULL,
    quantite INTEGER NOT NULL CHECK (quantite >= 0),
    FOREIGN KEY (livre_id) REFERENCES livres(id) ON DELETE CASCADE
);

-- Table des emprunts
CREATE TABLE emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    livre_id INTEGER NOT NULL,
    date_emprunt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_retour_prevu TIMESTAMP NOT NULL,
    date_retour_effectif TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (livre_id) REFERENCES livres(id) ON DELETE CASCADE
);
