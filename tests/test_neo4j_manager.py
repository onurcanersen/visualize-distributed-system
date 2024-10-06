import unittest
from unittest.mock import patch, MagicMock
from src.neo4j_manager import Neo4jManager

class TestNeo4jManager(unittest.TestCase):
    @patch("neo4j.GraphDatabase.driver")
    def setUp(self, mock_driver):
        self.mock_driver = mock_driver.return_value
        self.mock_session = MagicMock()

        self.mock_driver.session.return_value.__enter__.return_value = self.mock_session

        self.neo4j_manager = Neo4jManager()

    def test_create_application(self):
        # Arrange
        name = "Test App"
        type = "Web"

        # Act
        self.neo4j_manager.create_application(name, type)

        # Assert
        self.mock_session.execute_write.assert_called_once_with(
            self.neo4j_manager._create_application_tx, name, type
        )

    def test_create_information(self):
        # Arrange
        app_from = "Test App"
        app_to = "Another App"
        info = "Some information"

        # Act
        self.neo4j_manager.create_information(app_from, app_to, info)

        # Assert
        self.mock_session.execute_write.assert_called_with(
            self.neo4j_manager._create_information_tx, app_from, app_to, info
        )

    def tearDown(self):
        self.neo4j_manager.close()

if __name__ == "__main__":
    unittest.main()