import neat.checkpoint
import neat.nn.feed_forward
import neat.population
import pygame
import random
import neat
import os
import numpy as np


pygame.init()
generation = 0
# VARIABLES

WIDTH = 800
HEIGHT = 800
p = None
score = 0
run = generation*50
reward = 0
score_font = pygame.font.SysFont('Segoe', 45)
run_font = pygame.font.SysFont('Segoe', 45)
enter = False
exit = False
passed = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
background = pygame.image.load("bird_ai/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT+20))
ground = pygame.image.load("bird_ai/ground.png").convert()
ground = pygame.transform.scale(ground, (WIDTH, 150))
ground_mask = pygame.mask.from_surface(ground)

# Sound
flap_sfx = pygame.mixer.Sound("bird_ai/flap.mp3")
score_sfx = pygame.mixer.Sound("bird_ai/score.mp3")
collide_sfx = pygame.mixer.Sound("bird_ai/collide.mp3")

pygame.display.set_caption("Flappy Bird AI")
# pygame.mouse.set_visible(False)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (80, 172, 247, 255)
GREEN = (133, 184, 68, 255)
RED = (255, 0, 0)
TRANSPARENT = (0, 0, 0, 0)
SKY = (0, 153, 204, 255)

class Bird():

    def __init__(self):

        self.x = 100
        self.y = HEIGHT // 2
        self.vel = 0
        self.flapPower = -15
        self.gravity = 1.5

        self.flappyUp = pygame.image.load("bird_ai/bird_up.png").convert()
        self.flappyUp = pygame.transform.scale(self.flappyUp, (70, 50))

        self.flappyDown = pygame.image.load("bird_ai/bird_down.png").convert()
        self.flappyDown = pygame.transform.scale(self.flappyDown, (70, 50))

        self.flappyMid = pygame.image.load("bird_ai/bird_mid.png").convert()
        self.flappyMid = pygame.transform.scale(self.flappyMid, (70, 50))

        self.images = [self.flappyUp, self.flappyMid, self.flappyDown]
        self.currentImage = 0
        self.flappyMask = pygame.mask.from_surface(self.images[self.currentImage])
        self.animationFrames = 0
          
    def drawBird(self, screen):
        rotation = 0
        if self.vel < 0:
            rotation = 30
        if self.vel > 0:
            rotation = max(-2*self.vel, -40)

        tiltedBird = pygame.transform.rotate(self.images[self.currentImage], rotation)
        self.flappyMask = pygame.mask.from_surface(tiltedBird)

        tiltedBird_rect = tiltedBird.get_rect(center=(self.x, self.y)) #centers the coordinates relative to the bird's image

        screen.blit(tiltedBird, tiltedBird_rect.topleft)
    
    def flap(self):
        self.vel = self.flapPower
        # flap_sfx.play()
    
    def update(self):
        self.vel += self.gravity
        self.y += self.vel

        self.animationFrames += 1
    
        if self.animationFrames == 5:
            self.currentImage = 0
        
        if self.animationFrames == 10:
            self.currentImage = 1
        
        if self.animationFrames == 15:
            self.currentImage = 2
        
        if self.animationFrames == 20:
            self.currentImage = 1
        
        if self.animationFrames == 30:
            self.currentImage = 0
            self.animationFrames = 0

        self.flappyMask = pygame.mask.from_surface(self.images[self.currentImage])

        
class Pipe:
    
    def __init__(self):
        self.vel = 7

        self.pipe_spacing = 300
        self.gap = 190
        self.flag = True
        
        self.x = WIDTH
        self.x2 = self.x + self.pipe_spacing
        self.x3 = self.x2 + self.pipe_spacing
        self.speed = 0.5
        self.random_y1 = random.randint(90,400)
        self.random_y2 = random.randint(90,400)
        self.random_y3 = random.randint(90,400)

        self.pipey_vel_1 = random.choice([-self.speed, self.speed])
        self.pipey_vel_2 = random.choice([-self.speed, self.speed])
        self.pipey_vel_3 = random.choice([-self.speed, self.speed])

        self.positions = [(self.x, self.random_y1, self.pipey_vel_1), (self.x2, self.random_y2, self.pipey_vel_2), (self.x3, self.random_y3, self.pipey_vel_3)]

        self.pipe_img = pygame.image.load("bird_ai/pipe.png").convert_alpha()  
        self.pipe_img = pygame.transform.scale(self.pipe_img, (100, 500)) 
        
        self.topPipe = pygame.transform.flip(self.pipe_img, False, True)
        self.bottomPipe = self.pipe_img

        self.top_mask = pygame.mask.from_surface(self.topPipe)
        self.bottom_mask = pygame.mask.from_surface(self.bottomPipe)
        self.bottom_mask_rect = self.bottomPipe.get_rect()

    def renderPipe(self, screen, x, y):
       
        #STARTS WHERE THE SPACER BEGINS - THE PIPE HEIGHT = TOP PLACEMENT
        topPipeHeight = y - self.pipe_img.get_height()
        screen.blit(self.topPipe, (x, topPipeHeight))

        #STARTS WHERE THE SPACER BEGINS + GAP = BOTTOM PLACEMENET
        bottomPipeHeight = y + self.gap

        screen.blit(self.bottomPipe, (x, bottomPipeHeight))


    def drawPipes(self, screen):
        
        for x, y, vel in self.positions:
            self.renderPipe(screen, x, y)

    def update(self):

        new_positions = []

        for x, y, vel in self.positions:
            x -= self.vel
            
            # IF PIPES GO OUT OF BOUNDS, CALL THEM AGAIN WITH PROPER SPACING IN BETWEEN, AND RE-RANDOMIZE THE SPACERS
            if x + 100 < 0:
                # finds the largest X coordinate within the each pair in the positions array
                x = max(pos[0] for pos in self.positions) + self.pipe_spacing
                y = random.randint(90, 400) 
                vel = random.choice([-self.speed, self.speed])
                

            y += vel

            if y <= 90 or y >= 400:
                vel*= -1 # reverse the direction once it hits the endpoints

            new_positions.append((x, y, vel))
        
        self.positions = new_positions

def checkCollisions(bird, pipe):
    global score, reward
    # Check if the bird hits the top of the screen or the ground
    if bird.y - bird.flappyMask.get_size()[1] // 2 < 0 or bird.y + bird.flappyMask.get_size()[1] // 2 > HEIGHT - 149:
        score = 0
        reward = -1000
        return True
    
    # Check if bird collides with the Pipe
    for x, y, vel in pipe.positions:
        top_offset = (x - (bird.x - bird.flappyMask.get_size()[0] // 2), # pipe's top left x  - bird's top left x
                      (y - pipe.pipe_img.get_height()) - (bird.y - bird.flappyMask.get_size()[1] // 2)) #pipe's top left y - bird's top left y
        
        bottom_offset = (x - (bird.x - bird.flappyMask.get_size()[0] // 2), #pipe's bottom left x - bird's bottom left x
                         (y + pipe.gap) - (bird.y - bird.flappyMask.get_size()[1] // 2)) #pipe's bottom left y - bird's bottom left y

        if bird.flappyMask.overlap(pipe.top_mask, top_offset) or bird.flappyMask.overlap(pipe.bottom_mask, bottom_offset):
            score = 0
            reward = -1000
            return True
            
    return False


def countScore(bird, pipe, genome):
    global score, passed, enter, exit, reward

    for x, y, vel in pipe.positions:
            
        # check if bird passes pipe = reward for scoring
        if (x + 100 <= bird.x < x + 100 + pipe.vel):
            print("Passed")
            passed = True
            score_sfx.play()
            genome.fitness += 5 # reward for scoring
            score += 1
            print("Score: ", score)

        if (bird.x > x + 100 + pipe.vel):
            passed = False # Reset once bird passes the area
            
def displayScore(screen, score):
    score_text = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (0,0))

def displayRun(screen, run):
    run_text = run_font.render("Run: " + str(run), True, WHITE)
    screen.blit(run_text, (WIDTH-150,0))

def displayGen(screen, gen):
    gen_text = run_font.render("Gen: " + str(gen), True, WHITE)
    screen.blit(gen_text, (WIDTH-150,0+50))

def get_closest_pipe (bird, pipe):
    closestPipe = None
    min_distance = float('inf')
    for position in pipe.positions:
        pipe_x, pipe_y, vel = position   
        distance = (pipe_x+130) - bird.x - 10

        if 0 < distance < min_distance:
            min_distance = distance
            closestPipe = position
    
    return closestPipe

def draw_tracer(screen, color, start_pos, end_pos, width=2):
    pygame.draw.line(screen, color, start_pos, end_pos, width)

def game_loop(genome, config):

    net = neat.nn.FeedForwardNetwork.create(genome, config)
    genome.fitness = 0
    frame_count = 0
    global run, reward, generation
    bird = Bird()
    pipe = Pipe()
    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if checkCollisions(bird, pipe):
            bird = Bird()
            pipe = Pipe()
            run += 1
            genome.fitness -= 1 # bad reward for collision
            break

        countScore(bird, pipe, genome)
        
        screen.fill(SKY)
        screen.blit(background, (0, 20))
       
        pipe.drawPipes(screen)
        displayScore(screen, score)
        displayRun(screen, run)
        displayGen(screen, generation-1)

        screen.blit(ground, (0, HEIGHT-150))
        bird.drawBird(screen)

        closestPipe = get_closest_pipe(bird, pipe)

        if closestPipe:

            closest_pipex, closest_pipey, vel = closestPipe

            distance_bird_to_pipe_top = abs(bird.y - closest_pipey)
            distance_bird_to_pipe_bottom = abs(bird.y - (closest_pipey + pipe.gap))
            bird_y = bird.y


            inputs = (
                bird_y, distance_bird_to_pipe_top, distance_bird_to_pipe_bottom
            )
                
            output = net.activate(inputs)

            # Decide whether to flap or not
            if output[0] > 0.5:  # If output is greater than 0.5, flap (tanh activation function = output of -1 or 1)
                bird.flap()

            # Update positions and bird after the action
            pipe.update()
            bird.update()

            genome.fitness += 0.1 #reward for staying alive/frame

        # Draw distance from bird to the bottom edge of the pipe's gap
        draw_tracer(screen, RED, (bird.x, bird.y), (closest_pipex + 50, closest_pipey + pipe.gap), width=6)

        # Draw distance from bird to the top edge of the pipe's gap
        draw_tracer(screen, RED, (bird.x, bird.y), (closest_pipex + 50, closest_pipey), width=6)



        pygame.display.flip()
        pygame.time.delay(30)
    

#fitness function takes genomes from the current population from the generation, and gives them a fitness, and make changes as it executes.

def eval_genomes(genomes, config):
    global p, generation
    generation += 1
    for genome_id, genome in genomes:
        game_loop(genome, config)
    
    
def run_neat(config):
    global p
    p = neat.Checkpointer.restore_checkpoint('bird_ai/neat-checkpoint-46')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True)) #report the data (seee generation, avg fitness, best fitness, etc)
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10)) # check point every 100 generations, so data can be saved, and if changes are to be made, can be referred back to by calling a certain checkpoint
    
    winner = p.run(eval_genomes, 50) # best fitness within 50 generations

    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    run_neat(config)

