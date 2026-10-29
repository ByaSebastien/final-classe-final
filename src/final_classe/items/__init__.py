"""Les objets du jeu : ils ne dépendent d'aucun autre package de Final Classe."""

from final_classe.items.consumables import Elixir, Ether, PhoenixDown, Potion, Usable
from final_classe.items.equipment import Equipment
from final_classe.items.fighter import Fighter
from final_classe.items.kinds import Slot
from final_classe.items.materia import AttackMateria, HealMateria, Materia, SummonMateria

__all__ = [
    "AttackMateria",
    "Elixir",
    "Equipment",
    "Ether",
    "Fighter",
    "HealMateria",
    "Materia",
    "PhoenixDown",
    "Potion",
    "Slot",
    "SummonMateria",
    "Usable",
]
