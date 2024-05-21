import sqlite3
import requests

# Création des tables si elles n'existent pas déjà
def create_database():
    try:
        connexion = sqlite3.connect('db/sales_db.db')
        c = connexion.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS Magasins (
            ID_Magasin INTEGER PRIMARY KEY,
            Nombre_de_salaries INTEGER,
            Ville TEXT
        )''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS Produits (
            ID_Reference_Produit TEXT PRIMARY KEY,
            Nom TEXT,
            Prix REAL,
            Stock INTEGER
        )''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS Ventes (
            ID_Vente INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT,
            ID_Reference_Produit TEXT,
            Quantite INTEGER,
            ID_Magasin INTEGER,
            FOREIGN KEY (ID_Reference_Produit) REFERENCES Produits(ID_Reference_Produit),
            FOREIGN KEY (ID_Magasin) REFERENCES Magasins(ID_Magasin)
        )''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS Analyses (
            ID_Analyse INTEGER PRIMARY KEY AUTOINCREMENT,
            Type_Analyse TEXT,
            Resultat TEXT
        )''')

        connexion.commit()
        connexion.close()

        print("Database and tables created successfully.\n")
    except Exception as error:
        print(f"An error occurred while creating the database: {error}\n")
    
    return

# Ajout des underscores pour remplacer les espaces dans les noms de colonnes
def modify_column_names(original_names):
    return [name.replace(' ', '_') for name in original_names]

# Récupération des données sur un server
def fetch_and_load_data(url, table):
    try:
        response = requests.get(url)
        data = response.json()
        connexion = sqlite3.connect('db/sales_db.db')
        c = connexion.cursor()

        if table == 'Ventes':
            for item in data:
                columns = 'Date, ID_Magasin, ID_Reference_Produit, Quantite'
                placeholders = ', '.join(['?'] * 4)
                values_tuple = (item['Date'], item['ID Magasin'], item['ID Reference produit'], item['Quantite'])
                c.execute(f'INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})', values_tuple)
        else:
            for item in data:
                original_columns = list(item.keys())
                renamed_columns = modify_column_names(original_columns)
                columns = ', '.join([f'"{k}"' for k in renamed_columns])
                placeholders = ', '.join(['?'] * len(item))
                values_tuple = tuple(item.values())
                c.execute(f'INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})', values_tuple)

        connexion.commit()
        print(f"Data successfully loaded into {table}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        connexion.close()
    return

def perform_analyses():
    try:
        connexion = sqlite3.connect('db/sales_db.db')
        c = connexion.cursor()
        
         # Vider la table Analyses avant de commencer les nouvelles analyses
        c.execute('DELETE FROM Analyses')
        print("Previous analysed data cleared.")

        # Analyse 1: Revenu total
        query_total_revenue = '''
        SELECT SUM(Ventes.Quantite * Produits.Prix) AS Total_Revenue
        FROM Ventes
        JOIN Produits ON Ventes.ID_Reference_Produit = Produits.ID_Reference_Produit
        '''
        total_revenue = c.execute(query_total_revenue).fetchone()[0]
        if total_revenue is not None:
            c.execute('INSERT INTO Analyses (Type_Analyse, Resultat) VALUES (?, ?)', 
                      ('Total Revenue', str(total_revenue)))
        else:
            print("No data available to calculate total revenue.")

        # Analyse 2: Ventes par produit
        query_sales_by_product = '''
        SELECT Produits.Nom, SUM(Ventes.Quantite * Produits.Prix) AS Revenue
        FROM Ventes
        JOIN Produits ON Ventes.ID_Reference_Produit = Produits.ID_Reference_Produit
        GROUP BY Produits.Nom
        '''
        products_revenue = c.execute(query_sales_by_product).fetchall()
        for product, revenue in products_revenue:
            c.execute('INSERT INTO Analyses (Type_Analyse, Resultat) VALUES (?, ?)', 
                      (f'Revenue for {product}', str(revenue)))

        # Analyse 3: Ventes par region
        query_sales_by_region = '''
        SELECT Magasins.Ville, SUM(Ventes.Quantite * Produits.Prix) AS Revenue
        FROM Ventes
        JOIN Produits ON Ventes.ID_Reference_Produit = Produits.ID_Reference_Produit
        JOIN Magasins ON Ventes.ID_Magasin = Magasins.ID_Magasin
        GROUP BY Magasins.Ville
        '''
        region_revenue = c.execute(query_sales_by_region).fetchall()
        for region, revenue in region_revenue:
            c.execute('INSERT INTO Analyses (Type_Analyse, Resultat) VALUES (?, ?)', 
                      (f'Revenue in {region}', str(revenue)))
            
            
        # print("Updated Analyses Table:")
        # c.execute('SELECT Type_Analyse, Resultat FROM Analyses')
        # analyses_data = c.fetchall()
        # for analysis in analyses_data:
        #     print(analysis)

        connexion.commit()
        print("Analyses performed successfully and results saved.\n")
        
    except Exception as e:
        print(f"An error occurred while performing analyses: {e}\n")
    finally:
        connexion.close()
    
    return

if __name__ == '__main__':
    
    print("\nCreating empty database (db) and tables : ")
    create_database()

    print("Retrieving data and loading into the db: ")
    ### En utilisant le localhost
    # fetch_and_load_data('http://localhost:5000/data/magasins', 'Magasins')
    # fetch_and_load_data('http://localhost:5000/data/produits', 'Produits')
    # fetch_and_load_data('http://localhost:5000/data/ventes'  , 'Ventes')
    
    ### En utilisant le docker
    fetch_and_load_data('http://host.docker.internal:5000/data/magasins', 'Magasins')
    fetch_and_load_data('http://host.docker.internal:5000/data/produits', 'Produits')
    fetch_and_load_data('http://host.docker.internal:5000/data/ventes'  , 'Ventes')
    
    print("\nAnalyzing sales data and retrieving results into the db :")
    perform_analyses()
    
    # python.exe .\server\server.py
    # docker-compose up --build
