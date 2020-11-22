from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Test(db.Model):
    __tablename__ = 'test-table'
    key = db.Column(
        db.String(20),
        index=False,
        unique=True,
        nullable=False,
        primary_key=True
    )
    value = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=False
    )
