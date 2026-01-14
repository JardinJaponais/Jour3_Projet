import boto3
from boto3.session import Session
import os

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