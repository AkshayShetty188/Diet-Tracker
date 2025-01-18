from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://Akshay18:Akshay@18@localhost')
with engine.connect() as conn:
    conn.execute("CREATE DATABASE Diet")
