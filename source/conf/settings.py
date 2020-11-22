from envparse import env

env.read_envfile()

SQLALCHEMY_ECHO = env.bool("SQLALCHEMY_ECHO", default=False)
SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI", default="postgresql:///postgres:postgres@postgres:5432/results")
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS", default=False)