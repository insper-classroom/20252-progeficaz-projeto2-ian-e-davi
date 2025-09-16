from dotenv import load_dotenv
load_dotenv()  # carrega .env antes de importar o repo

from repo.mysql_repo import ImoveisRepo

r = ImoveisRepo()
print("Registros:", len(r.list_all()))
