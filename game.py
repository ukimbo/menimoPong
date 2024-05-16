import pygame, sys, random, button
from networking import Network

#Classes
class Ball:
    def __init__(self, speed):
        self.rectangle = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
        self.speed_x = speed * random.choice((1, -1))
        self.speed_y = speed * random.choice((1, -1))
        self.score_time = 0 
        self.active = False

    def collisions(self, p0, p1):
        if self.rectangle.bottom >= screen_height or self.rectangle.top <= 0:
            self.speed_y *= -1
        if self.rectangle.colliderect(p0.rectangle) and self.speed_x > 0:
            if abs(self.rectangle.right - p0.rectangle.left) < 20:
                self.speed_x *= -1
                p0.hits += 1
            if abs(self.rectangle.bottom - p0.rectangle.top) < 20 and self.speed_y > 0:
                self.speed_y *= -1
            if abs(self.rectangle.top - p0.rectangle.bottom) < 20 and self.speed_y < 0:
                self.speed_y *= -1
        if self.rectangle.colliderect(p1.rectangle) and self.speed_x < 0:
            if abs(self.rectangle.left - p1.rectangle.right) < 20:
                self.speed_x *= -1
                p1.hits += 1
            if abs(self.rectangle.bottom - p1.rectangle.top) < 20 and self.speed_y > 0:
                self.speed_y *= -1
            if abs(self.rectangle.top - p1.rectangle.bottom) < 20 and self.speed_y < 0:
                self.speed_y *= -1
    
    def ball_animations(self, p0, p1): #Game functions
        #players is a tuple of the rectangles of the players
        if self.active == True:
            self.rectangle.x += self.speed_x
            self.rectangle.y += self.speed_y
            self.collisions(p0, p1)
        else:
            self.prematch_timer()
        
        
    def reset_ball(self):
        self.active = False
        if abs(self.speed_x) > 7:
            self.speed_x = 14 * random.choice((1, -1, 0.5, -0.5))
        else:
            self.speed_x = 7 * random.choice((1, -1, 2, -2))
        self.speed_y = 7 * random.choice((1, -1))
        self.score_time = pygame.time.get_ticks()
        self.rectangle.center = (screen_width/2, screen_height/2)


    def prematch_timer(self):
        current_time = pygame.time.get_ticks() #Assuming self.score_time has a Truthy value, this function will be called repeatedly until ...
        countdown = ""
        if self.score_time == 0: 
            self.score_time = current_time
            self.prematch_timer()
        else:
            if current_time - self.score_time < 1000:
                countdown = "3"
            elif 1000 < current_time - self.score_time < 2000:
                countdown = "2"
            elif 2000 < current_time - self.score_time < 3000: 
                countdown = "1"
            if current_time - self.score_time > 3000: # ... until this condition is met
                self.active = True
        timer_text = timer_font.render(countdown, False, grey_again)
        screen.blit(timer_text, (633, 380))

class Player:
    def __init__(self, left, top, speed, score = 0):
        self.rectangle = pygame.Rect(left, top, 10, 140)
        self.speed = speed
        self.score = 0
        self.motion = 0
        self.hits = 0

    def constrains(self):
        if self.rectangle.top <= 0:
            self.rectangle.top = 0
        if self.rectangle.bottom >= screen_height:
            self.rectangle.bottom = screen_height

    def player_animations(self):
        self.rectangle.y += self.motion
        self.constrains()

class AI(Player):
    def player_animations(self):
        if self.rectangle.centery <= game_ball.rectangle.centery:
            self.rectangle.top += self.speed
        else:
            self.rectangle.top -= self.speed
        self.constrains()

class GameInfo:
    def __init__(self, game, player0, player1):
        self.p0_hits = player0.hits
        self.p1_hits = player1.hits
        self.p0_score = game.p0_score
        self.p1_score = game.p1_score

