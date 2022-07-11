import pygame
from pygame.locals import *
import random
from sys import exit
import os
pygame.init()
pygame.mixer.init()

altura_tela = 600
largura_tela = 1100
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('DINO-GAME')
diretorio_principal = os.path.dirname(__file__)
diretorio_sons =  os.path.join(diretorio_principal, 'sons')

#imagens
CORRE = [pygame.image.load(os.path.join("JOGODINO-GAME/imagens/dino", "DinoRun1.png")),
        pygame.image.load(os.path.join("JOGODINO-GAME/imagens/dino", "DinoRun2.png")),]

DINO_START = [pygame.image.load(os.path.join("JOGODINO-GAME/imagens/dino", "DinoStart.png"))]
DINO_MORTO = [pygame.image.load(os.path.join("JOGODINO-GAME/imagens/dino", "DinoDead.png"))]

'''CORRE = [pygame.image.load(os.path.join("JOGODINO-GAME/imagens/modazul", "dino.png"))]'''

PULA = pygame.image.load(os.path.join("JOGODINO-GAME/imagens/dino", "DinoJump.png"))

ABAIXA = [pygame.image.load(os.path.join("JOGODINO-GAME/imagens/dino", "DinoDuck1.png")),
         pygame.image.load(os.path.join("JOGODINO-GAME/imagens/dino", "DinoDuck2.png"))]

CACTU_PEQUENO = [pygame.image.load(os.path.join("JOGODINO-GAME/imagens/cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("JOGODINO-GAME/imagens/cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("JOGODINO-GAME/imagens/cactus", "SmallCactus3.png"))]

CACTU_GRANDE = [pygame.image.load(os.path.join("JOGODINO-GAME/imagens/cactus", "LargeCactus1.png")),
               pygame.image.load(os.path.join("JOGODINO-GAME/imagens/cactus", "LargeCactus2.png")),
               pygame.image.load(os.path.join("JOGODINO-GAME/imagens/cactus", "LargeCactus3.png"))]

PASSARO = [pygame.image.load(os.path.join("JOGODINO-GAME/imagens/passaro", "Bird1.png")),
          pygame.image.load(os.path.join("JOGODINO-GAME/imagens/passaro", "Bird2.png"))]

NUVENS = pygame.image.load(os.path.join("JOGODINO-GAME/imagens/outros", "Cloud.png"))
FUNDO = pygame.image.load(os.path.join("JOGODINO-GAME/imagens/outros", "Track.png"))
GAME_OVER = pygame.image.load(os.path.join("JOGODINO-GAME/imagens/outros", "gameover02.png"))
GAME_RESET = pygame.image.load(os.path.join("JOGODINO-GAME/imagens/outros", "Reset.png"))

#sons
som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav'))
som_colisao.set_volume(1)

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))
som_pontuacao.set_volume(1)


