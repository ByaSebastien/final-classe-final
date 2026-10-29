"""Party : l'équipe a des héros, une bourse, un sac, des objets et des materias."""

from final_classe.characters.heroes import Hero
from final_classe.characters.monsters import Monster
from final_classe.items import Equipment, Materia, PhoenixDown, Potion, Usable


class Party:
    """L'équipe : le héros du joueur en premier, puis ses compagnons."""

    def __init__(self, heroes: list[Hero]) -> None:
        self.heroes = heroes
        self.gil = 0
        self.bag: list[Equipment] = []  # l'équipement qui n'est porté par personne
        self.materias: list[Materia] = []  # les materias qui ne sont montées nulle part
        self.items: list[Usable] = [Potion(), Potion(), Potion(), PhoenixDown()]

    @property
    def leader(self) -> Hero:
        """Le héros du joueur."""
        return self.heroes[0]

    @property
    def standing(self) -> list[Hero]:
        """Les héros encore debout."""
        return [hero for hero in self.heroes if hero.is_alive]

    @property
    def knocked_out(self) -> list[Hero]:
        """Les héros K.O."""
        return [hero for hero in self.heroes if not hero.is_alive]

    def reward(self, monsters: list[Monster]) -> list[Hero]:
        """L'XP aux héros debout, les gils (même ceux volés) dans la bourse.

        Renvoie les héros qui ont gagné au moins un niveau.
        """
        xp = sum(monster.xp for monster in monsters)
        self.gil += sum(monster.gil for monster in monsters)
        for hero in self.heroes:  # les gils volés par un héros rejoignent la bourse
            self.gil += hero.gil
            hero.gil = 0
            self.items.extend(hero.loot)  # et les objets volés, le sac
            hero.loot.clear()
        return [hero for hero in self.standing if hero.gain_xp(xp) > 0]

    def rest(self) -> None:
        """Entre deux combats, chaque héros se repose."""
        for hero in self.heroes:
            hero.rest()
