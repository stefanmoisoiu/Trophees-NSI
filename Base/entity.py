from Base.animation import AnimationManager
from Combat.ability import Ability
import Base.gridManager as gridManager

'''Classe qui permet de gérer les propriétés d'une entite'''


class EntityProperties:
    def __init__(self, name: str, description: str, abilities: list[Ability]) -> None:
        self.name = name
        self.description = description
        self.animationManager = AnimationManager()
        self.abilities = abilities


'''Classe qui permet de gérer une entite dans le jeu, ex: joueur, ennemi'''


class Entity:
    def __init__(self, properties: EntityProperties, position: tuple[int, int] = (0, 0)) -> None:
        self.properties = properties
        self.position = position
        self.attackShape: tuple[list[str],
                                tuple[int, int, int], tuple[int, int]] = None

    '''Affiche l'entite sur l'ecran'''

    def Display(self, screen) -> None:
        self.properties.animationManager.Display(
            screen, gridManager.GetWorldPosition(self.position))

    '''Met a jour l'entite, ex: animation, position, etc...'''

    def Update(self, deltaTime: float) -> None:
        self.properties.animationManager.Update(deltaTime)
