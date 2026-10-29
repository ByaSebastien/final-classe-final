"""Les materias : une famille, donc une classe abstraite et des filles."""

from abc import ABC, abstractmethod
from typing import override

from final_classe.items.fighter import Fighter


class Materia(ABC):
    """Une materia, montée sur une pièce d'équipement : elle donne un sort."""

    TARGET = "ennemi"  # « ennemi », « allié », ou « ennemis » : tous les ennemis

    def __init__(self, name: str, cost: int, power: int) -> None:
        self.name = name
        self.cost = cost  # en PM
        self.power = power

    @abstractmethod
    def cast(self, caster: Fighter, target: Fighter) -> int:
        """Lance le sort sur une cible ; renvoie les dégâts ou les PV rendus."""


class AttackMateria(Materia):
    """Feu, Glace, Foudre : une attaque magique."""

    def __init__(self, name: str, cost: int, power: int, element: str | None = None) -> None:
        super().__init__(name, cost, power)
        self.element = element  # « feu », « glace » ou « foudre »

    @override
    def cast(self, caster: Fighter, target: Fighter) -> int:
        """Une attaque magique, avec la puissance de la materia."""
        return caster.magic_attack(target, self.power, self.element)


class HealMateria(Materia):
    """Soin : rend des PV à un allié."""

    TARGET = "allié"

    @override
    def cast(self, caster: Fighter, target: Fighter) -> int:
        """MAG × puissance PV rendus."""
        return target.heal(caster.magic * self.power)


class SummonMateria(AttackMateria):
    """Une invocation : une attaque magique sur tous les ennemis."""

    TARGET = "ennemis"
