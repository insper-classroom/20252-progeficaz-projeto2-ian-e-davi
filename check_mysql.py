from dotenv import load_dotenv
load_dotenv() 

from repo.mysql_repo import ImoveisRepo

r = ImoveisRepo()
print("Registros:", len(r.list_all()))
