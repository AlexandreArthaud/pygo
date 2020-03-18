import pygame

import constants
import utils
from point import Point
from point_group import PointGroup


class Board:
    def __init__(self, board_choice):
        if board_choice == constants.GameChoice.NINE_BY_NINE_GOBAN:
            self.size = 9
            self.grid = self.create_empty_board(9)
        elif board_choice == constants.GameChoice.THIRTEEN_BY_THIRTEEN_GOBAN:
            self.size = 13
            self.grid = self.create_empty_board(13)
        elif board_choice == constants.GameChoice.NINETEEN_BY_NINETEEN_GOBAN:
            self.size = 19
            self.grid = self.create_empty_board(19)
        Point.grid = self.grid

    def create_empty_board(self, length):
        grid = []
        for height in range(length):
            line = []
            for width in range(length):
                line.append(Point(height, width))
            grid.append(line)
        return grid

    def get_point(self, pos):
        for line in self.grid:
            for point in line:
                if (point.coordinates[0] - 5 <= pos[0] <= point.coordinates[0] + 5
                    and point.coordinates[1] - 5 <= pos[1] <= point.coordinates[1] + 5):
                    return point
        return None

    def draw_empty_board(self, surface):
        board_rect = pygame.Rect(
            constants.DIMENSIONS.window_gap,
            constants.DIMENSIONS.window_gap,
            constants.DIMENSIONS.board_width,
            constants.DIMENSIONS.board_heigt)

        case_rect = pygame.Rect(
            constants.DIMENSIONS.window_gap + constants.DIMENSIONS.case_gap,
            constants.DIMENSIONS.window_gap + constants.DIMENSIONS.case_gap + constants.DIMENSIONS.heading_height,
            constants.DIMENSIONS.board_width / (self.size - 1),
            constants.DIMENSIONS.board_heigt / (self.size - 1)
        )

        for line in self.grid:
            for point in line:
                point.coordinates = (case_rect.x, case_rect.y)
                if line.index(point) < self.size - 1 and self.grid.index(line) < self.size - 1:
                    pygame.draw.rect(surface, constants.CASE_COLOR, case_rect)
                case_rect.x += case_rect.width + constants.DIMENSIONS.case_gap
            case_rect.x = constants.DIMENSIONS.window_gap + constants.DIMENSIONS.case_gap
            case_rect.y += case_rect.height + constants.DIMENSIONS.case_gap
        pygame.display.flip()

    def draw_board_state(self, surface):
        for line in self.grid:
            for point in line:
                if point.team:
                    pygame.draw.circle(surface, point.team.value, point.coordinates, constants.DIMENSIONS.stone_size)
                else:
                    point.team = None
        pygame.display.flip()

    def update_board(self):
        for line in self.grid:
            for point in line:
                if not point.team:
                    continue
                if not point.is_in_group():
                    if not point.has_liberties():
                        point.team = None
                else:
                    group = PointGroup(point)
                    if not group.has_liberties():
                        group.erase()
                        Point.ko = None

    def get_game_infos(self):
        white_territory = 0
        black_territory = 0

        for line in self.grid:
            for point in line:
                if point.team == constants.Team.WHITE:
                    white_territory += 1
                elif point.team == constants.Team.BLACK:
                    black_territory += 1
                elif not point.team:
                    adjacent_points = point.get_adjacent_points()
                    for elt in adjacent_points:
                        if elt.team and elt.team != point.team:
                            continue


        infos = {}
        if white_territory > black_territory:
            infos["winning_team"] = "Winner: WHITE"
        elif white_territory < black_territory:
            infos["winning_team"] = "Winner: BLACK"
        else:
            infos["winning_team"] = "Winner: Nobody"

        return infos
