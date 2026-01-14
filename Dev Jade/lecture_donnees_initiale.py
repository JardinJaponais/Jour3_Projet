import boto3
from boto3.session import Session
import os
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine

# Créer une session boto3 avec les paramètres MinIO
session = Session(
    aws_access_key_id="studentSDV",
    aws_secret_access_key="coucou44",
)

# Créer un client S3 pointant vers MinIO
s3 = session.client(
    service_name="s3",
    endpoint_url= "http://51.77.215.42:9010",
)

# Exemple : Lister les objets dans un bucket

# response = s3.list_objects_v2(Bucket="wintershoplogs")
# for obj in response["Contents"]:
#     print(obj["Key"])


bucket_name = "wintershoplogs"
prefix = "access_2026"
local_dir = "Bronze"

# lister les fichiers du bucket
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

if "Contents" in response:
    for obj in response["Contents"]:
        file_key = obj["Key"]
        file_name = os.path.basename(file_key)
        local_path = local_dir + "/" + file_name

        s3.download_file(bucket_name, file_key, local_path)
        print("Téléchargé :", file_name)
else:
    print("Aucun fichier trouvé")

# bucket_name = "wintershoplogs"
# file_key = "access_2026-01-14_09-00-01.log"
# local_path = "access_2026-01-14_09-00-01.log"
# s3.download_file(bucket_name, file_key, local_path)

# mettre en df puis dans la bdd
# PostgreSQL
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "10.18.72.74"
DB_PORT = "5432"
DB_NAME = "postgres"
SCHEMA = "Jade_DEV"
TABLE_NAME = "logs_access"

if not df_all.empty:
    # Connexion SQLAlchemy
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    # Crée le schéma si nécessaire
    with engine.connect() as conn:
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};")

    # Écrire dans PostgreSQL
    df_all.to_sql(name=TABLE_NAME, con=engine, schema=SCHEMA, if_exists="append", index=False)
    print(f"Données insérées dans {SCHEMA}.{TABLE_NAME}")