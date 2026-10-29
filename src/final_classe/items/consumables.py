"""Les objets : aucune classe mère, mais tous respectent le même contrat, Usable."""

from typing import Protocol

from final_classe.items.fighter import Fighter


class Usable(Protocol):
    """Un objet qu'on utilise sur une cible."""

    name: str
    TARGET: str  # « allié », ou « K.O. » : un allié à terre

    def use(self, target: Fighter) -> int:
        """Utilise l'objet ; renvoie les PV ou les PM rendus."""
        ...


class Potion:
    """Rend 400 PV."""

    name = "Potion"
    TARGET = "allié"

    def use(self, target: Fighter) -> int:
        """Soigne la cible."""
        return target.heal(400)


class Ether:
    """Rend 60 PM."""

    name = "Éther"
    TARGET = "allié"

    def use(self, target: Fighter) -> int:
        """Rend des PM à la cible."""
        return target.restore_mp(60)


class PhoenixDown:
    """Relève un allié K.O., avec la moitié de ses PV."""

    name = "Queue de phénix"
    TARGET = "K.O."

    def use(self, target: Fighter) -> int:
        """Relève la cible."""
        return target.revive()


class Elixir:
    """Rend tous les PV et tous les PM."""

    name = "Élixir"
    TARGET = "allié"

    def use(self, target: Fighter) -> int:
        """Remet la cible au maximum ; renvoie les PV rendus."""
        target.restore_mp(9999)
        return target.heal(9999)
