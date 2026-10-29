"""Les genres du jeu : des Enum, à la place des chaînes."""

from enum import Enum


class Slot(Enum):
    """L'emplacement d'une pièce d'équipement."""

    WEAPON = "arme"
    ARMOR = "armure"
    ACCESSORY = "accessoire"
