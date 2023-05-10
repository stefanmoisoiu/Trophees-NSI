class Timer:
    """Une classe pour attendre un certain temps avant d'executer une fonction"""

    def __init__(self, duration: float, callbacks: list[callable], autoStart: bool = True):
        """Constructeur de la classe Timer qui prend en parametre la duree du timer et la fonction a executer"""

        self.duration: float = duration
        self.advancement: float = 0.0
        self.timePassed: float = 0.0
        self.timeLeft: float = duration
        self.callbacks: list[callable] = callbacks
        self.running: bool = autoStart

    def Reset(self):
        """Fonction qui reset le timer"""
        self.timePassed = 0.0
        self.timeLeft = self.duration
        self.advancement = 0.0
        self.running = False

    def Start(self):
        """Fonction qui demarre le timer"""

        self.running = True

    def Stop(self):
        """Fonction qui arrete le timer"""

        self.running = False

    def Update(self, deltaTime: float):
        """Fonction qui met a jour le timer"""

        if not self.running:
            return
        self.timePassed += deltaTime
        self.timeLeft -= deltaTime
        self.advancement = self.timePassed / self.duration
        if self.advancement >= 1.0:
            for callback in self.callbacks:
                callback()
            self.Stop()
