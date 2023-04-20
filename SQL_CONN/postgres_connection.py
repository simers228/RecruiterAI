from sqlalchemy import create_engine

host = '10.0.0.218'  # IP on my local network - watch for dynamic IP after a machine restart
port = '5432'  # Postgres is on port 5432
db_name = 'SQMAIN_DB'  # Replace with the name of your PostgreSQL database
user = 'usr_sqlalchemy'  # Replace with the username you use to connect to your PostgreSQL database
password = 'testconnection123'  # Replace with the password you use to connect to your PostgreSQL database

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')


with engine.connect() as conn:
    result = conn.execute('SELECT * FROM tbl_PeopleProfile')
    for row in result:
        print(row)
