import pygame

import utils
import constants

class Game:
    font = pygame.font.SysFont("comicsansms", 32)

    player_label = font.render("Your turn, Player 1", True, constants.LABEL_COLOR)
    player_label_rect = player_label.get_rect(topleft = (constants.DIMENSIONS.window_gap, 0))

    text_width, trash = font.size("Your turn, Player 1")

    pass_label = font.render("Pass", True, constants.LABEL_COLOR)
    pass_label_rect = pass_label.get_rect(topleft = (text_width + constants.DIMENSIONS.window_gap * 2, 0))

    back_label = font.render("Back", True, constants.LABEL_COLOR)
    back_label_rect = back_label.get_rect(topleft = (text_width * 1.5 + constants.DIMENSIONS.window_gap, 0))

    back_label_rect2 = back_label.get_rect(topleft = (0, 0))

    def __init__(self, surface, board):
        self.surface = surface
        self.board = board
        self.in_game = True
        self.current_player = constants.Team.BLACK
        self.passed = {
            constants.Team.BLACK: False,
            constants.Team.WHITE: False
        }

    def run(self):
        self.draw_game()

        while self.in_game:
            for event in pygame.event.get():
                utils.common_events(event)
                if event.type == pygame.MOUSEMOTION:
                    if self.board.get_point(event.pos):
                        pygame.mouse.set_cursor(*pygame.cursors.diamond)
                    else:
                        pygame.mouse.set_cursor(*pygame.cursors.arrow)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if Game.back_label_rect.collidepoint(event.pos):
                        return
                    elif Game.pass_label_rect.collidepoint(event.pos):
                        if self.pass_turn():
                            return self.board.get_game_infos()
                        self.draw_game()

                    clicked_point = self.board.get_point(event.pos)
                    if clicked_point:
                        self.play(clicked_point)

    def pass_turn(self):
        self.toggle_player()

        if self.passed[utils.get_opposite_team(self.current_player)]:
            return True

        self.passed[self.current_player] = True

    def play(self, point):
        if self.passed[self.current_player]:
            self.passed[self.current_player] = False

        if point.is_playable(self.current_player):
            point.team = self.current_player
            self.toggle_player()
            self.draw_game()
            return True
        else:
            return False

    def toggle_player(self):
        if self.current_player == constants.Team.WHITE:
            self.current_player = constants.Team.BLACK
        else:
            self.current_player = constants.Team.WHITE

    def draw_heading(self):
        if self.current_player == constants.Team.BLACK:
            Game.player_label = Game.font.render("BLACK's turn", True, constants.LABEL_COLOR)
        elif self.current_player == constants.Team.WHITE:
            Game.player_label = Game.font.render("WHITE's turn", True, constants.LABEL_COLOR)
        self.surface.blit(Game.player_label, Game.player_label_rect)
        self.surface.blit(Game.pass_label, Game.pass_label_rect)
        self.surface.blit(Game.back_label, Game.back_label_rect)

    def draw_game(self):
        self.surface.fill(constants.BACKGROUND_COLOR)
        self.draw_heading()
        self.board.draw_empty_board(self.surface)
        self.board.update_board()
        self.board.draw_board_state(self.surface)

    def draw_end(self):
        pass
