from flask import Flask, request, jsonify
import sqlite3
import requests
from remplissage import  get_capteurs, get_mesures
from flask import Flask, render_template


app = Flask(__name__)
DATABASE = 'site.db'

# Fonction pour se connecter à la base de données
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permet de récupérer les données sous forme de dictionnaire
    return conn

    # Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/consommation')
def consommation():
    return render_template('consommation.html')


@app.route('/capteurs')
def capteurs():
    return render_template('capteurs.html')

@app.route('/economies')
def economies():
    return render_template('economies.html')

@app.route('/factures', methods=['GET'])
def factures_page():
    return render_template('factures.html')

#######################################################################
#### ONGLET CONSOMMATIONS 
@app.route('/api/consommations', methods=['GET'])
def get_consommations():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type_consommation, valeur, unite, date_consommation 
        FROM Consommation
    """)
    consommations = cursor.fetchall()
    conn.close()
    return jsonify([{"type": row[0], "valeur": row[1], "unite": row[2], "date": row[3]} for row in consommations])


@app.route('/api/economies/eau', methods=['GET'])
def get_economies_eau():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date_consommation, valeur
        FROM Consommation
        WHERE type_consommation = 'Eau'
        AND date_consommation BETWEEN '2024-12-01' AND '2024-12-31'
        ORDER BY date_consommation;
    """)
    result = cursor.fetchall()
    conn.close()

    # Formater les données en JSON
    mesures = [{"date": row[0], "valeur": row[1]} for row in result]
    return jsonify(mesures)

@app.route('/api/economies/electricite', methods=['GET'])
def get_electricity_consumption():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date_consommation, valeur
        FROM Consommation
        WHERE type_consommation = 'Electricité'
        AND date_consommation BETWEEN '2024-12-01' AND '2024-12-31'
        ORDER BY date_consommation;
    """)
    result = cursor.fetchall()
    conn.close()

    # Retourner les données sous forme de JSON
    return jsonify([{"date": row[0], "valeur": row[1]} for row in result])

@app.route('/api/january/eau', methods=['GET'])
def get_january_eau():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date_consommation, valeur
        FROM Consommation
        WHERE type_consommation = 'Eau'
        AND date_consommation BETWEEN '2025-01-01' AND '2025-01-16'
        ORDER BY date_consommation;
    """)
    result = cursor.fetchall()
    conn.close()

    # Formater les données en JSON
    mesures = [{"date": row[0], "valeur": row[1]} for row in result]
    return jsonify(mesures)

@app.route('/api/january/electricite', methods=['GET'])
def get_january_electricity():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date_consommation, valeur
        FROM Consommation
        WHERE type_consommation = 'Electricité'
        AND date_consommation BETWEEN '2025-01-01' AND '2025-01-16'
        ORDER BY date_consommation;
    """)
    result = cursor.fetchall()
    conn.close()

    # Formater les données en JSON
    mesures = [{"date": row[0], "valeur": row[1]} for row in result]
    return jsonify(mesures)

#######################################################################
############ ONGLET Capteurs


    # CAPTEUR DE CO2
@app.route('/api/capteurs/co2/parentale', methods=['GET'])
def get_co2_parentale():
    return get_sensor_data(4)

@app.route('/api/capteurs/co2/enfants', methods=['GET'])
def get_co2_enfants():
    return get_sensor_data(6)

@app.route('/api/capteurs/co2/cuisine', methods=['GET'])
def get_co2_cuisine():
    return get_sensor_data(8)

@app.route('/api/capteurs/co2/salon', methods=['GET'])
def get_co2_salon():
    return get_sensor_data(10)


@app.route('/api/capteurs/temp/parentale', methods=['GET'])
def get_temp_parentale():
    return get_sensor_data(5)

@app.route('/api/capteurs/temp/enfants', methods=['GET'])
def get_temp_enfants():
    return get_sensor_data(7)

@app.route('/api/capteurs/temp/cuisine', methods=['GET'])
def get_temp_cuisine():
    return get_sensor_data(9)

@app.route('/api/capteurs/temp/salon', methods=['GET'])
def get_temp_salon():
    return get_sensor_data(11)



def get_co2_data_for_room(piece_id):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date_mesure, valeur
        FROM Mesure
        WHERE capteur_id IN (
            SELECT id FROM Capteur WHERE piece_id = ?
        )
        ORDER BY date_mesure DESC LIMIT 10;
    """, (piece_id,))
    result = cursor.fetchall()
    conn.close()

    mesures = [{"date": row[0], "valeur": row[1]} for row in result]
    return jsonify(mesures)

