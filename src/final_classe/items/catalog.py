"""Le catalogue : chaque fonction fabrique une pièce neuve."""

from final_classe.items.equipment import Equipment
from final_classe.items.kinds import Slot
from final_classe.items.materia import AttackMateria, HealMateria, Materia, SummonMateria
from final_classe.stats import Stats


def bronze_sword() -> Equipment:
    """Une épée simple."""
    return Equipment("Épée de bronze", Slot.WEAPON, 100, Stats(strength=4))


def rod() -> Equipment:
    """Le bâton des mages."""
    return Equipment("Bâton", Slot.WEAPON, 100, Stats(magic=4))


def leather_armor() -> Equipment:
    """Une armure légère."""
    return Equipment("Armure de cuir", Slot.ARMOR, 100, Stats(defense=4))


def chain_mail() -> Equipment:
    """Une armure plus lourde, qui protège aussi un peu de la magie."""
    return Equipment("Cotte de mailles", Slot.ARMOR, 300, Stats(defense=8, resistance=2))


def mythril_sword() -> Equipment:
    """Une épée solide, avec deux emplacements de materia."""
    return Equipment("Épée de mythril", Slot.WEAPON, 600, Stats(strength=8), slots=2)


def mythril_rod() -> Equipment:
    """Un bâton qui canalise la magie, avec deux emplacements."""
    return Equipment("Bâton de mythril", Slot.WEAPON, 600, Stats(magic=8), slots=2)


def mythril_armor() -> Equipment:
    """Une armure de mythril, avec un emplacement."""
    return Equipment("Armure de mythril", Slot.ARMOR, 600, Stats(defense=10, resistance=6), slots=1)


def ribbon() -> Equipment:
    """Le Ruban : l'accessoire légendaire."""
    return Equipment("Ruban", Slot.ACCESSORY, 2000, Stats(resistance=12, speed=2))


def fire() -> Materia:
    """Feu."""
    return AttackMateria("Feu", 8, 12, "feu")


def ice() -> Materia:
    """Glace."""
    return AttackMateria("Glace", 8, 12, "glace")


def thunder() -> Materia:
    """Foudre."""
    return AttackMateria("Foudre", 8, 12, "foudre")


def cure() -> Materia:
    """Soin."""
    return HealMateria("Soin", 10, 12)


def ifrit() -> Materia:
    """Ifrit : Flammes de l'enfer sur tous les ennemis."""
    return SummonMateria("Ifrit", 30, 20, "feu")


def shiva() -> Materia:
    """Shiva : Poussière de diamant sur tous les ennemis."""
    return SummonMateria("Shiva", 30, 20, "glace")


def ramuh() -> Materia:
    """Ramuh : Jugement divin sur tous les ennemis."""
    return SummonMateria("Ramuh", 30, 20, "foudre")
