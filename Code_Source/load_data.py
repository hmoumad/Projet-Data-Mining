import psycopg2
import json
import pandas as pd

df = pd.read_json('/home/yassine/python_works/processData.json', orient ='split', compression = 'infer')

con = psycopg2.connect(
    database='postgres',
    user='afrache',
    password='yassine',
    host='localhost',
    port='5432'
)

cursor_obj = con.cursor()


# Iterate over rows using iterrows()
for index, row in df.iterrows():
    nom = row['nom']
    adresse = row['adresse']
        #rate = float(row['rate'])
    nombre_reaction = int(row['nombre_reaction']) if row['nombre_reaction'] else None  # Cast rate to integer, handle empty values
    nom_banque = row['nom_banque']
    score = float(row['score'])
    
        # Use parameterized query to insert values
    cursor_obj.execute("INSERT INTO banques (agence,adresse,nombre_reaction,banque,score) VALUES (%s, %s, %s, %s, %s)",
                       (nom, adresse,nombre_reaction,nom_banque,score))
    print('inserted')
con.commit()
cursor_obj.close()
con.close()
