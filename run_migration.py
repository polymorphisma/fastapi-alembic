# app/alembic_runner.py
import alembic.config


def run_migration():
    alembicArgs = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembicArgs)


if __name__ == '__main__':
    run_migration()
