class FakeRepo:
    def __init__(self, seed=None):
        self.items = {}
        self._next_id = 1
        for obj in (seed or []):
            _id = obj.get("id")
            if not _id:
                _id = self._next_id
                obj["id"] = _id
            self.items[_id] = dict(obj)
            self._next_id = max(self._next_id, _id + 1)

    def _gen_id(self):
        _id = self._next_id
        self._next_id += 1
        return _id

    # LIST/FILTER
    def list_all(self, *, tipo=None, cidade=None):
        vals = list(self.items.values())
        if tipo:
            vals = [v for v in vals if (v.get("tipo") or "").lower() == tipo.lower()]
        if cidade:
            vals = [v for v in vals if (v.get("cidade") or "").lower() == cidade.lower()]
        return vals

    # GET
    def get(self, _id):
        return self.items.get(_id)

    # CREATE (id opcional)
    def create(self, obj):
        new_obj = dict(obj)
        _id = new_obj.get("id")
        if _id is None:
            _id = self._gen_id()
            new_obj["id"] = _id
        if _id in self.items:
            return None  # conflito
        # garante todas as chaves do esquema existam, se quiser
        for k in ["logradouro","tipo_logradouro","bairro","cidade","cep","tipo","valor","data_aquisicao"]:
            new_obj.setdefault(k, None)
        self.items[_id] = new_obj
        return new_obj

    # UPDATE parcial
    def update(self, _id, patch):
        if _id not in self.items:
            return None
        self.items[_id].update({k: v for k, v in patch.items() if k != "id"})
        return self.items[_id]

    # DELETE
    def delete(self, _id):
        return self.items.pop(_id, None) is not None
