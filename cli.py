#!/usr/bin/python3

""" CLI script for working with database """

import asyncio
from argparse import ArgumentParser
from os import listdir, getcwd, path

import aiopg


MIGRATION_DIRECTORY = path.join(getcwd(), 'migrations/')
INITIAL_MIGRATION = """CREATE TABLE IF NOT EXISTS migrations (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL UNIQUE
)"""
FIND_MIGRATION = """SELECT * FROM migrations WHERE name='{name}'"""
REMEMBER_MIGRATION = """INSERT INTO migrations (name) VALUES ('{name}')"""


def get_migrations_list():
    """ Return sorted list with files in migrations directory """

    files = listdir(MIGRATION_DIRECTORY)
    return sorted(files)

def get_migration(name):
    """ Return text of the migration """

    migration_path = path.join(MIGRATION_DIRECTORY, name)
    with open(migration_path, 'r') as file:
        return file.read()

async def migrate(conn, name):
    """ Applying migration by name """

    print('{}...'.format(name), end='\t')

    script = get_migration(name)
    async with conn.cursor() as cursor:
        await cursor.execute(FIND_MIGRATION.format(name=name))
        result = await cursor.fetchall()
        if result:
            print('skiped')
            return

        try:
            await cursor.execute(script)
        except Exception as err:
            print('error!')
            print(err)
            raise SystemExit(1)
        else:
            print('ok')
            await cursor.execute(REMEMBER_MIGRATION.format(name=name))


async def main(args):
    """ Main function """

    options = {
        'database': args.postgres_database,
        'user': args.postgres_user,
        'host': args.postgres_host,
        'port': args.postgres_port
    }
    if args.postgres_pass:
        options['password'] = args.postgres_pass

    if args.command == 'migrate':
        conn = await aiopg.connect(**options)

        async with conn.cursor() as cursor:
            print('Initialization...', end='\t')
            await cursor.execute(INITIAL_MIGRATION)
            print('ok')

        print('Migrating...')

        for name in get_migrations_list():
            await migrate(conn, name)

        await conn.close()


if __name__ == "__main__":
    PARSER = ArgumentParser()

    PARSER.description = 'CLI for applying migration'
    PARSER.prog = 'python3 cli.py'

    PARSER.add_argument(
        '--postgres-pass',
        dest='postgres_pass',
        type=str,
        help='PostgreSQL user password',
        default=None
    )
    PARSER.add_argument(
        '--postgres-user',
        dest='postgres_user',
        type=str,
        help='PostgreSQL user name',
        default='postgres'
    )
    PARSER.add_argument(
        '--postgres-host',
        dest='postgres_host',
        type=str,
        help='PostgreSQL database host',
        default='localhost'
    )
    PARSER.add_argument(
        '--postgres-port',
        dest='postgres_port',
        type=int,
        help='PostgreSQL database port',
        default=5432
    )
    PARSER.add_argument(
        '--postgres-database',
        dest='postgres_database',
        type=str,
        help='PostgreSQL database name',
        default='donkey-engine'
    )

    SUBPARSER = PARSER.add_subparsers(help='Command', dest='command')

    SUBPARSER.add_parser(
        'migrate',
        help='Apply all migrations'
    )

    ARGS = PARSER.parse_args()

    if not ARGS.command:
        PARSER.print_help()
        raise SystemExit()

    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main(ARGS))
