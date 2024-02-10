import pygame as pg


class Player:
    def __init__(self, surface, tile_size: int):
        self.surface = surface
        self.tile_size = tile_size
        # Posicionar la robotina en el centro de la primera cuadrícula
        self.pos = (self.tile_size // 2, self.tile_size // 2)

    def draw(self):
        # Dibujar la robotina como un círculo en su posición actual
        pg.draw.circle(self.surface, (255, 255, 255), self.pos, self.tile_size // 2)

    def move(self, target):
        # Calcular la nueva posición basada en el tamaño de la cuadrícula y el clic objetivo
        x = (self.tile_size * (target[0] // self.tile_size)) + (self.tile_size // 2)
        y = (self.tile_size * (target[1] // self.tile_size)) + (self.tile_size // 2)

        # Actualizar la posición de la robotina
        self.pos = (x, y)


class Game:
    def __init__(
        self,
        title: str,
        tile_size: int,
        tiles_horizontal: int,
        tiles_vertical: int,
    ):
        pg.init()
        self.clock = pg.time.Clock()
        pg.display.set_caption(title)

        self.tile_size = tile_size
        self.tiles_horizontal = tiles_horizontal
        self.tiles_vertical = tiles_vertical

        window_width = self.tile_size * self.tiles_horizontal
        window_height = self.tile_size * self.tiles_vertical
        self.surface = pg.display.set_mode((window_width, window_height))

        self.loop = True
        self.player = Player(self.surface, self.tile_size)

    def main(self):
        while self.loop:
            self.grid_loop()
        pg.quit()

    def grid_loop(self):
        self.surface.fill((0, 0, 0))
        for row in range(self.tiles_horizontal):
            for col in range(row % 2, self.tiles_horizontal, 2):
                pg.draw.rect(
                    self.surface,
                    (40, 40, 40),
                    (
                        row * self.tile_size,
                        col * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    ),
                )
        self.player.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.loop = False
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                self.player.move(pos)
        pg.display.update()


if __name__ == "__main__":
    mygame = Game(
        title="Robotina",
        tile_size=35,  # Tamaño de cada cuadrícula
        tiles_horizontal=30,
        tiles_vertical=20,
    )
    mygame.main()
