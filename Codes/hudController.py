import bge
from collections import OrderedDict

class Hud(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ])

    def start(self, args):
        #controladores
        self.scene = bge.logic.getCurrentScene()
        pass
    
    def lifeCount(self):
        #Atualiza a life
        life = bge.logic.globalDict.get('playerLife')
        count = self.scene.objects.get('hud_lifeCount')
        lifebar = ''
        for i in range(0, life // 2):
            lifebar += 'I'
        
        count['Text'] = f'Life: {lifebar}'
        return
    
    def levelCount(self):
        #atualiza o level
        level = bge.logic.globalDict.get('playerLevel')
        count = self.scene.objects.get('hud_levelCount')
        
        count['Text'] = f'Level: {str(level)}'
        return
    
    def stageText(self):
        stage = bge.logic.globalDict.get('stage')
        spawn = self.scene.objects.get('hud_spawnStage')
        
        if spawn['newStage'] == True:
            text = self.scene.addObject('text_stage', spawn, 100)
            text['Text'] = f'stage {stage + 1}'
            spawn['newStage'] = False
    
    def gravityText(self):
        gravity = bge.logic.globalDict.get('gravity')
        text = self.scene.objects.get('hud_gravity')
        
        text['Text'] = f'Gravity: {gravity}'
        
    
    def update(self):
        self.lifeCount()
        self.levelCount()
        self.stageText()
        self.gravityText()
        pass
