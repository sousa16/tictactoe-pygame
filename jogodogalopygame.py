import time

import pygame
from autopickplay import available_square, mark_square, get_row, get_col, get_diag, auto_pick_pos

pygame.init()
WIDTH, HEIGHT, LINE_WIDTH, NUM_ROWS, NUM_COLS, PLAYER, GAMEMODE, LOOP, PLAYER_TURN, SLEEP = 600, 600, 10, 3, 3, 0, 0, 1, 0, True
BOARD = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
COLORS = {'BG_COLOR': (28, 170, 156), 'LINE_COLOR': (23, 145, 135), 'WHITE': (255, 255, 255),
          'DARK_GREY': (68, 68, 68), 'RED': (220, 20, 60)}
FONT = pygame.font.SysFont('Comfortaa Light', 30)
BUTTONS = []
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')


def main():
    global PLAYER, GAMEMODE, LOOP, PLAYER_TURN, BOARD, BUTTONS, SLEEP

    run = True
    while run:
        if LOOP == 1:
            main_menu()
        elif LOOP == 2:
            pick_a_player()
        elif LOOP == 3:
            draw_window()
            draw_board()
            pygame.display.update()
            LOOP += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if LOOP == 1 and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                for button in BUTTONS:
                    if GAMEMODE == 0 and button[1] <= mouseX <= button[2] and button[3] <= mouseY <= button[4]:
                        GAMEMODE = button[0]
                        if GAMEMODE != '2 PLAYERS':
                            LOOP += 1
                        else:
                            PLAYER = 1
                            LOOP += 2
            elif LOOP == 2 and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                for button in BUTTONS[4:]:
                    if PLAYER == 0 and button[1] <= mouseX <= button[2] and button[3] <= mouseY <= button[4]:
                        if button[0] == 'X':
                            PLAYER = 1
                            PLAYER_TURN = True
                        else:
                            PLAYER = -1
                            PLAYER_TURN = False
                        LOOP += 1
            elif LOOP > 3:
                if GAMEMODE == '2 PLAYERS':
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]

                        clicked_row = int(mouseX // 200)
                        clicked_col = int(mouseY // 200)

                        if available_square(BOARD, clicked_row, clicked_col):
                            if PLAYER == 1:
                                draw_play(clicked_row, clicked_col, 1)
                                mark_square(BOARD, clicked_row, clicked_col, 1)
                                PLAYER = -1
                            elif PLAYER == -1:
                                draw_play(clicked_row, clicked_col, -1)
                                mark_square(BOARD, clicked_row, clicked_col, -1)
                                PLAYER = 1
                            pygame.display.update()
                else:
                    if PLAYER_TURN:
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            mouseX = event.pos[0]
                            mouseY = event.pos[1]

                            clicked_row = int(mouseX // 200)
                            clicked_col = int(mouseY // 200)

                            if available_square(BOARD, clicked_row, clicked_col):
                                draw_play(clicked_row, clicked_col, PLAYER)
                                mark_square(BOARD, clicked_row, clicked_col, PLAYER)
                                PLAYER_TURN = False
                        pygame.display.update()
                    if not (PLAYER_TURN or game_over()):
                        time.sleep(0.5)
                        draw_play(auto_pick_pos(BOARD, -PLAYER, GAMEMODE)[0], auto_pick_pos(BOARD, -PLAYER, GAMEMODE)[1], -PLAYER)
                        mark_square(BOARD, auto_pick_pos(BOARD, -PLAYER, GAMEMODE)[0], auto_pick_pos(BOARD, -PLAYER, GAMEMODE)[1], -PLAYER)
                        PLAYER_TURN = True
                        pygame.display.update()
                if game_over():
                    if SLEEP:
                        time.sleep(0.5)
                        SLEEP = False
                    draw_window()
                    if GAMEMODE != '2 PLAYERS':
                        if winning_player() == PLAYER:
                            write_text('CONGRATULATIONS, YOU WON!', COLORS['WHITE'], 230, 50)
                        elif winning_player() == -PLAYER:
                            write_text('YOU LOST', COLORS['WHITE'], 230, 50)
                    else:
                        if winning_player() == 1:
                            write_text('X WON!', COLORS['WHITE'], 230, 50)
                        elif winning_player() == -1:
                            write_text('O WON!', COLORS['WHITE'], 230, 50)

                    if winning_player() == 0:
                        write_text('DRAW', COLORS['WHITE'], 230, 50)

                    write_text('DO YOU WANT TO PLAY AGAIN?', COLORS['WHITE'], 230, 200)
                    yesorno = [['YES', 135], ['NO', 325]]
                    for button in yesorno:
                        draw_button(button[0], button[1], 350)

                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        for button in BUTTONS[-2:]:
                            if button[1] <= mouseX <= button[2] and button[3] <= mouseY <= button[4]:
                                if button[0] == 'YES':
                                    BOARD = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                                    BUTTONS = []
                                    PLAYER, GAMEMODE, LOOP, PLAYER_TURN, SLEEP = 0, 0, 1, 0, True
                                    main()
                                else:
                                    pygame.quit()
                                    exit()

        pygame.display.update()

    pygame.quit()
    exit()


def draw_window():
    WIN.fill(COLORS['BG_COLOR'])


def write_text(text, color, x, y):
    label = FONT.render(text, True, color)
    label_rect = label.get_rect(center=(x + 70, y + 30))
    WIN.blit(label, label_rect)


def draw_button(text, x, y):
    pygame.draw.rect(WIN, COLORS['LINE_COLOR'], [x, y, 140, 60])
    if [text, x, x+140, y, y+60] not in BUTTONS:
        BUTTONS.append([text, x, x+140, y, y+60])
    write_text(text, COLORS['WHITE'], x, y)


def draw_board():
    # 1 vertical
    pygame.draw.line(WIN, COLORS['LINE_COLOR'], (200, 0), (200, 600), LINE_WIDTH)
    # 2 vertical
    pygame.draw.line(WIN, COLORS['LINE_COLOR'], (400, 0), (400, 600), LINE_WIDTH)
    # 1 horizontal
    pygame.draw.line(WIN, COLORS['LINE_COLOR'], (0, 200), (600, 200), LINE_WIDTH)
    # 2 horizontal
    pygame.draw.line(WIN, COLORS['LINE_COLOR'], (0, 400), (600, 400), LINE_WIDTH)


def is_board_full():
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if BOARD[row][col] == 0:
                return False
    return True


def draw_play(row, col, p):
    if p == 1:
        pygame.draw.line(WIN, COLORS['DARK_GREY'], (200 * row + 40, 200 * col + 40), (
            200 * row + 160, 200 * col + 160), LINE_WIDTH)
        pygame.draw.line(WIN, COLORS['DARK_GREY'], (200 * row + 40, 200 * col + 160), (
            200 * row + 160, 200 * col + 40), LINE_WIDTH)
    elif p == -1:
        pygame.draw.circle(WIN, COLORS['RED'], (200 * row + 100, 200 * col + 100), 60, LINE_WIDTH)


def winning_player():
    vit = ((1, 1, 1), (-1, -1, -1))

    for a in range(0, 3):
        for c in vit:

            if get_row(BOARD, a) == c or get_col(BOARD, a) == c:
                return c[0]
            elif a != 3 and get_diag(BOARD, a) == c:
                return c[0]
    if is_board_full():
        return 0


def main_menu():
    draw_window()
    write_text('TIC TAC TOE', COLORS['WHITE'], 230, 50)
    gamemodes = [['EASY', 150], ['NORMAL', 250], ['HARD', 350], ['2 PLAYERS', 450]]
    for button in gamemodes:
        draw_button(button[0], 230, button[1])


def pick_a_player():
    draw_window()
    write_text('DO YOU WANT TO PLAY AS X OR O?', COLORS['WHITE'], 230, 50)
    players = [['X', 135], ['O', 325]]
    for player in players:
        draw_button(player[0], player[1], 200)


def game_over():
    if winning_player() == 1 or winning_player() == -1 or is_board_full():
        return True
    return False


main()