'''Une classe pour attendre un certain temps avant d'executer une fonction'''


class Timer:
    '''Constructeur de la classe Timer qui prend en parametre la duree du timer et la fonction a executer'''

    def __init__(self, duration: float, callback: callable, autoStart: bool = True):
        self.duration: float = duration
        self.callback: callable = callback
        self.running: bool = autoStart

    '''Fonction qui demarre le timer'''

    def Start(self):
        self.running = True

    '''Fonction qui arrete le timer'''

    def Stop(self):
        self.running = False

    '''Fonction qui met a jour le timer'''

    def Update(self, deltaTime: float):
        if not self.running:
            return
        duration -= deltaTime
        if duration <= 0:
            self.callback()
            self.Stop()
