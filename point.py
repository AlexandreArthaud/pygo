import utils
import point_group

class Point:
    grid = []
    ko = None

    def __init__(self, y, x):
        self.team = None
        self.y = y
        self.x = x

    def get_adjacent_points(self):
        adjacent_points = []
        positions_to_get = [
            (self.y - 1, self.x),
            (self.y + 1, self.x),
            (self.y, self.x - 1),
            (self.y, self.x + 1)
        ]

        for pos in positions_to_get:
            if pos[0] < 0 or pos[1] < 0:
                continue
            try:
                adjacent_points.append(Point.grid[pos[0]][pos[1]])
            except IndexError:
                continue
        return adjacent_points

    def has_empty_neighbor(self):
        for point in self.get_adjacent_points():
            if not point.team:
                return True
        return False

    def get_empty_neighbors(self):
        empty_points = []
        for point in self.get_adjacent_points():
            if not point.team:
                empty_points.append(point)
        return empty_points

    def is_surrounded(self, team, ignore=[]):
        for elt in self.get_adjacent_points():
            if elt in ignore:
                continue
            elif elt.team != team:
                return False
        return True

    def is_surrounded_by_surrounded(self, team, ignore=[]):
        opponent_points = self.get_adjacent_points()
        opponent_points = [x for x in opponent_points if x.team and x.team == utils.get_opposite_team(team)]

        for elt in opponent_points:
            if elt in ignore:
                continue
            if elt.is_in_group():
                opponent_group = point_group.PointGroup(elt)
                if not opponent_group.has_liberties([self]):
                    return elt
            else:
                if elt.is_surrounded(team, [self]) and not elt.is_surrounded_by_surrounded(utils.get_opposite_team(team), [self]):
                    return elt

    def is_playable(self, attacking_team):
        if not self.team:
            if self == Point.ko:
                print("Ko rule")
                return False
            if self.is_in_group(attacking_team):
                group = point_group.PointGroup(self, attacking_team)
                Point.ko = None
                if group.touches_surrounded():
                    return True
                return group.has_liberties([self])
            elif self.has_empty_neighbor():
                Point.ko = None
                return True
            elif self.is_surrounded(utils.get_opposite_team(attacking_team)):
                surr_by_surr = self.is_surrounded_by_surrounded(attacking_team)
                if surr_by_surr:
                    Point.ko = surr_by_surr
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_in_group(self, friendly_team=None):
        if self.team and not friendly_team:
            friendly_team = self.team

        friends = self.get_adjacent_points()
        friends = [x for x in friends if friendly_team and x.team == friendly_team]

        if friends:
            return True
        else:
            return False

    def has_liberties(self):
        if self.has_empty_neighbor():
            return True
        elif self.is_surrounded_by_surrounded(self.team) and self != Point.ko:
            return True
        else:
            return False
