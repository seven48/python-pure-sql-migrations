# python-pure-sql-migrations

Example of using pure SQL migrations with [aiopg](https://github.com/aio-libs/aiopg)

# Example of using

Put your SQL migrations in `migrations/` directory and run the following command:

`$ python3 cli.py migrate`

Migrations name should be started with numbers because script is apply them in alphabetical order.

# `--help`

```
usage: python3 cli.py [-h] [--postgres-pass POSTGRES_PASS]
                      [--postgres-user POSTGRES_USER]
                      [--postgres-host POSTGRES_HOST]
                      [--postgres-port POSTGRES_PORT]
                      [--postgres-database POSTGRES_DATABASE]
                      {migrate} ...

CLI for applying migration

positional arguments:
  {migrate}             Command
    migrate             Apply all migrations

optional arguments:
  -h, --help            show this help message and exit
  --postgres-pass POSTGRES_PASS
                        PostgreSQL user password
  --postgres-user POSTGRES_USER
                        PostgreSQL user name
  --postgres-host POSTGRES_HOST
                        PostgreSQL database host
  --postgres-port POSTGRES_PORT
                        PostgreSQL database port
  --postgres-database POSTGRES_DATABASE
                        PostgreSQL database name
```