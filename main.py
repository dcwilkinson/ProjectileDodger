import pygame
import time
import random
pygame.font.init()

WIDTH = 1000
HEIGHT = 800
FPS = 60

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Prjectile Dodger")

FONT = pygame.font.SysFont("Arial",30)

BGCOLOUR = (0, 0, 0)

PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 20
PROJECTILE_VEL = 10
PROJECTILE_RELEASE = 3 # how many projectiles drop at same time

HIT_THRESHOLD = 5

def checkGameOver(hits):
    gameOver = False
    if hits >= HIT_THRESHOLD:
        gameOver = True
    return gameOver

def gameOverMessage():
    centreCoords = (WIDTH/2, HEIGHT/2)
    gameOverText = FONT.render(f"GAME OVER!",1,"white")    
    WIN.blit(gameOverText,centreCoords)    

def draw(player,elapsedTime,projectiles,hits):
    
    WIN.fill(BGCOLOUR) # make sure fill is called first - otrherwise it fills entire window after other objects rendered
    timeText = FONT.render(f"Time: {round(elapsedTime)}s",1,"white")    
    hitsText = FONT.render(f"Hits: {hits} / {HIT_THRESHOLD}",1,"white")
    WIN.blit(timeText,(10,10))    
    WIN.blit(hitsText,(WIDTH - 130,10))
    
    # backup - player as rectangle
    # pygame.draw.rect(WIN,"red",player) # render player before projectiles, so projectiles overlap player
    
    # player with image as avatar
    catImg = pygame.image.load('assets/catsmall.png')
    catImg.convert()
    catImg = pygame.transform.scale(catImg, (PLAYER_WIDTH, PLAYER_HEIGHT)) 
    catRect = catImg.get_rect()
    catRect.center = PLAYER_WIDTH/2, PLAYER_HEIGHT/2
    WIN.blit(catImg, player)
    # pygame.draw.rect(WIN, "red", player, 1)
    
    
    for projectile in projectiles:
        pygame.draw.rect(WIN,"blue",projectile)
    
    if checkGameOver(hits):
        gameOverMessage()
    
    pygame.display.update() # not sure if should use .flip here instead
    

def main():
    run = True
    
    player = pygame.Rect(200,HEIGHT - PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    startTime = time.time()
    elapsedTime = 0
    
    projectileAddIncrement = 2000 # 2000 miliseconds (2s) before first projectile falls
    projectileCount = 0

    projectiles = []
    treats = []
    
    # TODO: when hit = true, spit out a message
    hit = False
    # TODO: when hit counter reaches threshold, stop game and write game over to window with time elapsed, etc
    hits = 0
        
    while run:
        
        projectileCount += clock.tick(FPS) # number of miliseconds since last clock tick
        
        clock.tick(FPS) # keeps framing consistent across all hardware/computers
        elapsedTime = time.time() - startTime
        
        if projectileCount > projectileAddIncrement:
            for _ in range(PROJECTILE_RELEASE):
                projectileX = random.randint(0,WIDTH - PROJECTILE_WIDTH)
                projectile = pygame.Rect(projectileX,-PROJECTILE_HEIGHT,PROJECTILE_WIDTH,PROJECTILE_HEIGHT) # negative top so projectile starts just above top of screen and gives impression of falling from sky
                projectiles.append(projectile)
                
            # minimum increment = 200 so no faster than that, but reduce time between projectiles appearing by 100ms each iteration (gets faster and faster)
            projectileAddIncrement = max(200,projectileAddIncrement - 100) 
            projectileCount = 0
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL <= WIDTH - PLAYER_WIDTH:
            player.x += PLAYER_VEL
            
        # TODO: utilise all movement keys as well
        
        # if keys[pygame.K_UP]:
        #     player.y -= PLAYER_VEL
        # if keys[pygame.K_DOWN]:
        #     player.y += PLAYER_VEL
        
        for projectile in projectiles[:]: # dont modify existing list, just get copy of it
            projectile.y += PROJECTILE_VEL
            if projectile.y > HEIGHT:
                projectiles.remove(projectile)
            elif projectile.y + projectile.height >= player.y and projectile.colliderect(player):
                projectiles.remove(projectile)
                hit = True
                hits += 1
                break
            
        draw(player,elapsedTime,projectiles,hits)
        
    
    pygame.quit()
    
if __name__ == "__main__":
    main()