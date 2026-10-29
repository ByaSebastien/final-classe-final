"""Le déroulement de la partie."""

from final_classe.characters import (
    Ahriman,
    Behemoth,
    Bomb,
    Cactuar,
    Flan,
    Golem,
    Malboro,
    Monster,
    Party,
    Sephiroth,
    Soldier,
    Tonberry,
    Wolf,
)
from final_classe.game.battle import fight
from final_classe.game.creation import ask_name, create_hero
from final_classe.game.display import banner, console, hero_sheet
from final_classe.game.preparation import prepare
from final_classe.game.recruit import recruit
from final_classe.items import Elixir, Ether, PhoenixDown, catalog


def prologue() -> None:
    """Nibelheim, il y a cinq ans : un duel perdu d'avance."""
    console.print("[italic]Nibelheim, il y a cinq ans…[/]\n")
    # Cloud, cinq ans plus tôt : moins aguerri que la recrue qu'on rencontrera ensuite.
    cloud = Soldier("Cloud", strength=20, magic=12, defense=15, resistance=13)
    sephiroth = Sephiroth()
    while cloud.is_alive:
        damage = cloud.attack(sephiroth)
        console.print(f"Cloud frappe Sephiroth : [bold]{damage}[/] dégât(s).")
        damage = sephiroth.attack(cloud)
        console.print(f"Sephiroth frappe Cloud : [bold red]{damage}[/] dégâts.")
    console.print(f"\n{hero_sheet(cloud)}")
    console.print(f"Sephiroth : PV {sephiroth.hp}/{sephiroth.max_hp}")
    console.print("\nSephiroth : « Tu n'es qu'une marionnette. »")
    console.print("[italic]Un jour, tu reviendras. Et cette fois, tu seras prêt.[/]")


def reward(party: Party, monsters: list[Monster]) -> None:
    """Le butin : l'équipe s'en charge, le jeu l'affiche."""
    xp = sum(monster.xp for monster in monsters)
    gil = party.gil
    leveled = party.reward(monsters)
    console.print(
        f"Butin : [yellow]+{xp} XP[/] pour chaque héros debout, [yellow]+{party.gil - gil} gils[/]"
    )
    for hero in leveled:
        console.print(f"[bold yellow]{hero.name} passe au niveau {hero.level} ![/]")


def cross(zone: str, party: Party, waves: list[list[Monster]]) -> bool:
    """Traverse une zone, vague après vague ; renvoie False si l'équipe tombe."""
    console.print(f"\n[bold cyan]=== {zone} ===[/]")
    for monsters in waves:
        if not fight(party, monsters):
            console.print("[bold red]=== Game over ===[/]")
            return False
        reward(party, monsters)
        party.rest()
        console.print("L'équipe se repose : PV et PM au maximum.")
    console.print(f"\n[bold green]{zone} : traversée ![/]")
    return True


def equip_starters(party: Party) -> None:
    """Avant la Forêt : une arme et une armure pour chacun, selon sa meilleure statistique."""
    for hero in party.heroes:
        hero.equip(catalog.rod() if hero.magic > hero.strength else catalog.bronze_sword())
        hero.equip(catalog.leather_armor())
        console.print(hero_sheet(hero))


def open_chest(party: Party) -> None:
    """À l'entrée de la Grotte, un coffre : de l'équipement, des materias et des objets."""
    party.bag.extend([catalog.mythril_sword(), catalog.mythril_rod(), catalog.mythril_armor()])
    party.bag.append(catalog.ribbon())
    party.materias.extend([catalog.fire(), catalog.ice(), catalog.thunder(), catalog.cure()])
    party.materias.extend([catalog.ifrit(), catalog.shiva(), catalog.ramuh()])
    party.items.extend([Ether(), Ether(), PhoenixDown(), Elixir()])
    console.print("\n[bold yellow]Un coffre ! Équipement, materias et objets rejoignent le sac.[/]")


def run() -> None:
    """Le prologue, la création du héros, le recrutement, puis trois zones."""
    console.print(banner())
    prologue()
    console.print("\n[bold]Cinq ans plus tard…[/]")
    party = Party(recruit(create_hero(ask_name())))
    for hero in party.heroes:
        console.print(hero_sheet(hero))
    plains: list[list[Monster]] = [
        [Flan()],
        [Wolf("Loup A"), Wolf("Loup B")],
        [Flan(), Wolf("Loup alpha", hp=600, strength=20)],
    ]
    forest: list[list[Monster]] = [
        [Bomb(), Ahriman()],
        [Cactuar()],
        [Bomb("Bombo A"), Bomb("Bombo B"), Ahriman()],
        [Malboro()],
    ]
    if not cross("Les Plaines de Dalmasca", party, plains):
        return
    console.print("\nUn marchand ambulant vous offre de quoi vous équiper :")
    equip_starters(party)
    if not cross("La Forêt de Macalania", party, forest):
        return
    open_chest(party)
    prepare(party)
    cave: list[list[Monster]] = [
        [Tonberry()],
        [Golem(), Golem("Golem B")],
        [Tonberry(), Golem()],
        [Behemoth()],
    ]
    cross("La Grotte des cristaux", party, cave)
