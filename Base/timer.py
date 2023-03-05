'''Une classe pour attendre un certain temps avant d'executer une fonction'''


class Timer:
    '''Constructeur de la classe Timer qui prend en parametre la duree du timer et la fonction a executer'''

    def __init__(self, duration: float, callbacks: list[callable], autoStart: bool = True):
        self.duration: float = duration
        self.advancement: float = 0.0
        self.timePassed: float = 0.0
        self.timeLeft: float = duration
        self.callbacks: list[callable] = callbacks
        self.running: bool = autoStart

    def Reset(self):
        self.timePassed = 0.0
        self.timeLeft = self.duration
        self.advancement = 0.0
        self.running = False

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
        self.timePassed += deltaTime
        self.timeLeft -= deltaTime
        self.advancement = self.timePassed / self.duration
        if self.advancement >= 1.0:
            for callback in self.callbacks:
                callback()
            self.Stop()
