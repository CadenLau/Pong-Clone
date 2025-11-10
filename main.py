# possible expansions:
# - randomize initial direction of ball (and possibly direction after paddle hits)
# - create an options menu for pixel size, win condition, and volume

import os
import arcade
import random
from pyglet.graphics import Batch

FONT_PATH = os.path.join(os.path.dirname(__file__), "font", "pong-score.ttf")
arcade.load_font(FONT_PATH)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PIXEL_SIZE = 8
FONT_SIZE = 24
BASE_SPEED = 200
SPEED_INCREASE = 75
MAX_SPEED = BASE_SPEED + SPEED_INCREASE * 6
WIN_CONDITION = 11
VOLUME = 0.5
HIT_SOUND = arcade.load_sound(":resources:/sounds/explosion1.wav")
WALL_SOUND = arcade.load_sound(":resources:/sounds/hit3.wav")
SCORE_SOUND = arcade.load_sound(":resources:/sounds/coin1.wav")
MUSIC = arcade.load_sound(":resources:/music/funkyrobot.mp3")

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pong Clone")


class Paddle:
    def __init__(self, x: float, y: float, speed_mult: float) -> None:
        self.x = x
        self.y = y
        self.speed = BASE_SPEED * speed_mult
        self.directions = {"up": False, "down": False}

    def update(self, delta_time: float) -> None:
        if self.directions["up"]:
            self.y += self.speed * delta_time
        if self.directions["down"]:
            self.y -= self.speed * delta_time

        # keep paddle on screen
        if self.y < 0:
            self.y = 0
        if self.y > SCREEN_HEIGHT - PIXEL_SIZE * 8:
            self.y = SCREEN_HEIGHT - PIXEL_SIZE * 8


# ----- Start Menu View -----
class StartView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.box_batch = arcade.shape_list.ShapeElementList()
        self.singleplayer_box = arcade.shape_list.create_rectangle_filled(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2 + 50,
            250,
            60,
            arcade.color.WHITE,
        )
        self.multiplayer_box = arcade.shape_list.create_rectangle_filled(
            SCREEN_WIDTH // 2 + 150,
            SCREEN_HEIGHT // 2 + 50,
            250,
            60,
            arcade.color.WHITE,
        )
        self.quit_box = arcade.shape_list.create_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, 200, 60, arcade.color.WHITE
        )
        self.box_batch.append(self.singleplayer_box)
        self.box_batch.append(self.multiplayer_box)
        self.box_batch.append(self.quit_box)

        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "PONG",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            arcade.color.WHITE,
            FONT_SIZE * 2,
            anchor_x="center",
            anchor_y="center",
            batch=self.text_batch,
        )
        self.singleplayer_text = arcade.Text(
            "Singleplayer",
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2 + 50,
            arcade.color.BLACK,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.text_batch,
        )
        self.multiplayer_text = arcade.Text(
            "Multiplayer",
            SCREEN_WIDTH // 2 + 150,
            SCREEN_HEIGHT // 2 + 50,
            arcade.color.BLACK,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.text_batch,
        )
        self.quit_text = arcade.Text(
            "Quit",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50,
            arcade.color.BLACK,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.text_batch,
        )

    def on_draw(self) -> None:
        self.clear()
        self.box_batch.draw()
        self.text_batch.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                SCREEN_WIDTH // 2 - 275 < x < SCREEN_WIDTH // 2 - 25
                and SCREEN_HEIGHT // 2 + 20 < y < SCREEN_HEIGHT // 2 + 80
            ):
                # Singleplayer selected
                singleplayer_view = DifficultySelect()
                window.show_view(singleplayer_view)
            elif (
                SCREEN_WIDTH // 2 + 25 < x < SCREEN_WIDTH // 2 + 275
                and SCREEN_HEIGHT // 2 + 20 < y < SCREEN_HEIGHT // 2 + 80
            ):
                # Multiplayer selected
                multiplayer_view = MultiplayerView()
                window.show_view(multiplayer_view)
            elif (
                SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100
                and SCREEN_HEIGHT // 2 - 80 < y < SCREEN_HEIGHT // 2 - 20
            ):
                # Quit selected
                arcade.close_window()


