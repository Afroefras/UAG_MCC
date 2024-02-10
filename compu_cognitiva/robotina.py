import pygame as pg


class Player:
    def __init__(self, surface, tile_size: int):
        """
        Inicializa el jugador (robotina), estableciendo su superficie de dibujo,
        tamaño de cuadrícula y posición inicial.
        """
        self.surface = surface
        self.tile_size = tile_size
        # Posicionar la robotina en el centro de la primera cuadrícula
        self.pos = (self.tile_size // 2, self.tile_size // 2)

    def draw(self):
        """
        Dibujar la robotina como un círculo en su posición actual
        """
        pg.draw.circle(self.surface, (255, 255, 255), self.pos, self.tile_size // 2)

    def move_with_click(self, target):
        """
        Calcular la nueva posición basada en el tamaño de la cuadrícula y el clic objetivo
        """
        x = (self.tile_size * (target[0] // self.tile_size)) + (self.tile_size // 2)
        y = (self.tile_size * (target[1] // self.tile_size)) + (self.tile_size // 2)

        # Actualizar la posición de la robotina
        self.pos = (x, y)


class Game:
    def __init__(
        self, title: str, tile_size: int, tiles_horizontal: int, tiles_vertical: int
    ):
        """
        Inicializa el juego, estableciendo el título, tamaño de cuadrícula,
        dimensiones y la superficie de dibujo.
        También crea el botón de inicio y la instancia de Player.
        """
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

        # Añadir botón de inicio
        self.start_button = pg.Rect(
            window_width / 2 - 50, window_height / 2 - 25, 100, 50
        )
        self.game_started = False

    def draw_button(self, text):
        """
        Dibuja el botón de inicio en la superficie del juego,
        con un color de fondo azul claro y texto blanco.
        """
        pg.draw.rect(self.surface, (51, 153, 255), self.start_button)
        font = pg.font.Font(None, 36)
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.start_button.center)
        self.surface.blit(text_surf, text_rect)

    def check_button_click(self, pos):
        """
        Verifica si el clic del mouse fue sobre el botón de inicio y,
        de ser así, cambia el estado para comenzar el juego.
        """
        if self.start_button.collidepoint(pos):
            self.game_started = True

    def move_with_keys(self, event) -> None:
        """
        Maneja el movimiento de la robotina con el teclado,
        asegurando que se mueva una cuadrícula a la vez y
        se mantenga dentro de los límites.
        """
        x, y = self.player.pos
        x -= self.tile_size // 2
        y -= self.tile_size // 2

        if event.key == pg.K_LEFT:
            x = max(0, x - self.tile_size)
        if event.key == pg.K_RIGHT:
            x = min(self.tile_size * (self.tiles_horizontal - 1), x + self.tile_size)
        if event.key == pg.K_UP:
            y = max(0, y - self.tile_size)
        if event.key == pg.K_DOWN:
            y = min(self.tile_size * (self.tiles_vertical - 1), y + self.tile_size)

        self.player.pos = (x + self.tile_size // 2, y + self.tile_size // 2)

    def main(self):
        """
        El bucle principal del juego que mantiene el juego en ejecución y
        llama a `grid_loop` para dibujar y actualizar la ventana.
        """
        while self.loop:
            self.grid_loop()
        pg.quit()

    def grid_loop(self):
        """
        Llena la superficie con negro, dibuja la cuadrícula y la robotina,
        maneja los eventos de clic y teclado y actualiza la ventana.
        Incluye la lógica para comenzar el juego con el botón de inicio y
        mover la robotina.
        """
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

        if not self.game_started:
            self.draw_button("Inicio")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False

            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()

                if not self.game_started and self.start_button.collidepoint(pos):
                    self.check_button_click(pos)
                else:
                    self.player.move_with_click(pos)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.loop = False

                elif self.game_started:
                    self.move_with_keys(event)

        pg.display.update()


if __name__ == "__main__":
    mygame = Game(
        title="Robotina",
        tile_size=22,  # Tamaño de cada cuadrícula
        tiles_horizontal=30,
        tiles_vertical=20,
    )
    mygame.main()
