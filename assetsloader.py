import pygame
class Assets:
    def load(self):
        self.kirbo_sprite = {
            "idle": [
                pygame.image.load("data/assets/kirbo/idle/kirbo-idle-0.png"),
                pygame.image.load("data/assets/kirbo/idle/kirbo-idle-1.png"),
                pygame.image.load("data/assets/kirbo/idle/kirbo-idle-2.png"),
                pygame.image.load("data/assets/kirbo/idle/kirbo-idle-3.png")
            ],
            "walk": [
                pygame.image.load("data/assets/kirbo/walk/kirbo-walk-0.png"),
                pygame.image.load("data/assets/kirbo/walk/kirbo-walk-1.png"),
                pygame.image.load("data/assets/kirbo/walk/kirbo-walk-2.png"),
                pygame.image.load("data/assets/kirbo/walk/kirbo-walk-3.png")
            ],
            "hiii": [
                pygame.image.load("data/assets/kirbo/hiii/kirbo-hiii-0.png")
            ],
            "jump": [
                pygame.image.load("data/assets/kirbo/jump/kirbo-jump-0.png"),
                pygame.image.load("data/assets/kirbo/jump/kirbo-jump-1.png"),
                pygame.image.load("data/assets/kirbo/jump/kirbo-jump-2.png"),
                pygame.image.load("data/assets/kirbo/jump/kirbo-jump-3.png"),
                pygame.image.load("data/assets/kirbo/jump/kirbo-jump-4.png")
            ],
            "fly": [
                pygame.image.load("data/assets/kirbo/fly/kirbo-fly-0.png"),
                pygame.image.load("data/assets/kirbo/fly/kirbo-fly-1.png")
            ],
            "breath": [
                pygame.image.load("data/assets/kirbo/breath/kirbo-breath-0.png"),
                pygame.image.load("data/assets/kirbo/breath/kirbo-breath-1.png"),
                pygame.image.load("data/assets/kirbo/breath/kirbo-breath-2.png"),
                pygame.image.load("data/assets/kirbo/breath/kirbo-breath-3.png"),
            ]
        }

        self.ground_tiles = [
            pygame.image.load("data/assets/tiles/ground/tile-0.png"),
            pygame.image.load("data/assets/tiles/ground/tile-1.png"),
            pygame.image.load("data/assets/tiles/ground/tile-2.png"),
            pygame.image.load("data/assets/tiles/ground/tile-3.png"),
            pygame.image.load("data/assets/tiles/ground/tile-4.png"),
            pygame.image.load("data/assets/tiles/ground/tile-5.png"),
            pygame.image.load("data/assets/tiles/ground/tile-6.png"),
            pygame.image.load("data/assets/tiles/ground/tile-7.png"),
            pygame.image.load("data/assets/tiles/ground/tile-8.png"),
            pygame.image.load("data/assets/tiles/ground/tile-9.png"),
            pygame.image.load("data/assets/tiles/ground/tile-10.png"),
            pygame.image.load("data/assets/tiles/ground/tile-11.png"),
        ]
        
        self.kirbo_smok = pygame.image.load("data/assets/kirbo-smok/kirbo-smok.png")