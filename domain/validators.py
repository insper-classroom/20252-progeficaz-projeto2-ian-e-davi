# domain/validators.py

from datetime import datetime

REQUIRED_MIN = {"logradouro", "cidade"}
ALL_FIELDS = {
    "logradouro", "tipo_logradouro", "bairro", "cidade",
    "cep", "tipo", "valor", "data_aquisicao"
}

def _is_date_iso(s: str) -> bool:
    try:
        # aceita "YYYY-MM-DD" (e também "YYYY-MM-DDTHH:MM:SS" se vier)
        datetime.fromisoformat(s)
        return True
    except Exception:
        return False


def validate_create(payload: dict) -> tuple[bool, dict | None]:
    if not isinstance(payload, dict) or not payload:
        return False, {"erro": "payload inválido"}

    # exige o mínimo (mantém compatibilidade com seus testes)
    miss = [k for k in REQUIRED_MIN if not payload.get(k)]
    if miss:
        return False, {"erro": "payload inválido", "missing": miss}

    # campos desconhecidos (id é permitido no create)
    unknown = [k for k in payload.keys() if k not in (ALL_FIELDS | {"id"})]
    if unknown:
        return False, {"erro": "campos desconhecidos", "fields": unknown}

    # validações de tipo/forma quando presentes
    if "valor" in payload and not isinstance(payload["valor"], (int, float)):
        return False, {"erro": "valor deve ser numérico"}

    if "data_aquisicao" in payload and not _is_date_iso(str(payload["data_aquisicao"])):
        return False, {"erro": "data_aquisicao deve ser ISO (YYYY-MM-DD)"}

    # opcional: se quiser validar CEP básico (xxxxx-xxx), descomente:
    # import re
    # if "cep" in payload and payload["cep"]:
    #     if not re.fullmatch(r"\d{5}-\d{3}", str(payload["cep"])):
    #         return False, {"erro": "cep inválido (formato esperado: 00000-000)"}

    return True, None


def validate_update(payload: dict) -> tuple[bool, dict | None]:
    """
    PUT e PATCH aceitos como atualização parcial (compatível com seus testes).
    Apenas valida tipos dos campos fornecidos e barra campos desconhecidos.
    """
    if not isinstance(payload, dict) or not payload:
        return False, {"erro": "payload inválido"}

    unknown = [k for k in payload.keys() if k not in ALL_FIELDS]
    if unknown:
        return False, {"erro": "campos desconhecidos", "fields": unknown}

    if "valor" in payload and not isinstance(payload["valor"], (int, float)):
        return False, {"erro": "valor deve ser numérico"}

    if "data_aquisicao" in payload and not _is_date_iso(str(payload["data_aquisicao"])):
        return False, {"erro": "data_aquisicao deve ser ISO (YYYY-MM-DD)"}

    # (mesmo comentário do CEP opcional se quiser aplicar aqui)

    return True, None
