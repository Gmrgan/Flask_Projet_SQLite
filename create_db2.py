import sqlite3

# Connexion à la base de données
connection = sqlite3.connect('database.db')

# Création des tables depuis schema.sql
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insertion d'utilisateurs (anciens clients) avec rôles
users = [
    ('DUPONT', 'Emilie', '123, Rue des Lilas, 75001 Paris', 'emilie.dupont@email.com', 'pass123', 'utilisateur'),
    ('LEROUX', 'Lucas', '456, Avenue du Soleil, 31000 Toulouse', 'lucas.leroux@email.com', 'pass456', 'utilisateur'),
    ('MARTIN', 'Amandine', '789, Rue des Érables, 69002 Lyon', 'amandine.martin@email.com', 'pass789', 'admin'),
    ('TREMBLAY', 'Antoine', '1010, Boulevard de la Mer, 13008 Marseille', 'antoine.tremblay@email.com', 'passabc', 'utilisateur'),
    ('LAMBERT', 'Sarah', '222, Avenue de la Liberté, 59000 Lille', 'sarah.lambert@email.com', 'passdef', 'utilisateur')
]

cur.executemany("INSERT INTO utilisateurs (nom, prenom, adresse, email, mot_de_passe, role) VALUES (?, ?, ?, ?, ?, ?)", users)

# Insertion de livres
books = [
    ('Les Misérables', 'Victor Hugo', 'Roman', 1862, '978-2-070-10170-5'),
    ('1984', 'George Orwell', 'Science-fiction', 1949, '978-0-452-28423-4'),
    ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Conte', 1943, '978-2-07-040850-4'),
    ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', 'Fantasy', 1997, '978-0-7475-3269-6'),
    ('La Peste', 'Albert Camus', 'Philosophie', 1947, '978-2-07-036042-9')
]

cur.executemany("INSERT INTO livres (titre, auteur, genre, annee_publication, isbn) VALUES (?, ?, ?, ?, ?)", books)

# Initialisation du stock
stock = [
    (1, 5),  # 5 exemplaires du livre 1
    (2, 3),  # 3 exemplaires du livre 2
    (3, 4),  # 4 exemplaires du livre 3
    (4, 2),  # 2 exemplaires du livre 4
    (5, 6)   # 6 exemplaires du livre 5
]

cur.executemany("INSERT INTO stocks (livre_id, quantite) VALUES (?, ?)", stock)

# Simuler un emprunt
emprunts = [
    (1, 2, '2025-03-10 10:00:00', '2025-03-25 10:00:00', None),  # Emilie emprunte "1984"
    (2, 4, '2025-03-12 14:00:00', '2025-03-27 14:00:00', None)   # Lucas emprunte "Harry Potter"
]

cur.executemany("INSERT INTO emprunts (utilisateur_id, livre_id, date_emprunt, date_retour_prevu, date_retour_effectif) VALUES (?, ?, ?, ?, ?)", emprunts)

# Commit et fermeture de la connexion
connection.commit()
connection.close()
