

from datetime import datetime

REQUIRED_MIN = {"logradouro", "cidade"}
ALL_FIELDS = {
    "logradouro", "tipo_logradouro", "bairro", "cidade",
    "cep", "tipo", "valor", "data_aquisicao"
}

def _is_date_iso(s: str) -> bool:
    try:
        
        datetime.fromisoformat(s)
        return True
    except Exception:
        return False


def validate_create(payload: dict) -> tuple[bool, dict | None]:
    if not isinstance(payload, dict) or not payload:
        return False, {"erro": "payload inválido"}

    
    miss = [k for k in REQUIRED_MIN if not payload.get(k)]
    if miss:
        return False, {"erro": "payload inválido", "missing": miss}

    
    unknown = [k for k in payload.keys() if k not in (ALL_FIELDS | {"id"})]
    if unknown:
        return False, {"erro": "campos desconhecidos", "fields": unknown}

    
    if "valor" in payload and not isinstance(payload["valor"], (int, float)):
        return False, {"erro": "valor deve ser numérico"}

    if "data_aquisicao" in payload and not _is_date_iso(str(payload["data_aquisicao"])):
        return False, {"erro": "data_aquisicao deve ser ISO (YYYY-MM-DD)"}


    return True, None


def validate_update(payload: dict) -> tuple[bool, dict | None]:
    
    if not isinstance(payload, dict) or not payload:
        return False, {"erro": "payload inválido"}

    unknown = [k for k in payload.keys() if k not in ALL_FIELDS]
    if unknown:
        return False, {"erro": "campos desconhecidos", "fields": unknown}

    if "valor" in payload and not isinstance(payload["valor"], (int, float)):
        return False, {"erro": "valor deve ser numérico"}

    if "data_aquisicao" in payload and not _is_date_iso(str(payload["data_aquisicao"])):
        return False, {"erro": "data_aquisicao deve ser ISO (YYYY-MM-DD)"}

    

    return True, None
