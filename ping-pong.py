import pygame
pygame.init()

running = True
clock = pygame.time.Clock()

WIDTH = 1000
HEIGHT = 600
WHITE = (255, 255, 255)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('pong')
FPS = 60

''' C L A S S E S '''
class GameSprite():
    def __init__(self, image, x=100, y=100):
        self.image = image
        self.hitbox = self.image.get_rect(center = (x, y))

class Player(GameSprite):
    def __init__(self, image, x=100, control_type=True, is_enemy=False):
        super().__init__(image, x, y=HEIGHT//2)
        if is_enemy:
            self.collisionside = self.hitbox.left
        else:
            self.collisionside = self.hitbox.right
        self.collidehitbox = pygame.Rect(self.collisionside, self.hitbox.top, 1, self.hitbox.height)
        self.speed = 10
        self.points = 0
        self.is_using_arrows = control_type

    def update(self):
        if not finish:
            keys = pygame.key.get_pressed()
            if self.is_using_arrows:
                if keys[pygame.K_UP] and self.hitbox.top > 0:
                    self.hitbox.y -= self.speed
                elif keys[pygame.K_DOWN] and self.hitbox.bottom < HEIGHT:
                    self.hitbox.y += self.speed
            else:
                if keys[pygame.K_w] and self.hitbox.top > 0:
                    self.hitbox.y -= self.speed
                elif keys[pygame.K_s] and self.hitbox.bottom < HEIGHT:
                    self.hitbox.y += self.speed

            self.collidehitbox.left = self.collisionside
            self.collidehitbox.top = self.hitbox.top

class Bot(GameSprite):
    def __init__(self, image, x=WIDTH-100, y=HEIGHT//2):
        super().__init__(image, x, y)
        # self.hitbox.center = (600, 250)
        self.collidehitbox = pygame.Rect(self.hitbox.left, self.hitbox.top, 1, self.hitbox.height)
        self.speed = 8
        self.points = 0
    
    def update(self):
        if not finish:
            if ball.hitbox.x >= WIDTH//64*46:
                if ball.hitbox.y > self.hitbox.y and self.hitbox.bottom < HEIGHT:
                    self.hitbox.y += self.speed
                elif ball.hitbox.y < self.hitbox.y and self.hitbox.top > 0:
                    self.hitbox.y -= self.speed
                self.collidehitbox.left = self.hitbox.left
                self.collidehitbox.top = self.hitbox.top

class Ball(GameSprite):
    def __init__(self, image):
        GameSprite.__init__(self, image, x=WIDTH//2, y=HEIGHT//2)
        self.speed = 8
        self.speed_x = self.speed
        self.speed_y = self.speed
        self.count = 0
        self.start_counting = False

    def update(self):
        if not finish:
            if not self.start_counting:
                self.hitbox.x += self.speed_x
                self.hitbox.y -= self.speed_y

            if self.hitbox.right >= WIDTH:
                self.speed_x = -self.speed_x
                self.hitbox.center = (WIDTH//2, HEIGHT//2)
                player.points += 1
                self.start_counting = True
            if self.hitbox.left <= 0:
                self.speed_x = -self.speed_x
                self.hitbox.center = (WIDTH//2, HEIGHT//2)
                enemy.points += 1
                self.start_counting = True


            if self.hitbox.top <= 0 or self.hitbox.bottom >= HEIGHT:
                self.speed_y = -self.speed_y

            if self.hitbox.colliderect(player.collidehitbox):
                self.speed_x = self.speed
            elif self.hitbox.colliderect(enemy.collidehitbox):
                self.speed_x = -self.speed

    def count_2_secs(self):
        if self.start_counting:
            if self.count == 120:
                self.count = 0
                self.start_counting = False
            else:
                self.count += 1
        


class Timer(GameSprite):
    def __init__(self, image, end_time=(3,0)):
        self.seconds = end_time[1]
        self.minutes = end_time[0]
        super().__init__(image)
        self.hitbox.center = (WIDTH//2, HEIGHT-40)
        # self.end_time = end_time

    def show_the_time(self):
        if len(str(self.seconds)) == 1:
            seconds = '0' + str(self.seconds)
        else:
            seconds = str(self.seconds)

        self.image = mid_robotroc.render(
            str(self.minutes) + ':' + seconds,
            False, WHITE
            )
        
        self.hitbox = self.image.get_rect()
        self.hitbox.center = (WIDTH//2, HEIGHT-40)
    
    def update(self):
        if i == FPS:
            self.seconds -= 1
        
        if self.seconds == -1:
            self.minutes -= 1
            self.seconds = 59

        self.show_the_time()

    
    def check_the_time(self):
        if self.minutes == 0 and self.seconds == 0:
            return True

class Count(GameSprite):
    def __init__(self):
        self.score = [player.points, enemy.points]
        image = big_robotroc.render(
            str(self.score[0]) + '   |   ' + str(self.score[1]),
            False, WHITE
            )
        super().__init__(image, x=WIDTH//2, y=35)
    
    def update(self):
        if self.score[0] < player.points:
            self.score[0] += 1
        if self.score[1] < enemy.points:
            self.score[1] += 1
        
        self.image = big_robotroc.render(
            str(self.score[0]) + '   :   ' + str(self.score[1]),
            False, WHITE
            )
        self.hitbox = self.image.get_rect()
        self.hitbox.center = (WIDTH//2, 35)
    
    def clear_score(self):
        player.points = 0
        enemy.points = 0
        self.__init__()

class GameModeController():
    def __init__(self):
        self.gamemode = [gamemodeText1, gamemodeText2]
        self.controls = [controlsText1, controlsText2]
        self.time = [timeText1, timeText2, timeText3]

        self.gamemode_is_chosen = False
        self.controls_are_chosen = False
        self.time_is_chosen = False

        self.enemy_is_a_bot = True
        self.p1_uses_arrows = False
        self.timestr_list = ['030', '100', '130', '200', '230', '300']

        self.complete = False

    def update(self):
        if not self.gamemode_is_chosen:
            for text in self.gamemode:
                window.blit(text.image, text.hitbox)
            
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_1]:
                self.enemy_is_a_bot = True
                self.gamemode_is_chosen = True
            elif keys[pygame.K_2]:
                self.enemy_is_a_bot = False
                self.gamemode_is_chosen = True

        if self.gamemode_is_chosen and not self.controls_are_chosen:
            for text in self.controls:
                window.blit(text.image, text.hitbox)

            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_3]:
                self.p1_uses_arrows = False
                self.controls_are_chosen = True
            elif keys[pygame.K_4]:
                self.p1_uses_arrows = True
                self.controls_are_chosen = True

        if self.gamemode_is_chosen and self.controls_are_chosen and not self.time_is_chosen:
            for text in self.time:
                window.blit(text.image, text.hitbox)
            timestr = None
            bigstr = ''
            iteration = 0
            for item in self.timestr_list:
                iteration += 1
                bigstr += str('['+str(iteration)+'] - '+item[0] + ':' + item[1:3]+ '; ')
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_1]:
                timestr = self.timestr_list[0]
            elif keys[pygame.K_2]:
                timestr = self.timestr_list[1]
            elif keys[pygame.K_3]:
                timestr = self.timestr_list[2]
            elif keys[pygame.K_4]:
                timestr = self.timestr_list[3]
            elif keys[pygame.K_5]:
                timestr = self.timestr_list[4]
            elif keys[pygame.K_6]:
                timestr = self.timestr_list[5]
            
            if timestr != None:
                timer.minutes = int(timestr[0])
                timer.seconds = int(timestr[1] + timestr[2])

            if keys[pygame.K_c]:
                self.time_is_chosen = True
                self.complete = True
            
            self.time[1].image = robotroc.render(bigstr, False, WHITE)
            self.time[1].hitbox = self.time[1].image.get_rect(center=(WIDTH//2, HEIGHT//3*2))
            timer.show_the_time()


''' F U N C T I O N S'''
def reset():
    player.__init__(plate_img)
    enemy.__init__(plate_img, x=WIDTH-100)
    ball.__init__(ball_img)
    timer.__init__(mid_robotroc.render('0:00', False, WHITE))
    count.__init__()
    controller.__init__()


''' S P R I T E S '''
plate_img = pygame.image.load('images/plate.png')
ball_img = pygame.image.load('images/ball.png')


''' F O N T S   &   T E X T'''
pygame.font.init()
robotroc = pygame.font.Font('font/RobotRocNotATilter-YjKL.ttf', 16)
big_robotroc = pygame.font.Font('font/RobotRoc-8X2A.ttf', 60)
mid_robotroc = pygame.font.Font('font/RobotRoc-8X2A.ttf', 30)
# verdana = pygame.font.SysFont('verdana', 32, True, False)

p_for_pause_text = robotroc.render('[P] - pause', False, WHITE)
pause_text = big_robotroc.render('PAUSED', False, WHITE)
continue_text = robotroc.render('[C] - continue', False, WHITE)
reset_text = robotroc.render('[R] - reset', False, WHITE)

arrows_text = robotroc.render('Use arrows to move', False, WHITE)

gamemode_text1 = mid_robotroc.render('Choose the opponent', False, WHITE)
gamemode_text2 = mid_robotroc.render('[1] - Bot; [2] - P2', False, WHITE)

controls_text1 = mid_robotroc.render('Choose controls for P1', False, WHITE)
controls_text2 = mid_robotroc.render('[3] - [W & S]; [4] - Arrows', False, WHITE)

time_choosing_text1 = mid_robotroc.render('Choose timer', False, WHITE)
time_choosing_text2 = mid_robotroc.render('0:00', False, WHITE)

time_out_text = big_robotroc.render('TIMEOUT!', False, WHITE)


''' O B J E C T S '''
gamemodeText1 = GameSprite(gamemode_text1, x=WIDTH//2, y=HEIGHT//3)
gamemodeText2 = GameSprite(gamemode_text2, x=WIDTH//2, y=HEIGHT//3*2)

controlsText1 = GameSprite(controls_text1, x=WIDTH//2, y=HEIGHT//3)
controlsText2 = GameSprite(controls_text2, x=WIDTH//2, y=HEIGHT//3*2)

timeText1 = GameSprite(time_choosing_text1, x=WIDTH//2, y=HEIGHT//3)
timeText2 = GameSprite(time_choosing_text2, x=WIDTH//2, y=HEIGHT//3*2)
timeText3 = GameSprite(continue_text, x=WIDTH//2, y=HEIGHT//4*3)

controller = GameModeController()

pauseText = GameSprite(pause_text, x=WIDTH//2, y=HEIGHT//2)
continueText = GameSprite(continue_text, x=WIDTH//2, y=HEIGHT//3*2)
resetText = GameSprite(reset_text, x=WIDTH//2, y=HEIGHT//3*2+20)
timeoutText = GameSprite(time_out_text, x=WIDTH//2, y=HEIGHT//2)

line = GameSprite(pygame.Surface((10, HEIGHT)), x=WIDTH//2, y=HEIGHT//2)
line.image.fill((92, 92, 92)) # grey

ball = Ball(ball_img)
player = Player(plate_img, control_type=controller.p1_uses_arrows)
if controller.enemy_is_a_bot:
    enemy = Bot(plate_img)
else:
    enemy = Player(plate_img, control_type=not controller.p1_uses_arrows, is_enemy=True)
timer = Timer(mid_robotroc.render('0:00', False, WHITE))
count = Count()


''' C Y C L E '''
i = 0
finish = True
paused = False
finish_priority = True
time_out_bool = False



while running:

    window.fill((0,0,0))

    window.blit(line.image, line.hitbox)
    
    window.blit(player.image, player.hitbox)
    player.update()

    window.blit(enemy.image, enemy.hitbox)
    enemy.update()

    window.blit(ball.image, ball.hitbox)
    ball.update()
    ball.count_2_secs()

    window.blit(p_for_pause_text, (0, 0))
    # window.blit(arrows_text, (0, 20))
    # window.blit(pause_text, (200, 200))

    if paused:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_c]:
            if not finish_priority:
                finish = False
            paused = False
        
        if keys[pygame.K_r]:
            finish = True
            finish_priority = True
            paused = False
            reset()
        window.blit(pauseText.image, pauseText.hitbox)
        window.blit(continueText.image, continueText.hitbox)
        window.blit(resetText.image, resetText.hitbox)
        timer.update()
        
    else:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_p] and not finish_priority:
            finish = True
            paused = True

        if i == FPS:
            i = 0
            
        else:
            i += 1
        
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    # timer = big_robotroc.render(str(i_2),False, WHITE)
    window.blit(timer.image, timer.hitbox)
    if not finish:
        timer.update()
        if not finish_priority:
            time_out_bool = timer.check_the_time()
            finish = time_out_bool
    # pause = timer.check_the_time()
            
    if time_out_bool:
        window.blit(timeoutText.image, timeoutText.hitbox)
        window.blit(resetText.image, (resetText.hitbox.x, resetText.hitbox.y - 20))
        if keys[pygame.K_r]:
            finish = True
            finish_priority = True
            reset()
            time_out_bool = False

    window.blit(count.image, count.hitbox)
    count.update()

    controller.update()
    if controller.complete:
        player = Player(plate_img, control_type=controller.p1_uses_arrows)
        if controller.enemy_is_a_bot:
            enemy = Bot(plate_img)
        else:
            enemy = Player(plate_img, x=WIDTH-100, control_type=not controller.p1_uses_arrows)
        finish = False
        finish_priority = False
        controller.complete = False
    
    
    pygame.display.update()
    clock.tick(FPS)