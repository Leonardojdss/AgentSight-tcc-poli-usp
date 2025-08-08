from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from ms_agents_server.infrastructure.connection_openai import ConnectionAzureOpenai
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseSQLTool:

    llm = ConnectionAzureOpenai.llm_azure_openai()

    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_NAME")
        self.username = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        
    def tool_sql(self):
        connection_string = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.db = SQLDatabase.from_uri(connection_string)
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        tools = self.toolkit.get_tools()
        return tools
