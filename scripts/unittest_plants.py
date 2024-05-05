import unittest
import pygame
from unittest.mock import MagicMock
from plants import Plant, Walnut

class TestPlant(unittest.TestCase):
    def setUp(self):
        self.game_mock = MagicMock()
        self.game_mock.assets = {
            "plants": {
                "sunflower": pygame.Surface((32, 32)),
                "peashooter": pygame.Surface((32, 32)),
                "walnut": [pygame.Surface((32, 32)), pygame.Surface((32, 32)), pygame.Surface((32, 32))]
            }
        }
        self.game_mock.assets["plants"]["walnut"][0].fill((255, 0, 0))
        self.game_mock.assets["plants"]["walnut"][1].fill((0, 255, 0))
        self.game_mock.assets["plants"]["walnut"][2].fill((0, 0, 255))

        self.game_mock.assets["plants"]["sunflower"].fill((255, 255, 0))
        self.game_mock.assets["plants"]["peashooter"].fill((0, 255, 255))

        pygame.init()

    def test_plant_initialization(self):
        game = self.game_mock
        plant = Plant(game, "sunflower", (0, 0), 10)
        self.assertEqual(plant.type, "sunflower")
        self.assertEqual(plant.pos, (0, 0))
        self.assertEqual(plant.max_health, 10)
        self.assertEqual(plant.health, 10)

    def test_walnut_initialization(self):
        game = self.game_mock
        walnut = Walnut(game, (0, 0))
        self.assertEqual(walnut.type, "walnut")
        self.assertEqual(walnut.pos, (0, 0))
        self.assertEqual(walnut.max_health, 30)
        self.assertEqual(walnut.health, 30)
        self.assertEqual(walnut.img.get_at((0, 0)), (255, 0, 0))
    def test_walnut_update(self):
        game = self.game_mock
        walnut = Walnut(game, (0, 0))
        walnut.health = 20
        walnut.update(None)
        self.assertEqual(walnut.img.get_at((0, 0)), (0, 255, 0))

    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
