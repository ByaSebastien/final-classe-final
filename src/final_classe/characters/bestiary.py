"""Le bestiaire : une classe par espèce."""

import random
from collections.abc import Sequence
from typing import override

from final_classe.characters.base import Character
from final_classe.characters.hit import Hit
from final_classe.characters.monsters import Monster


class Flan(Monster):
    """Sa gélatine encaisse les coups, mais craint la magie."""

    NAME = "Flan"
    HP = 450
    STRENGTH = 14
    DEFENSE = 18
    RESISTANCE = 4
    SPEED = 6
    XP = 60
    GIL = 50


class Wolf(Monster):
    """Il mord fort et vite, mais se protège mal."""

    NAME = "Loup"
    HP = 380
    STRENGTH = 16
    DEFENSE = 6
    RESISTANCE = 8
    SPEED = 14
    XP = 80
    GIL = 60


class Sephiroth(Monster):
    """Le souvenir de Nibelheim. Pour l'instant, hors d'atteinte."""

    NAME = "Sephiroth"
    HP = 30000
    MP = 999
    STRENGTH = 50
    MAGIC = 60
    DEFENSE = 99
    RESISTANCE = 99
    SPEED = 30


class Bomb(Monster):
    """Le Bombo : blessé, il explose sur un héros, et disparaît."""

    NAME = "Bombo"
    HP = 900
    STRENGTH = 28
    MAGIC = 28
    DEFENSE = 12
    RESISTANCE = 12
    SPEED = 9
    XP = 90
    GIL = 70

    @override
    def act(self, heroes: Sequence[Character]) -> list[Hit]:
        """Sous la moitié de ses PV, il explose : MAG × 20 sur un héros, et il tombe."""
        if self.hp_ratio >= 0.5:
            return super().act(heroes)
        target = random.choice([hero for hero in heroes if hero.is_alive])
        damage = self.strike(target, self.magic * 20)
        self._hp = 0
        return [Hit("Explosion", target, damage)]


class Ahriman(Monster):
    """L'Ahriman : un œil volant qui frappe à la magie."""

    NAME = "Ahriman"
    HP = 780
    STRENGTH = 10
    MAGIC = 30
    DEFENSE = 10
    RESISTANCE = 20
    SPEED = 12
    XP = 90
    GIL = 60

    @override
    def attack(self, target: Character) -> int:
        """Son attaque est magique : la MAG contre la RÉS."""
        return self.magic_attack(target, 10)


class Cactuar(Monster):
    """Le Pampa : deux attaques faibles, puis les 1000 épines."""

    NAME = "Pampa"
    HP = 675
    STRENGTH = 18
    DEFENSE = 26
    RESISTANCE = 26
    SPEED = 20
    XP = 160
    GIL = 150

    def __init__(self, name: str | None = None, **changes: int) -> None:
        super().__init__(name, **changes)
        self._turn = 0  # les tours joués : un sur trois, les 1000 épines

    @property
    @override
    def warning(self) -> str | None:
        """Le tour d'avant les 1000 épines, il se hérisse."""
        return f"{self.name} se hérisse…" if self._turn % 3 == 2 else None

    @override
    def act(self, heroes: Sequence[Character]) -> list[Hit]:
        """Un tour sur trois : exactement 1000 dégâts. Sinon, une attaque normale."""
        self._turn += 1
        if self._turn % 3 != 0:
            return super().act(heroes)
        target = random.choice([hero for hero in heroes if hero.is_alive])
        return [Hit("1000 épines", target, self.strike(target, 1000))]


class Malboro(Monster):
    """Le Morbol, boss de la Forêt de Macalania."""

    NAME = "Morbol"
    HP = 6600
    STRENGTH = 38
    MAGIC = 30
    DEFENSE = 18
    RESISTANCE = 14
    SPEED = 7
    XP = 600
    GIL = 500

    def __init__(self, name: str | None = None, **changes: int) -> None:
        super().__init__(name, **changes)
        self._turn = 0  # un tour sur trois, la Mauvaise haleine

    @property
    @override
    def warning(self) -> str | None:
        """Le tour d'avant, il prend une grande inspiration."""
        return f"{self.name} prend une grande inspiration…" if self._turn % 3 == 2 else None

    @override
    def act(self, heroes: Sequence[Character]) -> list[Hit]:
        """Un tour sur trois, la Mauvaise haleine sur toute l'équipe."""
        self._turn += 1
        if self._turn % 3 != 0:
            return super().act(heroes)
        standing = [hero for hero in heroes if hero.is_alive]
        return [Hit("Mauvaise haleine", hero, self.magic_attack(hero, 10)) for hero in standing]


class Tonberry(Monster):
    """Le Tonberry : lent, petit, et son couteau fait très mal."""

    NAME = "Tonberry"
    HP = 3630
    STRENGTH = 60
    MAGIC = 13
    DEFENSE = 26
    RESISTANCE = 20
    SPEED = 3
    XP = 240
    GIL = 200
    WEAKNESS = "feu"


class Golem(Monster):
    """Le Golem de cristal : une défense énorme. La magie, ou Brise-armure."""

    NAME = "Golem de cristal"
    HP = 3960
    STRENGTH = 44
    MAGIC = 8
    DEFENSE = 60
    RESISTANCE = 10
    SPEED = 5
    XP = 280
    GIL = 220
    WEAKNESS = "foudre"


class Behemoth(Monster):
    """Le Béhémoth, boss de la Grotte des cristaux."""

    NAME = "Béhémoth"
    HP = 17325
    STRENGTH = 52
    MAGIC = 39
    DEFENSE = 30
    RESISTANCE = 24
    SPEED = 12
    XP = 1200
    GIL = 1000
    WEAKNESS = "glace"
