# repo/mysql_repo.py
import os
from typing import Dict, List, Optional, Tuple
import pymysql
from urllib.parse import urlparse

# Campos do schema oficial (imoveis.sql)
CAMPOS = [
    "id",
    "logradouro",
    "tipo_logradouro",
    "bairro",
    "cidade",
    "cep",
    "tipo",
    "valor",
    "data_aquisicao",
]

def _parse_mysql_url(url: str) -> Tuple[str, int, str, str, str]:
    """
    Aceita DATABASE_URL no formato:
      mysql+pymysql://USER:PASSWORD@HOST:PORT/DB
    Retorna (host, port, user, password, database)
    """
    if url.startswith("mysql+pymysql://"):
        url = url.replace("mysql+pymysql://", "mysql://", 1)
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 3306
    user = parsed.username
    password = parsed.password
    database = parsed.path.lstrip("/")
    return host, port, user, password, database

def _conn():
    db_url = os.environ["DATABASE_URL"]
    host, port, user, password, database = _parse_mysql_url(db_url)
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

class ImoveisRepo:
    """Implementação real usando MySQL (Aiven)."""

    def list_all(self) -> List[Dict]:
        with _conn().cursor() as c:
            c.execute("SELECT * FROM imoveis ORDER BY id ASC")
            rows = c.fetchall()
        return [self._only_public(r) for r in rows]

    def get_by_id(self, _id: int) -> Optional[Dict]:
        with _conn().cursor() as c:
            c.execute("SELECT * FROM imoveis WHERE id=%s", (_id,))
            row = c.fetchone()
        return self._only_public(row) if row else None

    def create(self, data: Dict) -> Dict:
        cols = [
            "logradouro",
            "tipo_logradouro",
            "bairro",
            "cidade",
            "cep",
            "tipo",
            "valor",
            "data_aquisicao",
        ]
        vals = [data.get(k) for k in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        sql = f"INSERT INTO imoveis ({', '.join(cols)}) VALUES ({placeholders})"
        with _conn().cursor() as c:
            c.execute(sql, vals)
            new_id = c.lastrowid
        return self.get_by_id(new_id)

    def update(self, _id: int, data: Dict) -> Optional[Dict]:
        # Atualiza só os campos presentes em `data` e diferentes de id
        set_parts = []
        vals = []
        for k in CAMPOS:
            if k == "id":
                continue
            if k in data:
                set_parts.append(f"{k}=%s")
                vals.append(data[k])
        if not set_parts:
            # nada pra atualizar, apenas retorna o atual
            return self.get_by_id(_id)
        vals.append(_id)
        sql = f"UPDATE imoveis SET {', '.join(set_parts)} WHERE id=%s"
        with _conn().cursor() as c:
            c.execute(sql, vals)
        return self.get_by_id(_id)

    def delete(self, _id: int) -> bool:
        with _conn().cursor() as c:
            c.execute("DELETE FROM imoveis WHERE id=%s", (_id,))
            return c.rowcount > 0

    def list_by_tipo(self, tipo: str) -> List[Dict]:
        with _conn().cursor() as c:
            c.execute("SELECT * FROM imoveis WHERE tipo=%s ORDER BY id ASC", (tipo,))
            rows = c.fetchall()
        return [self._only_public(r) for r in rows]

    def list_by_cidade(self, cidade: str) -> List[Dict]:
        with _conn().cursor() as c:
            c.execute("SELECT * FROM imoveis WHERE cidade=%s ORDER BY id ASC", (cidade,))
            rows = c.fetchall()
        return [self._only_public(r) for r in rows]

    @staticmethod
    def _only_public(row: Optional[Dict]) -> Optional[Dict]:
        if row is None:
            return None
        # garante apenas as chaves esperadas no JSON
        return {k: row.get(k) for k in CAMPOS}
