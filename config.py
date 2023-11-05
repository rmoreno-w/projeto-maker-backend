import os

import databases
import sqlalchemy

POSTGRES_USERNAME = 'admin'
POSTGRES_PASSWORD = '2801'
POSTGRES_HOST = '172.17.0.2'
POSTGRES_PORT = '5432'

DATABASE_URL = os.getenv('DATABASE_URL', f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/projeto-maker')
TEST_DATABASE = os.getenv('TEST_DATABASE', 'false') in ('true', 'yes')

database = databases.Database(DATABASE_URL, force_rollback=TEST_DATABASE)
metadata = sqlalchemy.MetaData()