import sqlite3
import os
import random
from random import uniform
from datetime import datetime, timedelta


# Connexion à la base de données
try:
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    print("Connexion à la base de données réussie.")
    print(f"Base de données utilisée : {os.path.abspath('site.db')}")
except sqlite3.Error as e:
    print(f"Erreur lors de la connexion à la base de données : {e}")
    exit()


# Fonction pour créer la table Logement
def create_table_logement():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Logement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adresse TEXT NOT NULL,
            telephone TEXT NOT NULL,
            ip TEXT NOT NULL
        );
        """)
        conn.commit()
        print("Table Logement créée avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la table Logement : {e}")

# Fonction pour créer la table Piece
def create_table_piece():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Piece (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            logement_id INTEGER NOT NULL,
            nom TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            z INTEGER NOT NULL,
            FOREIGN KEY (logement_id) REFERENCES Logement(id)
        );
        """)
        conn.commit()
        print("Table Piece créée avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la table Piece : {e}")

# Fonction pour créer la table TypeCapteur
def create_table_type_capteur():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TypeCapteur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TypeCapteur TEXT NOT NULL,
            unite_mesure TEXT NOT NULL,
            plage_precision TEXT NOT NULL
        );
        """)
        conn.commit()
        print("Table TypeCapteur créée avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la table TypeCapteur : {e}")

# Fonction pour créer la table Capteur
def create_table_capteur():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Capteur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            piece_id INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            reference_commerciale TEXT NOT NULL,
            port_communication TEXT NOT NULL,
            FOREIGN KEY (piece_id) REFERENCES Piece(id),
            FOREIGN KEY (type_id) REFERENCES TypeCapteur(id)
        );
        """)
        conn.commit()
        print("Table Capteur créée avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la table Capteur : {e}")



# Fonction pour créer la table Mesure
def create_table_mesure():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mesure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capteur_id INTEGER NOT NULL,
            date_mesure DATETIME DEFAULT CURRENT_TIMESTAMP, -- Ajout de la colonne date_mesure
            valeur REAL NOT NULL,
            FOREIGN KEY (capteur_id) REFERENCES Capteur(id)
        );
        """)
        conn.commit()
        print("Table Mesure créée avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la table Mesure : {e}")


# Fonction pour créer la table Facture
def create_table_facture():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Facture (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            logement_id INTEGER NOT NULL DEFAULT 1,
            TypeFacture TEXT NOT NULL,
            montant REAL NOT NULL,
            valeur_consomme REAL DEFAULT 0,
            date_facture DATE NOT NULL,
            FOREIGN KEY (logement_id) REFERENCES Logement(id)
        );
        """)
        conn.commit()
        print("Table Facture créée avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la table Facture : {e}")

