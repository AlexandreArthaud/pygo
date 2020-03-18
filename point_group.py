import point
import utils

class PointGroup:
    def __init__(self, root, team=None):
        self.root = root
        if team:
            self.team = team
        else:
            self.team = root.team
        self.points = []
        self.points.append(root)
        self.collect_friendlies()

    def collect_friendlies(self):
        for elt in self.points:
            for point in elt.get_adjacent_points():
                if point.team == self.team and point not in self.points:
                    self.points.append(point)

    def erase(self):
        for elt in self.points:
            elt.team = None

    def is_surrounded(self, ignore=[]):
        surrounded = True
        for elt in self.points:
            if elt in ignore:
                continue
            if not elt.is_surrounded(self.team, self.points):
                surrounded = False
        return surrounded

    def touches_surrounded(self):
        surrounded_hostiles = False
        for elt in self.points:
            opponent_points = elt.get_adjacent_points()
            opponent_points = [x for x in opponent_points if x not in self.points and x.team == utils.get_opposite_team(self.team)]

            for x in opponent_points:
                if x.is_in_group(x.team):
                    group = PointGroup(x)
                    if not group.has_liberties(self.points):
                        group.erase()
                        surrounded_hostiles = True
                if x.is_surrounded(self.team, [elt]):
                    x.team = None
                    surrounded_hostiles = True

        return surrounded_hostiles

    def has_liberties(self, ignore=[]):
        surrounded = True
        for elt in self.points:
            if elt.has_empty_neighbor():
                # if one stone of the stone group has an empty neighbor, the chain is free
                empty_neighbors = elt.get_empty_neighbors()
                real_empty_point = False
                for empty_neighbor in empty_neighbors:
                    if empty_neighbor not in ignore:
                        real_empty_point = True

                if real_empty_point:
                    return True
            if self.team and (not elt.is_surrounded(self.team)):
                # if any single stone is NOT surrounded, the chain is not surrounded
                surrounded = False


        if surrounded:
            return surrounded

        return False
