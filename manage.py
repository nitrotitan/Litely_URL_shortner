import os
import argparse

psr = argparse.ArgumentParser('To use alembic start with \'manage.py -db\' then your argument\n')

psr.add_argument(
    "-db", "--option",
    choices=['init', 'migrate', 'upgrade'],
    help="this contains command that will init, migrate and upgrade your db",
    required=True
)
psr.add_argument(
    "-m", "--message",
    help="add your message, you might have left it like your brain",
    required=True,
    type=str
)


def migrate(message="init"):
    revision_ = "alembic revision --autogenerate -m {}".format(message)
    os.system(revision_)


def upgrade():
    upgrade_ = "alembic upgrade head"
    os.system(upgrade_)


def init():
    init_ = "alembic init migrations"
    os.system(init_)


args = psr.parse_args()
if __name__ == '__main__':
    if args.option == 'migrate':
        migrate(message=args.message)
    elif args.option == 'upgrade':
        upgrade()
    elif args.option == 'init':
        init()
