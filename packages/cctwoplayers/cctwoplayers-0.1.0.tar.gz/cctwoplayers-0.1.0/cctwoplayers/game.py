from enum import Enum
from player import Player


class InvalidGameStatus(Exception):
    pass


class Game:

    class Status(Enum):
        PLAYING = 0
        FINISHED = 1

    DEFAULT_MAX_POINTS = 100

    def __init__(
        self,
        max_points=DEFAULT_MAX_POINTS,
        player_one_name="Player one",
        player_two_name="Player two",
    ):
        self.status = self.Status.PLAYING.value
        self.max_points = max_points
        self.player_one = Player(
            name=player_one_name,
            color=(255, 0, 0),
        )
        self.player_two = Player(
            name=player_two_name,
            color=(0, 0, 255),
        )
        self.winner = None

    def restart_game(self):
        self.winner = None
        self.player_one.restart_counter()
        self.player_two.restart_counter()
        self.status = self.Status.PLAYING.value

    @property
    def is_finished(self):
        return self.status == self.Status.FINISHED.value

    def increase_player_one_counter(self):
        if self.is_finished:
            raise InvalidGameStatus(
                "Game is finished. Can not increase counters."
            )
        self.player_one.increase_counter()
        self.update_status(self.player_one)

    def increase_player_two_counter(self):
        if self.is_finished:
            raise InvalidGameStatus(
                "Game is finished. Can not increase counters."
            )
        self.player_two.increase_counter()
        self.update_status(self.player_two)

    def update_status(self, player):
        if player.counter >= self.max_points:
            self.status = self.Status.FINISHED.value
            self.winner = player