# Création de la table Consommation
def create_table_consommation():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Consommation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_consommation TEXT NOT NULL, -- Type de consommation (électricité, eau, etc.)
            valeur REAL NOT NULL,            -- Valeur mesurée
            unite TEXT NOT NULL,             -- Unité de mesure (kWh, litres, etc.)
            date_consommation DATE NOT NULL, -- Date de la consommation
            logement_id INTEGER,             -- Référence au logement
            FOREIGN KEY (logement_id) REFERENCES Logement(id) -- Clé étrangère vers Logement
        );
        """)
        conn.commit()
        print("Table Consommation créée avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la table Consommation : {e}")
# Fonctions pour insérer les données

def insert_logement(adresse, telephone, ip):
    try:
        cursor.execute("""
            INSERT INTO Logement (adresse, telephone, ip) 
            VALUES (?, ?, ?)""", (adresse, telephone, ip))
        conn.commit()
        print(f"Logement ajouté : {adresse}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion du logement : {e}")

def insert_piece(logement_id, nom, x, y, z):
    try:
        cursor.execute("""
            INSERT INTO Piece (logement_id, nom, x, y, z)
            VALUES (?, ?, ?, ?, ?)""", (logement_id, nom, x, y, z))
        conn.commit()
        print(f"Pièce ajoutée : {nom}")
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion de la pièce : {e}")

def insert_type_capteur(TypeCapteur, unite_mesure, plage_precision):
    try:
        cursor.execute("""
            INSERT INTO TypeCapteur (TypeCapteur, unite_mesure, plage_precision)
            VALUES (?, ?, ?)""", (TypeCapteur, unite_mesure, plage_precision))
        conn.commit()
        print(f"Type de capteur ajouté : {TypeCapteur}")
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion du type de capteur : {e}")

def insert_capteur(piece_id, type_id, reference_commerciale, port_communication):
    try:
        cursor.execute("""
            INSERT INTO Capteur (piece_id, type_id, reference_commerciale, port_communication)
            VALUES (?, ?, ?, ?)""", (piece_id, type_id, reference_commerciale, port_communication))
        conn.commit()
        print(f"Capteur ajouté : {reference_commerciale}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion du capteur : {e}")

# Fonction pour insérer des mesures avec date_mesure
def insert_mesure(capteur_id, valeur, date_mesure):
    try:
        cursor.execute("""
            INSERT INTO Mesure (capteur_id, date_mesure, valeur)
            VALUES (?, ?, ?)""", (capteur_id, date_mesure, valeur))
        conn.commit()
        print(f"Mesure ajoutée pour capteur {capteur_id} : {date_mesure} : {valeur}")
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion de la mesure : {e}")

def insert_facture(logement_id, TypeFacture, montant, valeur_consomme, date_facture):
    try:
        cursor.execute("""
            INSERT INTO Facture (logement_id, TypeFacture, montant, valeur_consomme, date_facture)
            VALUES (?, ?, ?, ?, ?)""", (logement_id, TypeFacture, montant, valeur_consomme, date_facture))
        conn.commit()
        print(f"Facture ajoutée : {TypeFacture} - {montant}€ - {date_facture}")
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion de la facture : {e}")

# Fonction pour insérer des consommations
def insert_consommation(type_consommation, valeur, unite, date_consommation, logement_id):
    try:
        cursor.execute("""
            INSERT INTO Consommation (type_consommation, valeur, unite, date_consommation, logement_id)
            VALUES (?, ?, ?, ?, ?)""", (type_consommation, valeur, unite, date_consommation, logement_id))
        conn.commit()
        print(f"Consommation ajoutée : {type_consommation} - {valeur}{unite} - {date_consommation}")
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion dans la table Consommation : {e}")

def get_consommation():
    """Récupère les consommations (électricité, eau, déchets)"""
    try:
        cursor.execute("""
            SELECT TypeFacture, montant, valeur_consomme
            FROM Facture
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des consommations : {e}")
        return []