# ----- AI Difficulty Select View -----
class DifficultySelect(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.box_batch = arcade.shape_list.ShapeElementList()
        self.easy_box = arcade.shape_list.create_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, 200, 60, arcade.color.WHITE
        )
        self.medium_box = arcade.shape_list.create_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 60, arcade.color.WHITE
        )
        self.hard_box = arcade.shape_list.create_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, 200, 60, arcade.color.WHITE
        )
        self.box_batch.append(self.easy_box)
        self.box_batch.append(self.medium_box)
        self.box_batch.append(self.hard_box)

        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "Select Difficulty",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            arcade.color.WHITE,
            FONT_SIZE * 2,
            anchor_x="center",
            anchor_y="center",
            batch=self.text_batch,
        )
        self.easy_text = arcade.Text(
            "Easy",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
            arcade.color.BLACK,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.text_batch,
        )
        self.medium_text = arcade.Text(
            "Medium",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.BLACK,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.text_batch,
        )
        self.hard_text = arcade.Text(
            "Hard",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            arcade.color.BLACK,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.text_batch,
        )

    def on_draw(self) -> None:
        self.clear()
        self.box_batch.draw()
        self.text_batch.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100
                and SCREEN_HEIGHT // 2 + 70 < y < SCREEN_HEIGHT // 2 + 130
            ):
                # Easy selected
                easy = Easy()
                window.show_view(easy)
            elif (
                SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100
                and SCREEN_HEIGHT // 2 - 30 < y < SCREEN_HEIGHT // 2 + 30
            ):
                # Medium selected
                medium = Medium()
                window.show_view(medium)
            elif (
                SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100
                and SCREEN_HEIGHT // 2 - 130 < y < SCREEN_HEIGHT // 2 - 70
            ):
                # Hard selected
                hard = Hard()
                window.show_view(hard)


