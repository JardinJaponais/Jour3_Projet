import os
from boto3.session import Session
import pandas as pd
from sqlalchemy import create_engine, text

def first_function():
    print("Première fonction")


def last_function():
    print("Dernière fonction")

def load_logs():
        # --- Config via variables d'environnement (recommandé) ---
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "studentSDV")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "coucou44")
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://51.77.215.42:9010")
    S3_BUCKET = os.getenv("S3_BUCKET", "wintershoplogs")

    LOCAL_DIR = os.getenv("LOCAL_DIR", "/opt/airflow/Bronze")


    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
    DB_HOST = os.getenv("DB_HOST", "10.18.72.74")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "postgres")

    SCHEMA = os.getenv("DB_SCHEMA", "PROD")
    TABLE_NAME = os.getenv("DB_TABLE", "BRONZE_LOGS")

    os.makedirs(LOCAL_DIR, exist_ok=True)

    # --- S3 Client ---
    session = Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    s3 = session.client(
        service_name="s3",
        endpoint_url=S3_ENDPOINT_URL,
    )

    # --- Trouver le dernier fichier présent localement (Bronze) ---
    local_files = [f for f in os.listdir(LOCAL_DIR) if f.startswith("access_")]
    latest_file = max(local_files) if local_files else None

    print(f"Latest local file: {latest_file}")

    # --- Lister bucket ---
    response = s3.list_objects_v2(Bucket=S3_BUCKET)

    files_to_download = []
    if "Contents" in response:
        for obj in response["Contents"]:
            file_key = obj["Key"]
            file_name = os.path.basename(file_key)

            # Si aucun fichier local -> on prend tout
            if latest_file is None or file_name >= latest_file:
                files_to_download.append(file_key)
    else:
        print("Aucun fichier trouvé dans le bucket.")
        return

    files_to_download.sort()

    # --- Télécharger + lire ---
    all_logs = []
    for file_key in files_to_download:
        file_name = os.path.basename(file_key)
        local_path = os.path.join(LOCAL_DIR, file_name)

        if not os.path.exists(local_path):
            s3.download_file(S3_BUCKET, file_key, local_path)
            print(f"Téléchargé : {file_name}")
        else:
            print(f"Déjà présent : {file_name}")

        df = pd.read_csv(local_path, sep="🎭", header=None, engine="python")
        all_logs.append(df)

    if not all_logs:
        print("Aucun log à traiter.")
        return

    df_all = pd.concat(all_logs, ignore_index=True)
    print(f"Total lignes : {len(df_all)}")

    df_all.columns = ["raw_line"]

    # --- Charger dans Postgres ---
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};"))

    df_all.to_sql(
        name=TABLE_NAME,
        con=engine,
        schema=SCHEMA,
        if_exists="append",
        index=False,
    )
    print(f"Données insérées dans {SCHEMA}.{TABLE_NAME}")

    # --- Nettoyage Bronze : garder uniquement le plus récent ---
    local_files = [f for f in os.listdir(LOCAL_DIR) if f.startswith("access_")]
    latest_file = max(local_files) if local_files else None

    for f in os.listdir(LOCAL_DIR):
        file_path = os.path.join(LOCAL_DIR, f)
        if os.path.isfile(file_path) and f != latest_file:
            os.remove(file_path)
        else:
            print(f"Gardé : {f}")
