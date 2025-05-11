import bge
from mathutils import Vector
from collections import OrderedDict

# Valor inicial do estágio para testes (debug)
STAGE_DEBUG = 1

class Spawner(bge.types.KX_PythonComponent):
    args = OrderedDict([
        # Nenhum argumento por enquanto, mas a estrutura está pronta
    ])

    def start(self, args):
        # Obtém a cena atual
        self.scene = bge.logic.getCurrentScene()

        # Define o estágio inicial a partir da constante de debug
        self.stage = STAGE_DEBUG

        # Define o estágio anterior (armazenado no objeto) como um antes do atual
        self.object['stage'] = STAGE_DEBUG - 1
        pass

    def createEnemy(self):
        # Só tenta criar inimigos se não houver nenhum atualmente
        if self.enemyCount() == 0:
            
            # Aguarda pelo menos 3 segundos com a variável 'temp'
            if self.object['temp'] >= 3:

                # Se o estágio atual ainda não foi iniciado
                if self.object['stage'] < self.stage:

                    # Se for um estágio múltiplo de 5 (ex: 5, 10, 15...)
                    if self.stage % 5 == 0:
                        cont = self.stage // 5  # Define quantos inimigos especiais devem ser criados
                        for n in range(0, cont):
                            rotaryEnemy = self.scene.addObject('obj_enemyRotary', self.object)
                            # Posição pode ser definida aqui se quiser personalizar

                    else:
                        # Em estágios normais, cria inimigos padrão conforme o número da fase
                        for n in range(0, self.stage):
                            newEnemy = self.scene.addObject('obj_enemyDefault', self.object)
                            # Posição também pode ser definida aqui

                    # Avança para o próximo estágio
                    self.object['stage'] += 1
                    self.stage += 1
                    return
            
            # Quando o tempo está quase em 1 segundo, envia sinal para HUD atualizar o estágio
            if 0.999 < self.object['temp'] < 1.0:
                bge.logic.globalDict['stage'] = self.object['stage']
                self.object.sendMessage(to='hud_spawnStage', subject='newStage')

        else:
            # Se ainda há inimigos vivos, reseta o tempo (para contar novamente)
            self.object['temp'] = 0

    def enemyCount(self):
        # Conta quantos inimigos padrão ainda estão vivos na cena
        enemyList = []
        names = ['obj_enemyDefault', 'obj_enemyRotary']
        for obj in self.scene.objects:
            if obj.name in names:
                enemyList.append(obj)

        return len(enemyList)

    def update(self):
        # Atualiza constantemente chamando o sistema de spawn
        self.createEnemy()
        pass
