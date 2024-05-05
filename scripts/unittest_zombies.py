import unittest
import pygame
from unittest.mock import MagicMock
from zombies import Zombie

class TestZombie(unittest.TestCase):
    def setUp(self):
        self.game_mock = MagicMock()
        self.game_mock.assets = {
            "zombies": {
                "normal": pygame.Surface((32, 32))
            }
        }
        self.game_mock.assets["zombies"]["normal"].fill((255, 0, 0))
        pygame.init()

    def test_zombie_initialization(self):
        game = self.game_mock
        zombie = Zombie(game, "normal", 1)
        self.assertEqual(zombie.type, "normal")
        self.assertEqual(zombie.lane, 1)
        self.assertEqual(zombie.pos, [320, 1 * 24 + 43 - 7])
        self.assertEqual(zombie.speed, 0.06)
        self.assertEqual(zombie.health, 10)

    def test_zombie_rect(self):
        game = self.game_mock
        zombie = Zombie(game, "normal", 1)
        rect = zombie.rect()
        self.assertEqual(rect, pygame.Rect(325, 76, 6, 16))

    def test_zombie_update_collision(self):
        game = self.game_mock
        zombie = Zombie(game, "normal", 1)
        plant_mock = MagicMock()
        plant_mock.rect.return_value = pygame.Rect(325, 60, 6, 16)
        game.grid = [[plant_mock], [0], [0], [0], [0]]
        zombie.update()
        self.assertTrue(zombie.moving)

    def test_zombie_update_no_collision(self):
        game = self.game_mock
        zombie = Zombie(game, "normal", 1)
        plant_mock = MagicMock()
        plant_mock.rect.return_value = pygame.Rect(500, 500, 6, 16)
        game.grid = [[plant_mock], [0], [0], [0], [0]]
        zombie.update()
        self.assertTrue(zombie.moving)

    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