class Game:
    def __init__(self, ball, player0, player1):
        self.p0_score = 0
        self.p1_score = 0
        self.ball = ball
        self.player0 = player0
        self.player1 = player1
    def reset_ball(self):
        if self.ball.rectangle.right >= screen_width:
            self.p1_score += 1
            self.ball.reset_ball()
        if self.ball.rectangle.left <= 0:
            self.p0_score += 1 
            self.ball.reset_ball()

    def run_game(self):
        game_ball.ball_animations(self.player0, self.player1)
        self.player0.player_animations()
        self.player1.player_animations()
        self.reset_ball()
        self.update()
        game_info = GameInfo(self, self.player0, self.player1)
        return game_info
    
    def update(self):
        pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))
        pygame.draw.rect(screen, light_grey, self.player0.rectangle) #In other words, screen.fill is below the players, ball and aaline
        pygame.draw.rect(screen, light_grey, self.player1.rectangle)
        pygame.draw.ellipse(screen, light_grey, self.ball.rectangle)
        self.scoreboard()

    def scoreboard(self):
        player0_text = score_font.render(f"{self.p0_score}", False, light_grey)
        screen.blit(player0_text, (660, 470))
        player1_text = score_font.render(f"{self.p1_score}", False, light_grey)
        screen.blit(player1_text, (600, 470))

# Initial and required setup
pygame.init() # Needed for every pygame, iniates ALL the pygame modules
clock = pygame.time.Clock() #pygame clock method

#Window/GUI Setup
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('menimoPong')

#Colors
grey_color = pygame.Color('gray12')
light_grey = pygame.Color(200, 200, 200)
grey_again = pygame.Color('gray75')

#Initate Sprites
game_ball = Ball(7) #first arg is a rectangle that creates a "frame" to contain the size of the ball
player0 = Player(screen_width - 20, screen_height/2 - 70, 7)
player1 = AI(10, screen_height/2 - 70, 7)
player2 = Player(10, screen_height/2 - 70, 7)

# Initializing Fonts
score_font = pygame.font.SysFont("onyx", 48)
timer_font = pygame.font.SysFont("onyx", 72)

font_location = ".\game\PressStart2P-vaV7.ttf"

ALT_FONT = pygame.font.Font(font_location, 40) #"menimo"
ALT_TEXT = ALT_FONT.render("menimo", True, light_grey)
ALT_RECT = ALT_TEXT.get_rect(center = (640, 160))

MENU_FONT = pygame.font.Font(font_location, 100) #"Pong"
MENU_TEXT = MENU_FONT.render("Pong", True, light_grey)
MENU_RECT = MENU_TEXT.get_rect(center = (640, 220))

BUTTON_FONT = pygame.font.Font(font_location, 65)

