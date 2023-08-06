from .base import db, Mixin


class ServerTemp(Mixin, db.Model):
    """
    """

    __tablename__ = "server_temp"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.REAL, nullable=False)

    def __repr__(self):  # pragma: no cover
        return "<ServerTemp {!r}, {!r}, {!r}>".format(self.name, self.time, self.value)
