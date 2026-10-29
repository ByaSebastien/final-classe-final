"""Equipment : une pièce d'équipement, ses bonus, et ses emplacements de materia."""

from dataclasses import dataclass, field

from final_classe.items.kinds import Slot
from final_classe.items.materia import Materia
from final_classe.stats import Stats


@dataclass
class Equipment:
    """Une arme, une armure… : un emplacement, un prix, des bonus, et des materias.

    @dataclass écrit __init__, __repr__ et __eq__ à partir des champs annotés.
    """

    name: str
    slot: Slot
    price: int
    stats: Stats = field(default_factory=Stats)  # les bonus ; aucun par défaut
    slots: int = 0  # le nombre d'emplacements de materia
    materias: list[Materia] = field(default_factory=list)  # une liste neuve par pièce

    def attach(self, materia: Materia) -> bool:
        """Monte une materia ; renvoie False s'il n'y a plus d'emplacement libre."""
        if len(self.materias) >= self.slots:
            return False
        self.materias.append(materia)
        return True

    def detach(self, materia: Materia) -> bool:
        """Retire une materia ; renvoie False si elle n'est pas montée ici."""
        if materia not in self.materias:
            return False
        self.materias.remove(materia)
        return True
