# repo/fake_repo.py

from typing import List, Dict, Optional

# campos do schema oficial:
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

class ImoveisRepo:
    def __init__(self):
        # armazenamento em memória
        self._itens: List[Dict] = []
        self._next_id = 1

    def _copy_public(self, item: Dict) -> Dict:
        # retorna apenas os campos esperados
        return {k: item.get(k) for k in CAMPOS if k in item}

    # CRUD básico
    def list_all(self) -> List[Dict]:
        return [self._copy_public(x) for x in self._itens]

    def get_by_id(self, _id: int) -> Optional[Dict]:
        for it in self._itens:
            if it["id"] == _id:
                return self._copy_public(it)
        return None

    def create(self, data: Dict) -> Dict:
        novo = {
            "id": self._next_id,
            "logradouro": data.get("logradouro"),
            "tipo_logradouro": data.get("tipo_logradouro"),
            "bairro": data.get("bairro"),
            "cidade": data.get("cidade"),
            "cep": data.get("cep"),
            "tipo": data.get("tipo"),
            "valor": data.get("valor"),
            "data_aquisicao": data.get("data_aquisicao"),
        }
        self._itens.append(novo)
        self._next_id += 1
        return self._copy_public(novo)

    def update(self, _id: int, data: Dict) -> Optional[Dict]:
        for it in self._itens:
            if it["id"] == _id:
                # atualiza só chaves presentes em data
                for k in CAMPOS:
                    if k != "id" and k in data:
                        it[k] = data[k]
                return self._copy_public(it)
        return None

    def delete(self, _id: int) -> bool:
        for i, it in enumerate(self._itens):
            if it["id"] == _id:
                del self._itens[i]
                return True
        return False

    # filtros
    def list_by_tipo(self, tipo: str) -> List[Dict]:
        return [self._copy_public(x) for x in self._itens if (x.get("tipo") == tipo)]

    def list_by_cidade(self, cidade: str) -> List[Dict]:
        return [self._copy_public(x) for x in self._itens if (x.get("cidade") == cidade)]
