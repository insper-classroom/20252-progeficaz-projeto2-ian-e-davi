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
    def __init__(self, seed: Optional[List[Dict]] = None):
        self._itens: List[Dict] = []
        self._next_id = 1
        for obj in (seed or []):
            novo = {k: obj.get(k) for k in CAMPOS if k != "id"}
            _id = obj.get("id")
            if _id is None:
                _id = self._next_id
            novo["id"] = _id
            self._itens.append(novo)
            self._next_id = max(self._next_id, _id + 1)

    def _copy_public(self, item: Dict) -> Dict:
        return {k: item.get(k) for k in CAMPOS}

    def list_all(self, tipo: str = None, cidade: str = None):
        itens = [self._copy_public(x) for x in self._itens]
        if tipo:
            itens = [i for i in itens if (i.get("tipo") or "").lower() == tipo.lower()]
        if cidade:
            itens = [i for i in itens if (i.get("cidade") or "").lower() == cidade.lower()]
        return itens

    def get_by_id(self, _id: int) -> Optional[Dict]:
        for it in self._itens:
            if it["id"] == _id:
                return self._copy_public(it)
        return None

    # alias para compatibilidade
    def get(self, _id: int):
        return self.get_by_id(_id)

    def _gen_id(self) -> int:
        val = self._next_id
        self._next_id += 1
        return val

    def create(self, data: Dict) -> Optional[Dict]:
        # se veio id e já existe -> conflito
        if "id" in data and any(it["id"] == data["id"] for it in self._itens):
            return None
        _id = data.get("id", self._gen_id())
        novo = {k: data.get(k) for k in CAMPOS if k != "id"}
        novo["id"] = _id
        # garante todas as chaves do schema
        for k in CAMPOS:
            novo.setdefault(k, None)
        self._itens.append(novo)
        self._next_id = max(self._next_id, _id + 1)
        return self._copy_public(novo)

    def update(self, _id: int, data: Dict) -> Optional[Dict]:
        for it in self._itens:
            if it["id"] == _id:
                for k, v in data.items():
                    if k != "id" and k in CAMPOS:
                        it[k] = v
                return self._copy_public(it)
        return None

    def delete(self, _id: int) -> bool:
        for i, it in enumerate(self._itens):
            if it["id"] == _id:
                del self._itens[i]
                return True
        return False

    # filtros diretos (opcionais; a rota já filtra via list_all)
    def list_by_tipo(self, tipo: str) -> List[Dict]:
        return [self._copy_public(x) for x in self._itens if (x.get("tipo") == tipo)]

    def list_by_cidade(self, cidade: str) -> List[Dict]:
        return [self._copy_public(x) for x in self._itens if (x.get("cidade") == cidade)]

FakeRepo = ImoveisRepo
