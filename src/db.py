import psycopg2
import json
import sys
import os

SQL_LIST_TABLES = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_schema,table_name;
"""

class PostgreSQL:
    def __init__(self):
        # The direct path '.dbauth' means python needs to be run in the
        # programs root directory. We might want to change this at some point
        with open('.dbauth', 'r') as f:
            data = json.load(f)
        if 'POSTGRES_DB' in os.environ:
            data['dbname'] = os.environ['POSTGRES_DB']
        conString = "sslmode=require port='{port}' dbname='{dbname}' " + \
                    "user='{user}' host='{host}' password='{password}'"
        # Make connection with database
        self.connection = psycopg2.connect(conString.format(**data)) 
        # Each database operation requires a cursor
        cur = self.connection.cursor()
        # Execute the above SQL on the new cursor
        cur.execute(SQL_LIST_TABLES)
        # Read all results from the executed SQL
        tables = cur.fetchall()
        # Format into a comma separated string
        tableString = ', '.join([t[0] for t in tables])
        print 'Database initialized. Found tables:', tableString
