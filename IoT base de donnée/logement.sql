 -- Question 1 

-- Voir modele sur tablette

-- Question 2 
-- Suppression des tables existantes

DROP TABLE IF EXISTS Logement;
DROP TABLE IF EXISTS Piece;
DROP TABLE IF EXISTS Capteur;
DROP TABLE IF EXISTS Mesure;
DROP TABLE IF EXISTS TypeCapteur;
DROP TABLE IF EXISTS Facture;


-- Question 3

-- Table Logement
CREATE TABLE Logement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adresse TEXT NOT NULL,  -- adresse du logement
    telephone TEXT,  -- numero de telephone du logement
    ip TEXT, -- adresse IP
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- date d'insertion dans la base de données
);

-- Table Piece
CREATE TABLE Piece (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    logement_id INTEGER,
    nom TEXT,  -- nom de la piece
    x INTEGER,
    y INTEGER,    -- coordonees x,y,z de la matrice pour situer la piece dans le logement
    z INTEGER,
    FOREIGN KEY (logement_id) REFERENCES Logement(id) -- association pour avoir l'id du logement
);

-- Table TypeCapteur
CREATE TABLE TypeCapteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    TypeCapteur TEXT, 
    unite_mesure TEXT,  -- unite de mesure du capteur
    plage_precision TEXT -- plage de precision du capteur
);

-- Table Capteur
CREATE TABLE Capteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    piece_id INTEGER,  -- variable afin de pouvoir faire la foreign key piece id
    type_id INTEGER,    -- variable afin de pouvoir faire la foreign key type capteur id
    reference_commerciale TEXT,  -- reference commerciale du capteur
    port_communication TEXT,  -- port COM du capteur
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- date d'insertion de la data
    FOREIGN KEY (piece_id) REFERENCES Piece(id), -- on recupere l'id de la table Piece
    FOREIGN KEY (type_id) REFERENCES TypeCapteur(id) -- on recupere l'id de la table type capteur
);

-- Table Mesure
CREATE TABLE Mesure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    capteur_id INTEGER, -- variable afin de pouvoir faire la foreign key capteur id
    valeur REAL, -- valeur de la mesure
    date_mesure TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- date d'insertion de la data
    FOREIGN KEY (capteur_id) REFERENCES Capteur(id) -- on recupere l'id de la table capteur
);

-- Table Facture
CREATE TABLE Facture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    TypeFacture TEXT,   -- type de la facture (elec,eau,...)
    --logement_id INTEGER, -- -- variable afin de pouvoir faire la foreign key logement id
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- date d'insertion de la data
    date_facture TEXT,
    montant REAL, -- montant de la facture
    valeur_consomme REAL, -- valeur consommée de la facture (ex: nbr de watt/h facture electricite)
    FOREIGN KEY (logement_id) REFERENCES Logement(id) -- on recupere l'id de la table logement
);

-- Table Consommation
CREATE TABLE Consommation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_consommation TEXT NOT NULL, -- Type de consommation (électricité, eau, etc.)
    valeur REAL NOT NULL,            -- Valeur mesurée
    unite TEXT NOT NULL,             -- Unité de mesure (kWh, litres, etc.)
    date_consommation DATE NOT NULL, -- Date de la consommation
    logement_id INTEGER,             -- Référence au logement
    FOREIGN KEY (logement_id) REFERENCES Logement(id) -- Clé étrangère vers Logement
);


-- Question 4 

-- Insertion d'un logement
INSERT INTO Logement (adresse, telephone, ip) VALUES ('14 Rue Candale', '0103050709', '172.20.10.14');

-- Insertion de 4 pièces dans le logement
INSERT INTO Piece (logement_id, nom, x, y, z) VALUES (1,'Salon', 0, 0, 0);
INSERT INTO Piece (logement_id, nom, x, y, z) VALUES (1,'Chambre', 1, 0, 0);
INSERT INTO Piece (logement_id, nom, x, y, z) VALUES (1,'Cuisine', 2, 0, 0);
INSERT INTO Piece (logement_id, nom, x, y, z) VALUES (1,'Salle de bain', 3, 0, 0);


-- Question 5 

-- Insertion de types de capteurs/actionneurs
INSERT INTO TypeCapteur (unite_mesure, plage_precision) VALUES ('°C', '0-100');
INSERT INTO TypeCapteur (unite_mesure, plage_precision) VALUES ('kWh', '0-1000');
INSERT INTO TypeCapteur (unite_mesure, plage_precision) VALUES ('Lux', '0-10000');
INSERT INTO TypeCapteur (unite_mesure, plage_precision) VALUES ('Personnes', '0-10');


-- Question 6 

INSERT INTO Capteur (piece_id, type_id, reference_commerciale, port_communication) VALUES (1, 1, 'Capteur de temperature', 'COM1');
INSERT INTO Capteur (piece_id, type_id, reference_commerciale, port_communication) VALUES (2, 2, 'Compteur electrique', 'COM2');

-- Question 7

-- Mesures pour le premier capteur
INSERT INTO Mesure (capteur_id, valeur) VALUES (1, 22.5);
INSERT INTO Mesure (capteur_id, valeur) VALUES (1, 23.1);

-- Mesures pour le deuxieme capteur
INSERT INTO Mesure (capteur_id, valeur) VALUES (2, 30.5);
INSERT INTO Mesure (capteur_id, valeur) VALUES (2, 41.8);

-- Question 8 

INSERT INTO Facture (logement_id, TypeFacture, montant, valeur_consomme) VALUES (1, 'Electricite', 45.6, 100);
INSERT INTO Facture (logement_id, TypeFacture, montant, valeur_consomme) VALUES (1, 'Eau', 30.2, 50);
INSERT INTO Facture (logement_id, TypeFacture, montant, valeur_consomme) VALUES (1, 'Dechets', 15.0, 20);
INSERT INTO Facture (logement_id, TypeFacture, montant, valeur_consomme) VALUES (1, 'Gaz', 60.5, 80);


