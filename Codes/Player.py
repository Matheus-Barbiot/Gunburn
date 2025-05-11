import bge
from mathutils import Vector, Matrix
from collections import OrderedDict

DEBUG = False
MAX_LIFE_PLAYER = 50
DEMAGE_PLAYER = 2
ADD_LIFE = 3
ADD_JUMP = 1
ADD_SPEED = 0.005

class Player(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ])

    def start(self, args):
        #controladores e variaveis
        self.scene = bge.logic.getCurrentScene()
        self.character = bge.constraints.getCharacter(self.object)
        self.keyboard = bge.logic.keyboard.inputs
        self.mouse = bge.logic.mouse.inputs
        self.object.collisionCallbacks.append(self.collisions)
        
        self.fireDelay = [0.3, 0.2, 0.3, 0.15]
        self.object['life'] = MAX_LIFE_PLAYER
        
        #objetos:
        self.obj_camera = self.object.children.get('cam_player')
        self.obj_gun = None
        
        self.aimList = list()
        
        for object in self.obj_camera.children:
            #pega as miras do player:
            if 'aim' in object.name:
                self.aimList.append(object)
                
            #pega o objeto da arma do player:
            if 'gunMesh' in object.name:
                self.obj_gun = object
        
        print(f'Lista de miras: {self.aimList}')
        
        #inputs
        self.WKEY = self.keyboard[bge.events.WKEY]
        self.SKEY = self.keyboard[bge.events.SKEY]
        self.DKEY = self.keyboard[bge.events.DKEY]
        self.AKEY = self.keyboard[bge.events.AKEY]
        self.SPACEKEY = self.keyboard[bge.events.SPACEKEY]
        
        self.LEFT = self.mouse[bge.events.LEFTMOUSE]
        pass
    

    def movement(self):
        #define os movimentos padrões do player:
        y = self.WKEY.active - self.SKEY.active
        x = self.DKEY.active - self.AKEY.active
        direction = self.object.worldOrientation * Vector([x,y,0])
        
        self.character.walkDirection = direction.normalized() * self.object['velocity'] # direção X velocidade)
        
        #Atualiza propriedas do pulo conforme as propriedades do player
        self.character.fallSpeed = self.object['fallSpeed']
        self.character.maxJumps = self.object['maxJumps']
        self.character.jumpSpeed = self.object['jumpForce']
        #ativa o pulo
        if self.SPACEKEY.activated: self.character.jump()
        pass
    
    def shoot(self, n):
        #aplica o disparo da bala:
        if self.LEFT.active:
            if self.object['fireTime'] >= self.object["fireDelay"]: # fireTime é propriedade do tipo Timer
                for aim in range(0, n):
                    self.obj_gun.playAction('Gun', 0, 3, play_mode=0)
                    self.scene.addObject('obj_playerBullet', self.aimList[aim], 200)
                    fire = self.scene.addObject('obj_fireGun', self.aimList[0], 5)
                    self.object['fireTime'] = 0 #reinicia timer
    
    # Controla o nível da arma do player:
    def gun(self):
        level = self.object['gun level']
        
        if 1 <= level <= 6:
            shots = (level - 1) % 3 + 1
            delay = self.fireDelay[shots - 1] if level <= 3 else self.fireDelay[-1]
            self.object['fireDelay'] = delay
            self.shoot(shots)
        else:
            print(f'Erro: {self.object.name}["gun level"] não suportado.')

        if DEBUG:
            print(f'nivel atual: {self.object["gun level"]}')
            print(f'->  Delay da arma: {self.object["fireDelay"]}')
        
        # Nivel 1 - uma bala lenta    > Nivel 4 - uma bala rápida
        # Nivel 2 - duas balas lentas > Nivel 5 - duas balas rápidas
        # Nivel 3 - três balas lentas > Nivel 6 - três balas rápidas
    
    
    #Aplica as funções básicas do player
    def default(self):
        if self.object['life'] <= 0:
            bge.logic.endGame()
        
        if self.object['life'] > MAX_LIFE_PLAYER:
            self.object['life'] = MAX_LIFE_PLAYER
    
    #configura as colisões do player
    def collisions(self, obj, point, normal):
        if 'obj_enemyBullet'in obj.name:
            self.object['life'] -= DEMAGE_PLAYER
            self.object.sendMessage(to='hud_demage', subject='demage')
            self.object.sendMessage(to='cam_player', subject='demage')
            obj.endObject()
            return
        
        if 'obj_lifePowerUp' in obj.name:
            if self.object['life'] < MAX_LIFE_PLAYER:
                self.object['life'] += ADD_LIFE
                self.object.sendMessage(to='hud_spawnPowerUp', subject='lifePowerUp')
                obj.endObject()
                
        if 'obj_jumpPowerUp' in obj.name:
            self.object['jumpForce'] += ADD_JUMP
            self.object.sendMessage(to='hud_spawnPowerUp', subject='jumpPowerUp')
            obj.endObject()
                
        if 'obj_speedPowerUp' in obj.name:
            self.object['velocity'] += ADD_SPEED
            self.object.sendMessage(to='hud_spawnPowerUp', subject='speedPowerUp')
            obj.endObject()
            
            
    def update(self):
        self.movement()
        self.gun()
        self.default()
        pass
