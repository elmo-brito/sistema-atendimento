from datetime import datetime, timezone

def utc_now():
    """Retorna o datetime atual em UTC, sem fuso horário (naive) para compatibilidade com o BD."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
