import ormar

from config import database, metadata


class Team(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str = 'teams'

    id: int = ormar.Integer(primary_key=True)
    area: str = ormar.String(max_length=40)
    description: str = ormar.String(max_length=200)
    is_team_deleted: bool = ormar.Boolean(default=False)