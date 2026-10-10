import random
import pygame

# Размер окна
WIDTH = 700
HEIGHT = 500

# Настройки
FPS = 60
STAR_COUNT = 100

# Цвета
BACKGROUND_COLOR = (5, 7, 20)

NEON_PINK = (255, 40, 180)
NEON_BLUE = (30, 220, 255)
NEON_PURPLE = (125, 50, 255)
WHITE = (245, 245, 255)

class Star:
    def __init__(self, start_above_screen=False):
        self.reset(start_above_screen)

    def reset(self, start_above_screen=True):
        # Случайная позиция по горизонтали
        self.x = random.uniform(0, WIDTH)

        # При создании распределяем звёзды по всему экрану.
        # После падения возвращаем звезду выше верхней границы.
        if start_above_screen:
            self.y = random.uniform(-100, -10)
        else:
            self.y = random.uniform(0, HEIGHT)

        # Индивидуальные параметры звезды
        self.speed = random.uniform(60, 220)
        self.size = random.choice([1, 1, 1, 2, 2, 3])
        self.trail_length = random.uniform(5, 25)
        self.brightness = random.randint(140, 255)

    def update(self, delta_time):
        self.y += self.speed * delta_time

        # Возвращаем звезду наверх после выхода за экран
        if self.y - self.trail_length > HEIGHT:
            self.reset()

    def draw(self, surface):
        x = int(self.x)
        y = int(self.y)

        # След звезды немного темнее самой звезды
        trail_color = (
            self.brightness // 3,
            self.brightness // 3,
            self.brightness // 2,
        )

        pygame.draw.line(
            surface,
            trail_color,
            (x, int(y - self.trail_length)),
            (x, y),
            max(1, self.size),
        )

        # Основная светлая точка
        star_color = (
            self.brightness,
            self.brightness,
            min(255, self.brightness + 20),
        )

        pygame.draw.circle(
            surface,
            star_color,
            (x, y),
            self.size,
        )

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface):
        hovered = self.is_hovered()

        # Свечение вокруг кнопки
        glow_surface = pygame.Surface(
            (self.rect.width + 40, self.rect.height + 40),
            pygame.SRCALPHA,
        )

        glow_color = (
            (30, 220, 255, 45)
            if hovered
            else (255, 40, 180, 35)
        )

        pygame.draw.rect(
            glow_surface,
            glow_color,
            (20, 20, self.rect.width, self.rect.height),
            border_radius=12,
        )

        surface.blit(
            glow_surface,
            (self.rect.x - 20, self.rect.y - 20),
        )

        # Основной фон кнопки
        button_color = (
            (25, 35, 75)
            if hovered
            else (15, 20, 50)
        )

        border_color = NEON_BLUE if hovered else NEON_PINK

        pygame.draw.rect(
            surface,
            button_color,
            self.rect,
            border_radius=10,
        )

        # Внешняя неоновая рамка
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            width=3,
            border_radius=10,
        )

        # Дополнительная внутренняя рамка
        inner_rect = self.rect.inflate(-10, -10)

        pygame.draw.rect(
            surface,
            NEON_PURPLE,
            inner_rect,
            width=1,
            border_radius=7,
        )

        # Текст кнопки
        text_color = WHITE if hovered else (220, 225, 255)
        text_surface = self.font.render(
            self.text,
            True,
            text_color,
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        # Небольшая тень текста
        shadow_surface = self.font.render(
            self.text,
            True,
            (70, 20, 100),
        )

        shadow_rect = shadow_surface.get_rect(
            center=(self.rect.centerx + 2, self.rect.centery + 2)
        )

        surface.blit(shadow_surface, shadow_rect)
        surface.blit(text_surface, text_rect)

def draw_logo(surface, logo_font, subtitle_font):
    logo_text = "SHOOTER"

    # Несколько смещённых слоёв создают эффект неоновой тени
    shadow_purple = logo_font.render(
        logo_text,
        True,
        NEON_PURPLE,
    )

    shadow_pink = logo_font.render(
        logo_text,
        True,
        NEON_PINK,
    )

    main_text = logo_font.render(
        logo_text,
        True,
        NEON_BLUE,
    )

    highlight = logo_font.render(
        logo_text,
        True,
        WHITE,
    )

    logo_rect = main_text.get_rect(
        center=(WIDTH // 2, 145)
    )

    # Дальняя фиолетовая тень
    surface.blit(
        shadow_purple,
        (logo_rect.x + 9, logo_rect.y + 10),
    )

    # Розовая тень
    surface.blit(
        shadow_pink,
        (logo_rect.x + 5, logo_rect.y + 5),
    )

    # Голубой основной слой
    surface.blit(main_text, logo_rect)

    # Белый блик с небольшим смещением
    surface.blit(
        highlight,
        (logo_rect.x, logo_rect.y - 2),
    )

    # Декоративные линии в стиле 80-х
    line_y = logo_rect.bottom + 12

    pygame.draw.line(
        surface,
        NEON_PINK,
        (logo_rect.left + 15, line_y),
        (logo_rect.right - 15, line_y),
        3,
    )

    pygame.draw.line(
        surface,
        NEON_BLUE,
        (logo_rect.left + 45, line_y + 7),
        (logo_rect.right - 45, line_y + 7),
        2,
    )

    # Маленькая подпись под логотипом
    subtitle_surface = subtitle_font.render(
        "RETRO SPACE ACTION",
        True,
        (180, 120, 255),
    )

    subtitle_rect = subtitle_surface.get_rect(
        center=(WIDTH // 2, line_y + 35)
    )

    surface.blit(subtitle_surface, subtitle_rect)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shooter")

    clock = pygame.time.Clock()

    # Шрифты создаются один раз, а не каждый кадр
    logo_font = pygame.font.SysFont(
        "arialblack",
        82,
        bold=True,
        italic=True,
    )

    subtitle_font = pygame.font.SysFont(
        "arial",
        17,
        bold=True,
    )

    button_font = pygame.font.SysFont(
        "arial",
        27,
        bold=True,
    )

    # Создаём звёзды
    stars = [Star() for _ in range(STAR_COUNT)]

    # Создаём кнопку по центру окна
    start_button = Button(
        x=WIDTH // 2 - 140,
        y=335,
        width=280,
        height=65,
        text="Начать игру",
        font=button_font,
    )

    running = True

    while running:
        # Время между кадрами в секундах
        delta_time = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Закрытие окна по клавише Escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Кнопка уже реагирует на нажатие,
            # но пока ничего не запускает
            if start_button.is_clicked(event):
                pass

        # Заливаем экран тёмным цветом
        screen.fill(BACKGROUND_COLOR)

        # Обновляем и рисуем звёзды
        for star in stars:
            star.update(delta_time)
            star.draw(screen)

        # Рисуем элементы меню поверх звёзд
        draw_logo(screen, logo_font, subtitle_font)
        start_button.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()