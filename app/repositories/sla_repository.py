from app.models import SLA
from app.repositories.base import BaseRepository

class SLARepository(BaseRepository):
    model = SLA

    def get_expired(self):
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return self.model.query.filter(SLA.vencimento < now, SLA.cumprido == False).all()
