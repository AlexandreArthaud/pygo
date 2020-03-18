import webbrowser
import pygame

import constants
import utils

class Menu:
    font = pygame.font.SysFont("comicsansms", 72)

    play_choice = font.render("Play", True, constants.LABEL_COLOR)
    play_choice_rect = play_choice.get_rect(center = (constants.DIMENSIONS.window_width//2, 100))

    rules_choice = font.render("Rules", True, constants.LABEL_COLOR)
    rules_choice_rect = rules_choice.get_rect(center = (constants.DIMENSIONS.window_width//2, 200))

    quit_choice = font.render("Quit", True, constants.LABEL_COLOR)
    quit_choice_rect = quit_choice.get_rect(center = (constants.DIMENSIONS.window_width//2, 300))

    nine_by_nine_goban_choice = font.render("9x9 Board", True, constants.LABEL_COLOR)
    nine_by_nine_goban_choice_rect = nine_by_nine_goban_choice.get_rect(center = (constants.DIMENSIONS.window_width//2, 100))
    thirteen_by_thirteen_goban_choice = font.render("13x13 Board", True, constants.LABEL_COLOR)
    thirteen_by_thirteen_goban_choice_rect = thirteen_by_thirteen_goban_choice.get_rect(center = (constants.DIMENSIONS.window_width//2, 200))
    nineteen_by_nineteen_goban_choice = font.render("19x19 Board", True, constants.LABEL_COLOR)
    nineteen_by_nineteen_goban_choice_rect = nineteen_by_nineteen_goban_choice.get_rect(center = (constants.DIMENSIONS.window_width//2, 300))
    return_choice = font.render("Back", True, constants.LABEL_COLOR)
    return_choice_rect = return_choice.get_rect(center = (constants.DIMENSIONS.window_width//2, 400))

    winner_label = None
    winner_label_rect = None


    main_menu = [[play_choice, play_choice_rect], [rules_choice, rules_choice_rect], [quit_choice, quit_choice_rect]]
    game_menu = [
                    [nine_by_nine_goban_choice, nine_by_nine_goban_choice_rect],
                    [thirteen_by_thirteen_goban_choice, thirteen_by_thirteen_goban_choice_rect],
                    [nineteen_by_nineteen_goban_choice, nineteen_by_nineteen_goban_choice_rect],
                    [return_choice, return_choice_rect]
                ]
    results_menu = [
        [return_choice, return_choice_rect],
        [quit_choice, quit_choice_rect]
    ]

    def __init__(self, surface):
        self.surface = surface
        self.current_menu = Menu.main_menu

    def set_menu(self, infos):
        if type(infos) == dict and "winning_team" in infos:
            winner_label = Menu.font.render(infos["winning_team"], True, constants.LABEL_COLOR)
            winner_label_rect = winner_label.get_rect(center = (constants.DIMENSIONS.window_width//2, 100))
            Menu.results_menu.append([winner_label, winner_label_rect])
            self.current_menu = Menu.results_menu
        else:
            pass

    def show_menu(self):
        self.surface.fill(constants.BLACK)
        for elt in self.current_menu:
            self.surface.blit(elt[0], elt[1])

    def run(self):
        self.show_menu()
        for event in pygame.event.get():
            utils.common_events(event)
            if event.type == pygame.MOUSEMOTION:
                mouseover = False
                for element in Menu.main_menu + Menu.game_menu + Menu.results_menu:
                    if element[1].collidepoint(event.pos):
                        pygame.mouse.set_cursor(*pygame.cursors.diamond)
                        mouseover = True
                if not mouseover:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_menu == Menu.main_menu:
                    if Menu.play_choice_rect.collidepoint(event.pos):
                        self.current_menu = Menu.game_menu
                        self.show_menu()
                    elif Menu.rules_choice_rect.collidepoint(event.pos):
                        webbrowser.open("https://en.wikipedia.org/wiki/Rules_of_Go")
                    elif Menu.quit_choice_rect.collidepoint(event.pos):
                        utils.quit()
                elif self.current_menu == Menu.game_menu:
                    if Menu.nine_by_nine_goban_choice_rect.collidepoint(event.pos):
                        return constants.GameChoice.NINE_BY_NINE_GOBAN
                    elif Menu.thirteen_by_thirteen_goban_choice_rect.collidepoint(event.pos):
                        return constants.GameChoice.THIRTEEN_BY_THIRTEEN_GOBAN
                    elif Menu.nineteen_by_nineteen_goban_choice_rect.collidepoint(event.pos):
                        return constants.GameChoice.NINETEEN_BY_NINETEEN_GOBAN
                    elif Menu.return_choice_rect.collidepoint(event.pos):
                        self.current_menu = Menu.main_menu
                        self.show_menu()
                elif self.current_menu == Menu.results_menu:
                    if Menu.return_choice_rect.collidepoint(event.pos):
                        self.current_menu = Menu.main_menu
                        self.show_menu()
                    elif Menu.quit_choice_rect.collidepoint(event.pos):
                        utils.quit()
            pygame.display.flip()
