import sqlite3
import os

# Connexion à la base de données
try:
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    print("Connexion à la base de données réussie.")
    print(f"Base de données utilisée : {os.path.abspath('site.db')}")
except sqlite3.Error as e:
    print(f"Erreur lors de la connexion à la base de données : {e}")
    exit()

# Fonction pour supprimer toutes les tables
def drop_all_tables():
    try:
        # Récupérer la liste des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        # Supprimer chaque table
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
            print(f"Table supprimée : {table[0]}")
        conn.commit()
        print("Toutes les tables ont été supprimées avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression des tables : {e}")

# Supprimer les tables
try:
    drop_all_tables()
except Exception as e:
    print(f"Erreur inattendue : {e}")
finally:
    conn.close()
    print("Connexion à la base fermée.")
