# domain/validators.py
REQUIRED_MIN = {"logradouro", "cidade"}
ALL_FIELDS = {"logradouro","tipo_logradouro","bairro","cidade","cep","tipo","valor","data_aquisicao"}

def validate_create(payload: dict) -> tuple[bool, dict|None]:
    miss = [k for k in REQUIRED_MIN if not payload.get(k)]
    if miss:
        return False, {"erro":"payload inválido", "missing": miss}
    unknown = [k for k in payload.keys() if k not in ALL_FIELDS|{"id"}]
    if unknown:
        return False, {"erro":"campos desconhecidos", "fields": unknown}
    return True, None

def validate_update(payload: dict) -> tuple[bool, dict|None]:
    if not payload: 
        return False, {"erro":"payload inválido"}
    unknown = [k for k in payload.keys() if k not in ALL_FIELDS]
    if unknown:
        return False, {"erro":"campos desconhecidos", "fields": unknown}
    return True, None
