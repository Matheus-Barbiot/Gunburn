import bge
from collections import OrderedDict

class Controller(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ])

    def start(self, args):
        self.scene = bge.logic.getCurrentScene()
        self.player = self.scene.objects.get('obj_player')
        pass
    
    def toBullets(self):
        enemyBulletSpeed = self.object['bulletsSpeed']
        playerBulletSpeed = self.object['playerBullets']
        
        for bullet in self.scene.objects:
            if 'enemyBullet' in  bullet.name:
                direction = [0, enemyBulletSpeed, 0]
                bullet.applyMovement(direction, True)
                if bullet.getDistanceTo(self.scene.objects.get('obj_player')) > 25:
                    bullet.endObject()
                
            if 'playerBullet' in bullet.name:
                direction = [0, playerBulletSpeed, 0]
                bullet.applyMovement(direction, True)
    
    def globalDict(self):
        bge.logic.globalDict['playerLife'] = self.player['life']
        bge.logic.globalDict['playerLevel'] = self.player['gun level']
        
    def update(self):
        self.toBullets()
        self.globalDict()
        pass
