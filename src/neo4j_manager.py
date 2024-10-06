from dotenv import load_dotenv
from neo4j import GraphDatabase
import os

load_dotenv()

class Neo4jManager:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    @staticmethod
    def _create_application_tx(tx, name, type):
        tx.run("CREATE (a:Application {name: $name, type: $type})", name=name, type=type)

    def create_application(self, name, type):
        with self.driver.session() as session:
            session.execute_write(self._create_application_tx, name, type)

    @staticmethod
    def _create_information_tx(tx, app_from, app_to, info):
        tx.run("""
        MATCH (a:Application {name: $app_from})
        MATCH (b:Application {name: $app_to})
        CREATE (a)-[:INFOMS {info: $info}]->(b)
        """, app_from=app_from, app_to=app_to, info=info)

    def create_information(self, app_from, app_to, info):
        with self.driver.session() as session:
            session.execute_write(self._create_information_tx, app_from, app_to, info)

if __name__ == "__main__":
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    neo4j_manager = Neo4jManager(uri, username, password)

    neo4j_manager.create_application("App 1", "Web")
    neo4j_manager.create_application("App 2", "Web")

    neo4j_manager.create_information("App 1", "App 2", "Data request")

    neo4j_manager.close()