def get_sensor_data(capteur_id):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT date_mesure, valeur
            FROM Mesure
            WHERE capteur_id = ?
            ORDER BY date_mesure DESC LIMIT 10;
        """, (capteur_id,))
        rows = cursor.fetchall()
        data = [{"date": row[0], "valeur": row[1]} for row in rows]
        return jsonify(data)
    except sqlite3.Error as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()


#######################################################################
############ ONGLET Economies
    
@app.route('/api/economies/decembre2024', methods=['GET'])
def get_economie_decembre2024():
    conn = sqlite3.connect('site.db')  # Utilisation de la base de données correcte
    cursor = conn.cursor()
    try:
        # Récupérer les consommations d'eau pour décembre 2024
        cursor.execute("""
            SELECT date_consommation, valeur
            FROM Consommation
            WHERE type_consommation = 'Eau'
            AND date_consommation BETWEEN '2024-12-01' AND '2024-12-31'
            ORDER BY date_consommation;
        """)
        rows = cursor.fetchall()

        # Formater les données pour le calcul des économies
        data = []
        for row in rows:
            date = row[0]
            consommation_reelle = row[1]
            consommation_sans_economiseur = consommation_reelle * 2  # Hypothèse sans économiseur
            data.append({
                "date": date,
                "consommation_reelle": consommation_reelle,
                "consommation_sans_economiseur": consommation_sans_economiseur
            })

        return jsonify(data)
    except sqlite3.Error as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()


@app.route('/api/consommation/electricite/decembre2024', methods=['GET'])
def get_electricite_decembre2024():
    conn = sqlite3.connect('site.db')  # Votre base de données
    cursor = conn.cursor()
    try:
        # Récupérer uniquement les consommations d'électricité pour décembre 2024
        cursor.execute("""
            SELECT date_consommation, valeur AS consommation_reelle
            FROM Consommation
            WHERE type_consommation = 'Electricité'
            AND date_consommation BETWEEN '2024-12-01' AND '2024-12-31'
            ORDER BY date_consommation;
        """)
        rows = cursor.fetchall()

        # Calculer consommation sans économiseur dans l'API
        data = []
        for row in rows:
            consommation_reelle = row[1]
            consommation_sans_economiseur = (consommation_reelle + 13.97) * 0.25  # Calcul correct
            data.append({
                "date": row[0],
                "consommation_reelle": consommation_reelle,
                "consommation_sans_economiseur": consommation_sans_economiseur
            })

        return jsonify(data)
    except sqlite3.Error as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()





#######################################################################
############ ONGLET Capteurs


@app.route('/api/factures', methods=['GET'])
def get_factures():
    conn = sqlite3.connect('site.db')  # Vérifiez le chemin de votre base
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT TypeFacture, montant, date_facture FROM Facture")
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({
                "type": row[0],
                "montant": row[1],
                "date": row[2]
            })
        return jsonify(data)
    except sqlite3.Error as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()



@app.route('/api/factures', methods=['POST'])
def add_facture():
    data = request.get_json()
    type_facture = data.get('type')
    montant = data.get('montant')
    date_facture = data.get('date')

    # Vérifiez que toutes les données nécessaires sont présentes
    if not all([type_facture, montant, date_facture]):
        return jsonify({"error": "Tous les champs sont requis (type, montant, date)."}), 400

    try:
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Facture (TypeFacture, montant, date_facture, logement_id)
            VALUES (?, ?, ?, 1)
        """, (type_facture, montant, date_facture))
        conn.commit()
        return jsonify({"message": "Facture ajoutée avec succès"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()








if __name__ == '__main__':
    print(app.url_map)

    app.run(host='0.0.0.0', port=5000, debug=True)






#### SOURCE 

##      https://www.youtube.com/watch?v=J9w-cir5a6U&list=PLMS9Cy4Enq5JAzNgWPK96HnkE_U7Ol3im     Graven-Developpement

##      https://www.youtube.com/watch?v=Q6jHYBnPsIg&list=PLuMW20nBgcbr6NyyY_d-76ujdG2-22WHU&index=4  Faiz Dev

##      https://www.youtube.com/watch?v=6hCGTJCo_Uo     Graven-Developpement CSS/HTML

###      https://www.youtube.com/watch?v=FdA1P7dY_18    METHODE GET/POST