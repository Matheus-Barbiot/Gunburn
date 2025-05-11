import bge
import json
from collections import OrderedDict

class Options(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ])

    def start(self, args):
        self.scene = bge.logic.getCurrentScene()
        
        pass
    
    def setFullscreen(self):
        if self.object['SetFull'] == True:
            obj = self.scene.objects.get('op_wideButton')
            bge.render.setFullScreen(obj['full']) # Modo janela
            
            self.object['SetFull'] = False
    
    def setMusic(self):
        print('mudar music')
        pass
    
    def setSounds(self):
        print('mudar sons')
        pass
        
    def update(self):
        self.setFullscreen()
          # retorna o diretório do .blend
          
        caminho = "Codes/options.json"

        with open(caminho, "r") as arquivo:
            options = json.load(arquivo)

        print(options)
        pass
