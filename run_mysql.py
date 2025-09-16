from app import create_app
from repo.mysql_repo import ImoveisRepo

app = create_app(repo=ImoveisRepo())

if __name__ == "__main__":
    app.run(debug=True)
