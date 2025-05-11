import bge
from random import choice, random, randint
from mathutils import Vector
from collections import OrderedDict

class Enemy(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ('type', {'Default', 'Rotary'}),
    ])

    def start(self, args):
        #controladores:
        self.scene = bge.logic.getCurrentScene()
        self.character = bge.constraints.getCharacter(self.object)
        
        #definindo posição inicial:
        pos = Vector((
            randint(-20, 20),
            randint(-20, 20),
            randint(1, 15)
        ))
        self.object.worldPosition = pos
        
        
        #objetos:
        self.aimList = []
        
        for obj in self.object.children:
            if "Aim" in obj.name:
                self.aimList.append(obj)
        
        #colisões
        self.object.collisionCallbacks.append(self.collisionBullet)
        
        #variaveis
        self.type = args['type']
        self.character.fallSpeed = self.object['fallSpeed']
        
        self.meshDefault = 'obj_enemy' + self.type
        self.meshHit = 'obj_enemy' + self.type + 'Hit'
        pass
    
    def chase(self, player, speed):
        #Funcão para o objeto seguir o player 
        if player:
            distance = self.object.getDistanceTo(player)
            direction = player.localPosition - self.object.localPosition
            if distance >= 5:
                self.object.applyMovement([0, speed, 0], True) # aplica movemento constante no eixo Y
            self.object.alignAxisToVect(direction, 1, 0.05) # faz ele sempre olhar para o player
    
    def rotate(self, player, speed):
        if player:
            self.object.applyRotation([0, 0, speed], True)
            
            
    def shoot(self, player):
        #aplica o disparo da bala caso o player esteja na distância e o :
        distance = self.object.getDistanceTo(player)
        
        if distance <= self.object['distance']:
            if self.object['fireTime'] >= self.object['fireDelay']:
                for aim in self.aimList:
                    self.scene.addObject('obj_enemyBullet', aim, 300)
                        
                self.object['fireTime'] = 0 #reinicia timer
                
    def dropPowerUp(self):
        chance = 0.5 # 50% de chance
        powerUpList = ['obj_lifePowerUp', 'obj_jumpPowerUp', 'obj_speedPowerUp']
        
        if random() < chance:
            powerUp = choice(powerUpList)
            self.scene.addObject(powerUp, self.object, 1000) #spawna o power up
        
        
            
    def collisionBullet(self, obj, point, normal):
        #Remove 1 da vida caso ele colida com a Bala do player e também muda sua malha
        if 'obj_playerBullet'in obj.name:
            self.object['life'] -= 1
            self.object['hitTemp'] = 0
            self.object.replaceMesh(self.meshHit, True, False)
            obj.endObject()
            return
    
                
    def default(self): #configurações padrão do inimigo:
        #atualiza a malha para o padrão
        if self.object['hitTemp'] > 0.05:
            self.object.replaceMesh(self.meshDefault, True, False)
            self.object['hitTemp'] = 0.5
        
        #caso a vida chegue a zero o inimigo morre
        if self.object['life'] <= 0:
            self.dropPowerUp()
            self.object.endObject()
            
            
    def update(self):
        #objetos: que mudam de posição
        self.player = self.scene.objects.get('obj_player')
        
        #funções:
        self.default()
        self.shoot(self.player)
        
        #tipos:
        if self.type == 'Default':
            self.chase(self.player, self.object['speed'])
        elif self.type == 'Rotary':
            self.rotate(self.player, self.object['speed'])
        
