from app.models import LogAuditoria
from app.repositories.base import BaseRepository

class LogAuditoriaRepository(BaseRepository):
    model = LogAuditoria
