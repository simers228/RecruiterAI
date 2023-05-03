import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2

# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class PostgresConnection:
    def __init__(self, host, port, database, username, password, sslmode='required'):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.sslmode = sslmode
        
        self.engine = None
        self.session = None

    def connect(self):
        """Connect to the PostgreSQL server using SQLAlchemy and psycopg2."""
        connectionString = f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode={self.sslmode}'
        self.engine = create_engine(connectionString)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # print("very nice connection")
        return self.session

    def disconnect(self):
        """Disconnect from the PostgreSQL server."""
        self.session.close()
        self.engine.dispose()

    def listCurrentDatabase(self):
        currentDatabaseQuery = text("SELECT * from tbl_LinkedinExperience")
        result = self.session.execute(currentDatabaseQuery)
        for i in result:
            print(i)


    def main(self):
        print('good job')

# Define the variables in the connection string
hostname = '76.130.239.195' # Public IP for my house hold - consider making this a hidden variable
port = 5432 # Default postgres port - should never change
database = 'seq_app' # Main DB for production - will be dev instance at some point
username = 'usrrecruiterai' # User with CRUD privileges
password = 'seqWDFHDF300' # Make hidden variable asap

# Establish the variables in the class
conn = PostgresConnection(hostname, port, database, username, password)

print(conn.host) # Show how variables are called in class, can also be set

conn.connect() # call the create function to make the connection

conn.listCurrentDatabase()

conn.disconnect # call the disconnect function to end the connection


