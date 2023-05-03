import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2

host = '10.0.0.122'  # IP on my local network - watch for dynamic IP after a machine restart
port = '5432'  # Postgres is on port 5432
db_name = 'seq_app'  # Replace with the name of your PostgreSQL database
user = 'usrrecruiterai'  # Replace with the username you use to connect to your PostgreSQL database
password = 'seqWDFHDF300'  # Replace with the password you use to connect to your PostgreSQL database
# user = 'seqadmin'
# password = 'SQLAdmin2023'

connectionString = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
print(connectionString)
engine = create_engine(connectionString)

# Open connection
connection = engine.connect()
print("Connection great success!")

# Verify we are connected to the correct database
qry0 = text("SELECT current_database();")
result0 = connection.execute(qry0)
for row in result0:
    print(row)

# Create a SQL statement object
qry1 = text("SELECT * from tbl_LinkedinExperience")
#qry1 = text("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")


# Execute the statement
result = connection.execute(qry1)

# Print the column names
print(result.keys())

# Print the query results
for row in result:
    print(row)

# Close connection
connection.close()