class Dinossauro:
    x_pos = 80
    y_pos = 310
    y_pos_abaixa = 340
    velo_pulo = 8.5

    def __init__(self):
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)
        
        self.abaixa_img = ABAIXA
        self.corre_img = CORRE
        self.pula_img = PULA

        self.dino_abaixa =  False
        self.dino_corre = True
        self.dino_pula = False

        self.index_passos = 0
        self.pulo_velo = self.velo_pulo #PS: O nome é bem parecido, mas não é o mesmo :(
        self.image = self.corre_img[0]
        self.dino_retan = self.image.get_rect()
        self.dino_retan.x = self.x_pos
        self.dino_retan.y = self.y_pos

    def atualiza(self, entrada_usu):
        if (self.dino_abaixa):
            self.abaixa()
        if (self.dino_corre):
            self.corre() 
        if (self.dino_pula):
            self.pula() 
            

        if (self.index_passos >= 10):
            self.index_passos = 0
        
        if entrada_usu[pygame.K_UP] and not self.dino_pula:
            self.dino_abaixa = False
            self.dino_corre = False
            self.dino_pula = True
            self.som_pulo.play()
                  
        elif (entrada_usu[pygame.K_SPACE] and not self.dino_pula):
            self.dino_abaixa = False
            self.dino_corre = False
            self.dino_pula = True
            self.som_pulo.play() 
             
        elif entrada_usu[pygame.K_DOWN] and not self.dino_pula:
            self.dino_abaixa = True
            self.dino_corre = False
            self.dino_pula = False

        elif not (self.dino_pula or entrada_usu[pygame.K_DOWN]):
            self.dino_abaixa = False
            self.dino_corre = True
            self.dino_pula = False
        
    def abaixa(self):
        self.image = self.abaixa_img[self.index_passos // 5]
        self.dino_retan = self.image.get_rect()
        self.dino_retan.x = self.x_pos
        self.dino_retan.y = self.y_pos_abaixa
        self.index_passos += 1

    def corre(self):
        self.image = self.corre_img[self.index_passos // 5]
        self.dino_retan = self.image.get_rect()
        self.dino_retan.x = self.x_pos
        self.dino_retan.y = self.y_pos
        self.index_passos += 1

    def pula(self):
        self.image = self.pula_img
        if (self.dino_pula):
            self.dino_retan.y -= self.pulo_velo * 4
            self.pulo_velo -= 0.8

        if (self.pulo_velo < -self.velo_pulo):
            self.dino_pula = False
            self.pulo_velo = self.velo_pulo

    def draw(self, tela):
        tela.blit(self.image, (self.dino_retan.x, self.dino_retan.y))

class Nuvem:
    def __init__(self):
        self.x = largura_tela + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = NUVENS
        self.whidth = self.image.get_width()
    
    def atualiza(self):
        self.x -= velocidade_jogo
        if (self.x < -self.whidth):
            self.x = largura_tela + random.randint(2500, 3000)
            self.y = random.randint(50, 1000)
    
    def draw(self, tela):
        tela.blit(self.image, (self.x, self.y))

class Obstaculo:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = largura_tela
    
    def atualiza(self):
        self.rect.x -= velocidade_jogo
        if (self.rect.x < -self.rect.width):
            obstaculos.pop()

    def draw(self, tela):
        tela.blit(self.image[self.type], self.rect)

class cactusPequenos(Obstaculo):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class cactusGrandes(Obstaculo):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Passaro(Obstaculo):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0
    
    def draw(self, tela):
        if (self.index >= 9):
            self.index = 0
        tela.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def main():
    global velocidade_jogo, x_pos_fundo, y_pos_fundo, pontos, obstaculos
    corrida = True
    tempo = pygame.time.Clock()
    jogador = Dinossauro()
    nuvem = Nuvem()
    velocidade_jogo = 14
    x_pos_fundo = 0
    y_pos_fundo = 380
    pontos = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstaculos = []
    cont_mortes = 0

    def placar():
        global pontos, velocidade_jogo
        pontos += 1
        if (pontos % 100 == 0):
            som_pontuacao.play()
            if velocidade_jogo >= 23:
                velocidade_jogo += 0
            else:
                velocidade_jogo += 1
        
        texto = font.render("Pontos: {}".format(str(pontos)), True, (0,0,0))
        texto_ret = texto.get_rect()
        texto_ret.center = (1000, 40) 
        tela.blit(texto, texto_ret)

    def fundoTela():
        global  x_pos_fundo, y_pos_fundo
        image_larg = FUNDO.get_width()
        tela.blit(FUNDO, (x_pos_fundo, y_pos_fundo))
        tela.blit(FUNDO, (image_larg + x_pos_fundo, y_pos_fundo))
        if(x_pos_fundo <= - image_larg):
            tela.blit(FUNDO, (image_larg + x_pos_fundo, y_pos_fundo))
            x_pos_fundo = 0
        x_pos_fundo -= velocidade_jogo

    while (corrida):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
                corrida = False

        tela.fill((247,247,247))
        entrada_usu = pygame.key.get_pressed()

        jogador.draw(tela)
        jogador.atualiza(entrada_usu)

        if (len(obstaculos) == 0):
            if (random.randint(0, 2) == 0):
                obstaculos.append(cactusPequenos(CACTU_PEQUENO))
            elif(random.randint(0, 2) == 1):
                 obstaculos.append(cactusGrandes(CACTU_GRANDE))
            elif(random.randint(0, 2) == 2):
                obstaculos.append(Passaro(PASSARO))

        for obstaculo in obstaculos:
            obstaculo.draw(tela)
            obstaculo.atualiza()
            if (jogador.dino_retan.colliderect(obstaculo.rect)):
                som_colisao.play()
                pygame.time.delay(1000)
                cont_mortes += 1
                menu(cont_mortes)

        fundoTela()

        nuvem.draw(tela)
        nuvem.atualiza()

        placar()

        tempo.tick(30)
        pygame.display.flip()


def menu(cont_mortes):
    global pontos
    corrida = True
    while (corrida):
        tela.fill((247,247,247))
        font = pygame.font.Font('freesansbold.ttf', 30)
        font_game_over = pygame.font.Font('freesansbold.ttf', 40)
        font_pontos = pygame.font.Font('freesansbold.ttf', 25)

        if (cont_mortes == 0):
            text = font.render("Pressione qualquer tecla para Iniciar!", True, (0,0,0))
            DINO_START[0]
        elif (cont_mortes > 0):
            
             text = font_game_over.render("G A M E   O V E R", True, (0,0,0))
             placar = font_pontos.render("Pontos: {}".format(str(pontos)), True, (0,0,0))
             placar_retan = placar.get_rect()
             placar_retan.center = (largura_tela // 2 + 140, altura_tela // 2 - 100)
             tela.blit(placar, placar_retan)
             #tela.blit(GAME_OVER, (largura_tela // 2 - 30, largura_tela // 2 - 350))
             DINO_START[0] = DINO_MORTO[0]
             
        
        texto_retan = text.get_rect()
        texto_retan.center = (largura_tela // 2, altura_tela // 2 + 40)
        tela.blit(text, texto_retan)
        tela.blit(DINO_START[0], (largura_tela // 2 - 30, largura_tela // 2 - 350))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
                corrida = False
            if evento.type == pygame.KEYDOWN:
                main()

menu(cont_mortes = 0)