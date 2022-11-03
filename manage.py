import os
import sys


def migrate():
    revision = "alembic revision --autogenerate -m \"init\" "
    os.system(revision)


def upgrade():
    upgrade = "alembic upgrade head"
    os.system(upgrade)

if __name__ == '__main__':
    migrate()
    upgrade()