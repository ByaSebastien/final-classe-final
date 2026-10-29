"""Stats : les cinq statistiques, rangées ensemble.

Ni personnage ni objet : items/ et characters/ s'en servent tous les deux. Ce module
n'importe rien du jeu, il ne peut donc pas créer d'import circulaire.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Stats:
    """FOR, MAG, DÉF, RÉS et VIT. Gelée : on ne la modifie pas, on en crée une autre."""

    strength: int = 0
    magic: int = 0
    defense: int = 0
    resistance: int = 0
    speed: int = 0

    def __add__(self, other: Stats) -> Stats:
        """Additionne champ à champ : la base, plus le bonus d'une pièce."""
        return Stats(
            self.strength + other.strength,
            self.magic + other.magic,
            self.defense + other.defense,
            self.resistance + other.resistance,
            self.speed + other.speed,
        )

    def __str__(self) -> str:
        """La ligne de la fiche : FOR 25  MAG 21  DÉF 25  RÉS 21  VIT 12."""
        return (
            f"FOR {self.strength}  MAG {self.magic}  DÉF {self.defense}  "
            f"RÉS {self.resistance}  VIT {self.speed}"
        )