# ===== Game View =====
class GameView(arcade.View):
    def __init__(self, p2_speed: float, view) -> None:
        super().__init__()
        self.view = view

        self.square_x = SCREEN_WIDTH // 2 - PIXEL_SIZE // 2
        self.square_y = SCREEN_HEIGHT // 2 - PIXEL_SIZE // 2
        if random.random() < 0.5:
            self.square_speed_x = BASE_SPEED
        else:
            self.square_speed_x = -BASE_SPEED
        if random.random() < 0.5:
            self.square_speed_y = BASE_SPEED
        else:
            self.square_speed_y = -BASE_SPEED

        self.player1 = Paddle(PIXEL_SIZE * 2, SCREEN_HEIGHT // 2 - PIXEL_SIZE // 2, 2)
        self.player1_score = arcade.Text(
            "0",
            SCREEN_WIDTH // 4 - FONT_SIZE // 2,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            FONT_SIZE,
            font_name="Pong Score",
        )

        self.player2 = Paddle(
            SCREEN_WIDTH - PIXEL_SIZE * 3,
            SCREEN_HEIGHT // 2 - PIXEL_SIZE // 2,
            p2_speed,
        )
        self.player2_score = arcade.Text(
            "0",
            SCREEN_WIDTH * 3 // 4 - FONT_SIZE // 2,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            FONT_SIZE,
            font_name="Pong Score",
        )

        self.batch = arcade.shape_list.ShapeElementList()

        def create_centerline(y_pos: int):
            line = arcade.shape_list.create_rectangle_filled(
                SCREEN_WIDTH // 2, y_pos, PIXEL_SIZE, PIXEL_SIZE * 2, arcade.color.WHITE
            )
            self.batch.append(line)

        for y in range(PIXEL_SIZE + (PIXEL_SIZE // 2), SCREEN_HEIGHT, PIXEL_SIZE * 4):
            create_centerline(y)

    def on_draw(self) -> None:
        self.clear()
        arcade.draw_lbwh_rectangle_filled(
            self.square_x, self.square_y, PIXEL_SIZE, PIXEL_SIZE, arcade.color.WHITE
        )
        arcade.draw_lbwh_rectangle_filled(
            self.player1.x,
            self.player1.y,
            PIXEL_SIZE,
            PIXEL_SIZE * 8,
            arcade.color.WHITE,
        )
        arcade.draw_lbwh_rectangle_filled(
            self.player2.x,
            self.player2.y,
            PIXEL_SIZE,
            PIXEL_SIZE * 8,
            arcade.color.WHITE,
        )
        self.player1_score.draw()
        self.player2_score.draw()
        self.batch.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.W:
            self.player1.directions["up"] = True
        if symbol == arcade.key.S:
            self.player1.directions["down"] = True

        if symbol == arcade.key.ESCAPE:  # pause
            pause_view = PauseView(self)
            window.show_view(pause_view)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.W:
            self.player1.directions["up"] = False
        if symbol == arcade.key.S:
            self.player1.directions["down"] = False

    def on_update(self, delta_time: float) -> None:
        # Move the square
        self.square_x += self.square_speed_x * delta_time
        self.square_y += self.square_speed_y * delta_time

        # top boundary
        if self.square_y > SCREEN_HEIGHT - PIXEL_SIZE:
            self.square_y = SCREEN_HEIGHT - PIXEL_SIZE
            self.square_speed_y *= -1
            arcade.play_sound(WALL_SOUND, VOLUME)

        # bottom boundary
        if self.square_y < 0:
            self.square_y = 0
            self.square_speed_y *= -1
            arcade.play_sound(WALL_SOUND, VOLUME)

        # Move players
        self.player1.update(delta_time)
        self.player2.update(delta_time)

        # Check for collisions with paddles
        if self.check_paddle_collision(self.player1):
            self.square_x = self.player1.x + PIXEL_SIZE
            self.square_speed_x = abs(self.square_speed_x)  # ensure moving right
            self.apply_speed_increase()
            arcade.play_sound(HIT_SOUND, VOLUME)

        if self.check_paddle_collision(self.player2):
            self.square_x = self.player2.x - PIXEL_SIZE
            self.square_speed_x = -abs(self.square_speed_x)  # ensure moving left
            self.apply_speed_increase()
            arcade.play_sound(HIT_SOUND, VOLUME)

        # Check for scoring
        # Right boundary
        if self.square_x > SCREEN_WIDTH - PIXEL_SIZE:
            self.player1_score.text = str(int(self.player1_score.text) + 1)
            arcade.play_sound(SCORE_SOUND, VOLUME)
            self.square_x = SCREEN_WIDTH // 2 - PIXEL_SIZE // 2
            self.square_y = random.randint(
                SCREEN_HEIGHT // 4, SCREEN_HEIGHT * 3 // 4 - PIXEL_SIZE
            )
            self.square_speed_x = -BASE_SPEED
            if random.random() < 0.5:
                self.square_speed_y = BASE_SPEED
            else:
                self.square_speed_y = -BASE_SPEED

        # Left boundary
        if self.square_x < 0:
            self.player2_score.text = str(int(self.player2_score.text) + 1)
            arcade.play_sound(SCORE_SOUND, VOLUME)
            self.square_x = SCREEN_WIDTH // 2 - PIXEL_SIZE // 2
            self.square_y = random.randint(
                SCREEN_HEIGHT // 4, SCREEN_HEIGHT * 3 // 4 - PIXEL_SIZE
            )
            self.square_speed_x = BASE_SPEED
            if random.random() < 0.5:
                self.square_speed_y = BASE_SPEED
            else:
                self.square_speed_y = -BASE_SPEED

        # Check for win condition
        if int(self.player1_score.text) >= WIN_CONDITION:
            end_view = GameEndView("Player 1", self.view)
            window.show_view(end_view)
        if int(self.player2_score.text) >= WIN_CONDITION:
            if self.view == MultiplayerView:
                end_view = GameEndView("Player 2", self.view)
            elif self.view == Easy or self.view == Medium or self.view == Hard:
                end_view = GameEndView("AI", self.view)
            window.show_view(end_view)

    def check_paddle_collision(self, paddle: Paddle) -> bool:
        paddle_top = paddle.y + PIXEL_SIZE * 8
        paddle_bottom = paddle.y
        if self.square_y + PIXEL_SIZE > paddle_bottom and self.square_y < paddle_top:
            return abs(self.square_x - paddle.x) < PIXEL_SIZE
        return False

    def apply_speed_increase(self) -> None:
        if abs(self.square_speed_x) < MAX_SPEED:
            self.square_speed_x += SPEED_INCREASE * (
                1 if self.square_speed_x > 0 else -1
            )
        if abs(self.square_speed_y) < MAX_SPEED:
            self.square_speed_y += SPEED_INCREASE * (
                1 if self.square_speed_y > 0 else -1
            )


# ----- Singleplayer Game View -----
class SingleplayerView(GameView):
    def __init__(self, AI_speed: float, view) -> None:
        super().__init__(AI_speed, view)

    def on_update(self, delta_time: float) -> None:
        AI_center = self.player2.y + PIXEL_SIZE * 4
        ball_center = self.square_y + PIXEL_SIZE / 2
        if ball_center > AI_center:
            self.player2.directions["up"] = True
            self.player2.directions["down"] = False
        elif ball_center < AI_center:
            self.player2.directions["up"] = False
            self.player2.directions["down"] = True

        super().on_update(delta_time)


# SinglePlayer difficulties written as classes for potential future expansion
# ----- Easy Difficulty Singleplayer Game View -----
class Easy(SingleplayerView):
    def __init__(self) -> None:
        super().__init__(2, Easy)


# ----- Medium Difficulty Singleplayer Game View -----
class Medium(SingleplayerView):
    def __init__(self) -> None:
        super().__init__(2.5, Medium)


# ----- Hard Difficulty Singleplayer Game View -----
class Hard(SingleplayerView):
    def __init__(self) -> None:
        super().__init__(3, Hard)


# ----- Multiplayer Game View -----
class MultiplayerView(GameView):
    def __init__(self) -> None:
        super().__init__(2, MultiplayerView)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        super().on_key_press(symbol, modifiers)

        if symbol == arcade.key.UP:
            self.player2.directions["up"] = True
        if symbol == arcade.key.DOWN:
            self.player2.directions["down"] = True

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        super().on_key_release(symbol, modifiers)

        if symbol == arcade.key.UP:
            self.player2.directions["up"] = False
        if symbol == arcade.key.DOWN:
            self.player2.directions["down"] = False


# ----- Pause Menu View -----
class PauseView(arcade.View):
    def __init__(self, game_view: GameView) -> None:
        super().__init__()
        self.game_view = game_view

        self.batch = Batch()
        self.message1 = arcade.Text(
            "Game Paused",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 50,
            arcade.color.WHITE,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            align="center",
            batch=self.batch,
        )
        self.message2 = arcade.Text(
            "Press Esc to Resume",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            FONT_SIZE * 3 // 4,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )
        self.message3 = arcade.Text(
            "Press Q to Quit to Main Menu",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50,
            arcade.color.WHITE,
            FONT_SIZE * 3 // 4,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ESCAPE:
            window.show_view(self.game_view)
        elif key == arcade.key.Q:
            main_menu = StartView()
            window.show_view(main_menu)


# ----- Game End Menu View -----
class GameEndView(arcade.View):
    def __init__(self, winner: str, view: GameView) -> None:
        super().__init__()
        self.view = view
        self.player = arcade.play_sound(MUSIC, VOLUME)

        self.batch = Batch()
        self.message1 = arcade.Text(
            f"{winner} Wins!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 40,
            arcade.color.WHITE,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )
        self.message2 = arcade.Text(
            "Press Enter to play again",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 10,
            arcade.color.WHITE,
            FONT_SIZE * 3 // 4,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )
        self.message3 = arcade.Text(
            "Press Q to Quit to Main Menu",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50,
            arcade.color.WHITE,
            FONT_SIZE * 3 // 4,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ENTER:
            arcade.stop_sound(self.player)
            game = self.view()
            window.show_view(game)
        elif key == arcade.key.Q:
            arcade.stop_sound(self.player)
            main_menu = StartView()
            window.show_view(main_menu)


start = StartView()
window.show_view(start)
arcade.run()