def get_capteurs():
    """Récupère les informations des capteurs et actionneurs"""
    try:
        cursor.execute("""
            SELECT Capteur.reference_commerciale, TypeCapteur.TypeCapteur, Piece.nom
            FROM Capteur
            JOIN TypeCapteur ON Capteur.type_id = TypeCapteur.id
            JOIN Piece ON Capteur.piece_id = Piece.id
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des capteurs : {e}")
        return []

def get_mesures():
    """Récupère les mesures enregistrées par les capteurs"""
    try:
        cursor.execute("""
            SELECT Capteur.reference_commerciale, Mesure.valeur
            FROM Mesure
            JOIN Capteur ON Mesure.capteur_id = Capteur.id
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des mesures : {e}")
        return []


# Fonction pour générer des mesures pour les capteurs de CO2
def generate_co2_measures(capteur_id, days=1, interval_minutes=5):
    start_date = datetime(2025, 1, 16)
    for i in range(0, days * 24 * 60, interval_minutes):
        date_mesure = (start_date + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')
        valeur = uniform(500, 950)  # Générer une valeur entre 500 et 950 ppm
        insert_mesure(capteur_id, valeur, date_mesure)

# Fonction pour générer des mesures pour n'importe quel capteur
def generate_measures(capteur_id, min_val, max_val, days=1, interval_minutes=5):
    start_date = datetime(2025, 1, 16)
    for i in range(0, days * 24 * 60, interval_minutes):
        date_mesure = (start_date + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')
        valeur = uniform(min_val, max_val)  # Générer une valeur entre min_val et max_val
        insert_mesure(capteur_id, valeur, date_mesure)

# Remplissage de la base avec des données
try:
    # Creation des tables
    create_table_logement()
    create_table_piece()
    create_table_type_capteur()
    create_table_capteur()
    create_table_mesure()
    create_table_facture()
    create_table_consommation()
    print("Toutes les tables ont été créées avec succès.")
    # Ajout d'un logement
    logement_id = insert_logement('14 Rue Candale', '0123456789', '172.20.10.14')

    # Ajout de pièces
    insert_piece(logement_id, 'Salon', 0, 0, 0)
    insert_piece(logement_id, 'Cuisine', 0, 1, 0)
    insert_piece(logement_id, 'Chambre parentale', 0, 2, 0)
    insert_piece(logement_id, 'Chambre des enfants', 0, 3, 0)

    # Ajout de types de capteurs
    insert_type_capteur('Temperature','°C', '0-100')
    insert_type_capteur('Electricite','kWh', '0-1000')

    # Ajout de capteurs/actionneurs
    capteur1_id = insert_capteur(1, 1, 'Capteur de temperature', 'COM1')
    capteur2_id = insert_capteur(2, 2, 'Compteur electrique', 'COM2')
    capteur3_id = insert_capteur(3, 2, 'Compteur litres eau', 'COM3')


    # Ajout de mesures
    """ insert_mesure(capteur1_id, 22.5)
    insert_mesure(capteur1_id, 23.1) 
    insert_mesure(capteur2_id, 15.2)
    insert_mesure(capteur2_id, 15.8) """

    # Ajout de factures avec des dates
    date_facture = '2025-01-01'

    insert_facture(logement_id, 'Gaz', 60.5, 80, date_facture)
    insert_facture(logement_id, 'Netflix', 10.99, 1, date_facture)
    insert_facture(logement_id, 'Internet', 49.99, 1, date_facture)
    insert_facture(logement_id, 'Uber Eats', 84.7, 5, date_facture)
    insert_facture(logement_id, 'Forfait Mobile Bouygues', 13.99, 1, date_facture)
    insert_facture(logement_id, 'Forfait Fibre + Télé Bouygues', 53.99, 1, date_facture)
    



    

    # Fonction pour générer 31 mesures aléatoires pour capteur3_id

    capteur3_id = 3  # Assurez-vous que cet ID correspond au capteur "Compteur litres eau"
    start_date = datetime(2024, 12, 1)
    for i in range(31):
        date_mesure = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        valeur = random.uniform(140, 160)  # Générer une valeur aléatoire entre 140 et 160
        cursor.execute("""
            INSERT INTO Mesure (capteur_id, valeur)
            VALUES (?, ?)""", (capteur3_id, valeur))

        cursor.execute("""
            INSERT INTO Consommation (type_consommation, valeur, unite, date_consommation, logement_id)
            VALUES (?, ?, ?, ?, ?)""", ('Eau', valeur, 'L', date_mesure, 1))

    conn.commit()
    print("31 mesures pour le capteur conso eau ont été ajoutées avec succès.")

    capteur2_id = 2  
    start_date = datetime(2024, 12, 1)
    for i in range(31):
        date_mesure = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        valeur = random.uniform(50, 60)  # Générer une valeur aléatoire entre 50 et 60
        cursor.execute("""
            INSERT INTO Mesure (capteur_id, valeur)
            VALUES (?, ?)""", (capteur2_id, valeur))

        cursor.execute("""
            INSERT INTO Consommation (type_consommation, valeur, unite, date_consommation, logement_id)
            VALUES (?, ?, ?, ?, ?)""", ('Electricité', valeur, 'kWh', date_mesure, 1))

    conn.commit()
    print("31 mesures pour le compteur electrique ont été ajoutées avec succès.")


# POUR JANVIER 2025

    capteur3_id = 3  # Assurez-vous que cet ID correspond au capteur "Compteur litres eau"
    start_date = datetime(2025, 1, 1)
    for i in range(16):
        date_mesure = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        valeur = random.uniform(140, 160)  # Générer une valeur aléatoire entre 140 et 160
        cursor.execute("""
            INSERT INTO Mesure (capteur_id, valeur)
            VALUES (?, ?)""", (capteur3_id, valeur))

        cursor.execute("""
            INSERT INTO Consommation (type_consommation, valeur, unite, date_consommation, logement_id)
            VALUES (?, ?, ?, ?, ?)""", ('Eau', valeur, 'L', date_mesure, 1))

    conn.commit()
    print("16 mesures pour le capteur conso eau ont été ajoutées avec succès.")

    capteur2_id = 2  
    start_date = datetime(2025, 1, 1)
    for i in range(16):
        date_mesure = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        valeur = random.uniform(50, 60)  # Générer une valeur aléatoire entre 50 et 60
        cursor.execute("""
            INSERT INTO Mesure (capteur_id, valeur)
            VALUES (?, ?)""", (capteur2_id, valeur))

        cursor.execute("""
            INSERT INTO Consommation (type_consommation, valeur, unite, date_consommation, logement_id)
            VALUES (?, ?, ?, ?, ?)""", ('Electricité', valeur, 'kWh', date_mesure, 1))

    conn.commit()
    print("16 mesures pour le compteur electrique ont été ajoutées avec succès.")


#################################
################################
#################################
################################
################################
###############################
#################################
################################
#################################
################################
################################
###############################
#################################
################################
#################################
################################
################################
###############################

    # CAPTEUR DE CO2 et temperature

# Ajout du type de capteur CO2 (s'il n'est pas déjà présent)
    # Ajout du type de capteur CO2 (s'il n'est pas déjà présent)
    insert_type_capteur('CO2', 'ppm', '500-950')
    insert_type_capteur('Température', '°C', '20-25')

    # Ajout des capteurs pour chaque pièce
    capteur_co2_parentale_id = insert_capteur(4, 3, 'Capteur CO2 Chambre Parentale', 'COM5')
    capteur_temp_parentale_id = insert_capteur(5, 4, 'Capteur Température Chambre Parentale', 'COM6')

    capteur_co2_enfants_id = insert_capteur(6, 3, 'Capteur CO2 Chambre Enfants', 'COM7')
    capteur_temp_enfants_id = insert_capteur(7, 4, 'Capteur Température Chambre Enfants', 'COM8')

    capteur_co2_cuisine_id = insert_capteur(8, 3, 'Capteur CO2 Cuisine', 'COM9')
    capteur_temp_cuisine_id = insert_capteur(9, 4, 'Capteur Température Cuisine', 'COM10')

    capteur_co2_salon_id = insert_capteur(10, 3, 'Capteur CO2 Salon', 'COM11')
    capteur_temp_salon_id = insert_capteur(11, 4, 'Capteur Température Salon', 'COM12')

    # Génération des données pour chaque capteur de CO2 et Température
    generate_measures(capteur_co2_parentale_id, 500, 950, days=1)
    generate_measures(capteur_temp_parentale_id, 20, 25, days=1)

    generate_measures(capteur_co2_enfants_id, 500, 950, days=1)
    generate_measures(capteur_temp_enfants_id, 20, 25, days=1)

    generate_measures(capteur_co2_cuisine_id, 500, 950, days=1)
    generate_measures(capteur_temp_cuisine_id, 20, 25, days=1)

    generate_measures(capteur_co2_salon_id, 500, 950, days=1)
    generate_measures(capteur_temp_salon_id, 20, 25, days=1)

    conn.commit()
    print("Toutes les données pour CAPTEUR DE CO2 et temperature ont été insérées avec succès.")



    print("Toutes les données ont été insérées avec succès.")


except Exception as e:
    print(f"Erreur inattendue : {e}")
finally:
    conn.close()
    print("Connexion à la base fermée.")
