import bge
from random import choice
from collections import OrderedDict

class Gravity(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ])

    def start(self, args):
        self.scene = bge.logic.getCurrentScene()
        self.gravityListName = ('inverse', 'normal', 'zero')
        self.object['gravity'] = 'normal'
        
        bge.logic.globalDict['gravity'] = self.object['gravity']
        pass
    
    def gravityNormal(self):
        for object in self.scene.objects:
            if object.get('fallSpeed') != None:
                if 'enemyDefault' in object.name: #inimigo que voa
                    object['fallSpeed'] = 0.0
                elif 'obj_player'in object.name:
                    object['fallSpeed'] = 55
                    object['maxJumps'] = 1
                else:
                    object['fallSpeed'] = 55
                    
    def gravityZero(self):
        for object in self.scene.objects:
            if 'enemyDefault' in object.name:
                object['fallSpeed'] = 0
            if object.get('fallSpeed') != None:
                object['fallSpeed'] = 1
            if 'obj_player'in object.name:
                object['maxJumps'] = 100
    
    def gravityInverse(self):
        for object in self.scene.objects:
            if object.get('fallSpeed') != None:
                object['fallSpeed'] = 0
                object.applyMovement([0,0, 0.03], False)
            if 'obj_player'in object.name:
                object['maxJumps'] = 100
        
        
    def setGravity(self):
        # a cada 10 segundos a gravidade irá mudar:
        if self.object['gravityTemp'] > 10:
            gravity = choice(self.gravityListName) #escolhe uma gravidade aleatória
            self.object['gravity'] = gravity
            
            #aplica as funções que mudam apenas as props e não precisam ser chamadas a cada quadro
            if self.object['gravity'] == 'normal':
                self.gravityNormal()
                
            elif self.object['gravity'] == 'zero':
                self.gravityZero()
            
            bge.logic.globalDict['gravity'] = self.object['gravity']
            self.object['gravityTemp'] = 0
        
        
    def update(self):
        if bge.logic.globalDict.get('stage') != None:
            self.setGravity()
            
            if self.object['gravity'] == 'inverse':
                self.gravityInverse() #função que tem que ser atualizada constatimente para que o applymovement funcione
        else:
            self.object['gravityTemp'] = 0
        pass
