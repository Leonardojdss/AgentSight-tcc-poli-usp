from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


class PostgreSQLConnection:
    def __init__(self):
        # Variáveis de ambiente para PostgreSQL
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_NAME")
        self.username = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        
        if not all([self.database, self.username, self.password]):
            raise ValueError("Variáveis de ambiente DB_NAME, DB_USER e DB_PASSWORD devem estar definidas no .env")
        
        # String de conexão PostgreSQL
        connection_string = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine: Engine = create_engine(connection_string, echo=False, future=True)
        self.conn: Connection | None = None
        self.session = sessionmaker(bind=self.engine)

    def connect(self):
        try:
            self.conn = self.engine.connect()
            return self.conn
        except SQLAlchemyError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query: str, params: dict = None):
        if not self.conn:
            self.connect()
        try:
            if params is None:
                params = {}
            result = self.conn.execute(text(query), params)
            self.conn.commit()
            return result
        except SQLAlchemyError as e:
            print(f"Erro ao executar query: {e}")
            return None

    def fetch_all(self, query: str, params: dict = None):
        result = self.execute_query(query, params)
        if result:
            return result.fetchall()
        return []
    
    def test_connection(self) -> bool:
        """
        Testa se a conexão com o banco de dados pode ser estabelecida e executa uma query simples.
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as e:
            print(f"Falha no teste de conexão: {e}")
            return False
        
    def get_session(self):
        return self.session()

# teste de conexão
if __name__ == "__main__":
    db = PostgreSQLConnection()
    if db.test_connection():
        print("Conexão com o banco de dados estabelecida com sucesso.")
    else:
        print("Falha ao conectar ao banco de dados.")

# teste de execução de query
    query = "SELECT * FROM faturamento_vendas;"
    print(db.execute_query(query=query))