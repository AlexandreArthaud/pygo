import pygame
import sys

import constants

def quit():
    pygame.quit()
    sys.exit(0)

def common_events(event):
    if event.type == pygame.QUIT:
        quit()

def is_opposite_team(ateam, bteam):
    if (ateam == constants.Team.WHITE and bteam == constants.Team.BLACK or
        ateam == constants.Team.BLACK and bteam == constatns.TEAM.WHITE):
        return True
    return False

def get_opposite_team(team):
    if team == constants.Team.WHITE:
        return constants.Team.BLACK
    else:
        return constants.Team.WHITE