#Main Menu function
def main_manu():
    while True:
        screen.fill(pygame.Color('gray5'))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        play_button = button.Button(None, 640, 480, BUTTON_FONT, "Play", light_grey, pygame.Color('darkslategray4'))
        quit_button = button.Button(None, 640, 720, ALT_FONT, "Quit", light_grey, pygame.Color('darkslategray4'))

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(ALT_TEXT, ALT_RECT)
        for b in [play_button, quit_button]:
            b.hover(MENU_MOUSE_POS)
            b.update(screen)
        for event in pygame.event.get(): #This specific loop handles the inputs of the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if play_button.click(MENU_MOUSE_POS):
                        play_menu()
                if pygame.mouse.get_pressed()[0]:
                    if quit_button.click(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
        pygame.display.flip()
        clock.tick(120)

#Play Menu function
def play_menu():
    running = True
    while running:
        screen.fill(pygame.Color('gray5'))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        one_p_button = button.Button(None, 410, 460, ALT_FONT, "1 Player", light_grey, pygame.Color('darkslategray4'))
        two_p_button = button.Button(None, 880, 460, ALT_FONT, "2 Player", light_grey, pygame.Color('darkslategray4'))
        online_button = button.Button(None, 640, 650, ALT_FONT, "Online???", light_grey, pygame.Color('darkslategray4'))
        back_button = button.Button(None, 640, 820, pygame.font.Font(font_location, 25), "Back", light_grey, pygame.Color('darkslategray4'))

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(ALT_TEXT, ALT_RECT)

        for b in [two_p_button, one_p_button, online_button, back_button]:
            b.hover(MENU_MOUSE_POS)
            b.update(screen)
        for event in pygame.event.get(): #This specific loop handles the inputs of the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if one_p_button.click(MENU_MOUSE_POS):
                        play_game(player0, player1)
                if pygame.mouse.get_pressed()[0]:
                    if two_p_button.click(MENU_MOUSE_POS):
                        play_game(player0, player2)
                if pygame.mouse.get_pressed()[0]:
                    if back_button.click(MENU_MOUSE_POS):
                        running = False
                if pygame.mouse.get_pressed()[0]:
                    if online_button.click(MENU_MOUSE_POS):
                        online()
        pygame.display.flip()
        clock.tick(120)

#Game function
def play_game(p1, p2):
    pong = Game(game_ball, p1, p2)
    game_ball.score_time = 0
    pong.player0.rectangle.center = (screen_width - 15, screen_height/2)
    pong.player1.rectangle.center = (15, screen_height/2)
    game_ball.reset_ball()
    game_ball.prematch_timer()
    running = True
    while running: #usually at the bottom of the code
        # events can be player movement, mouse clicks, scoring etc.
        # this loop constantly updates the game through applying the events and returning their effects on the display
        for event in pygame.event.get(): #This specific loop handles the inputs of the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Right Paddle Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pong.player0.motion += pong.player0.speed
                if event.key == pygame.K_UP:
                    pong.player0.motion -= pong.player0.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pong.player0.motion -= pong.player0.speed
                if event.key == pygame.K_UP:
                    pong.player0.motion += pong.player0.speed
            
            #Left Paddle Movement
            if event.type == pygame.KEYDOWN: # and not isinstance(pong.player1, AI):
                if event.key == pygame.K_s:
                    pong.player1.motion += pong.player1.speed
                if event.key == pygame.K_w:
                    pong.player1.motion -= pong.player1.speed
            if event.type == pygame.KEYUP: # and not isinstance(pong.player1, AI):
                if event.key == pygame.K_s:
                    pong.player1.motion -= pong.player1.speed
                if event.key == pygame.K_w:
                    pong.player1.motion += pong.player1.speed
        
        # Visuals
        screen.fill(grey_color) #Succesive elements are drawn on top of each other

        pong.run_game()
        
        pygame.display.flip()
        clock.tick(60)

#Online Functionality
def read_pos(string): #takes string tuple and converts it to an actual tuple of integers
    string = string.split(",")
    return int(string[0]), int(string[1])
def make_pos(tup): #takes tuple of integers and converts it into a string
    return str(tup[0]) + "," + str(tup[1]) 

def online():
    running = True
    n = Network()
    startPos = read_pos(n.getPos())
    op1 = Player(startPos[0], startPos[1], 7)
    op2 = Player(10, screen_height/2 - 70, 7)
    pong = Game(game_ball, op1, op2)
    game_ball.score_time = 0
    pong.player0.rectangle.center = (screen_width - 15, screen_height/2)
    pong.player1.rectangle.center = (15, screen_height/2)
    game_ball.reset_ball()
    game_ball.prematch_timer()
    while running: #usually at the bottom of the code
        p2Pos = read_pos(n.send(make_pos((op1.rectangle.x, op2.rectangle.y))))
        op2.rectangle.x = p2Pos[0]
        op2.rectangle.y = p2Pos[1]
        for event in pygame.event.get(): #This specific loop handles the inputs of the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Right Paddle Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pong.player0.motion += pong.player0.speed
                if event.key == pygame.K_UP:
                    pong.player0.motion -= pong.player0.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pong.player0.motion -= pong.player0.speed
                if event.key == pygame.K_UP:
                    pong.player0.motion += pong.player0.speed
        
        # Visuals
        screen.fill(grey_color) #Succesive elements are drawn on top of each other

        pong.run_game()
        
        pygame.display.flip()
        clock.tick(60)

main_manu()