import sys

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Mixin:
    """Base class for sensor value tables
    """

    def __repr__(self):  # pragma: no cover
        return "<{!r}: {!r}, {!r}, {!r}>".format(
            self.__tablename__, self.name, self.time, self.value
        )

    def to_dict(self) -> dict:  # pragma: no cover
        """Method to serialise SQLAlchemy response for JSON

        :returns <dict>
        """
        d_out = dict((key, val) for key, val in self.__dict__.items())
        d_out.pop("_sa_instance_state", None)
        d_out["_id"] = d_out.pop("id", None)  # rename id key to interface with response
        if "time" in d_out:
            d_out["time"] = d_out["time"].isoformat()

        return d_out


def init_test_db():
    """
    Initialise the in memory SQLite3 testing DB
    with a sample SQL file
    """
    try:
        with open("data/sample.sql") as f:
            data = f.read()
    except FileNotFoundError:  # pragma: no cover
        sys.exit("Sample SQL file not found.")

    c = db.engine.raw_connection().cursor()
    c.executescript(data)
    c.close()
