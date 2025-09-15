import os
from .fake_repo import ImoveisRepo as FakeRepo
from .mysql_repo import ImoveisRepo as MysqlRepo

def get_repo():
    backend = os.getenv("REPO_BACKEND", "fake").lower()
    return MysqlRepo() if backend == "mysql" else FakeRepo()
