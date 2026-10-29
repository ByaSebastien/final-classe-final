# Étape 03 : l'équipement, les materias et la Grotte des cristaux

> **Chapitre** : 03, composition, délégation et Protocol
> **Point de départ** : votre projet, dans l'état de la démo (`items/` et `Equipment`, l'arme et l'armure des héros, `Party`)
> **Durée** : le palier obligatoire en 1 h 30 environ, puis les bonus
> **Solution** (bonus compris) : [`solution/final-classe/`](solution/final-classe/)

La Forêt est derrière vous. À la fin de cette étape, l'équipe a un sac d'objets, des materias montées sur son équipement, et elle traverse la Grotte des cristaux jusqu'au Béhémoth.

**Les règles du projet** :
- `items/` n'importe rien d'autre du jeu, ni `characters/`, ni `game/` : c'est `characters/` qui importe `items/` ;
- `characters/` n'affiche rien ;
- jamais d'`isinstance` pour savoir si un objet est une potion ou une materia : chaque sorte a sa liste.

---

## Le palier obligatoire

Chaque étape se teste dans le jeu, sauf les materias : on ne peut les monter qu'à partir de l'étape 3. Pour l'étape 2, un `essai.py` suffit.

### 1. Les objets (≈ 30 min)

**Le contrat d'un combattant.** Un objet soigne un héros : il a besoin de sa méthode `heal`. Mais `items/` ne peut pas importer `Character` : ce serait un import circulaire. Dans un nouveau module `items/fighter.py`, écrivez le `Protocol` **`Fighter`** : ce dont un objet a besoin d'un combattant, et rien de plus.
- `heal(amount) -> int` ;
- `restore_mp(amount) -> int` ;
- `revive() -> int`.

**Dans `Character`** (`base.py`), les deux méthodes qui manquent :
- `restore_mp(amount) -> int` : rend des PM à un personnage debout, sans dépasser le maximum. Renvoie les PM rendus ;
- `revive() -> int` : relève un personnage K.O. avec la moitié de ses PV max. Renvoie les PV rendus, ou 0 s'il était debout.

**Les objets.** Dans `items/consumables.py`, le `Protocol` **`Usable`** : un attribut `name: str`, un attribut `TARGET: str`, et `use(target: Fighter) -> int`. Puis quatre classes, **sans aucune mère commune** :

| Classe | `name` | `TARGET` | `use(target)` |
|---|---|---|---|
| `Potion` | Potion | `"allié"` | Rend 400 PV |
| `Ether` | Éther | `"allié"` | Rend 60 PM |
| `PhoenixDown` | Queue de phénix | `"K.O."` | Relève l'allié K.O. |
| `Elixir` | Élixir | `"allié"` | Rend tous les PM, puis tous les PV ; renvoie les PV rendus |

Réexportez-les dans `items/__init__.py`, avec `Fighter` et `Usable`.

**Le sac de l'équipe.** Dans `Party`, l'attribut `items: list[Usable]`, qui commence avec trois Potions et une Queue de phénix, et la propriété `knocked_out` : les héros K.O. Dans `Hero`, les potions disparaissent : `potions`, `POTION_HEAL` et `drink_potion`.

**Le combat.** `hero_turn` devient trop long. Découpez-le : chaque action est une fonction `(hero, party, monsters) -> bool`, qui renvoie `True` si le héros a agi, et `False` pour revenir au menu.
- `attack_action`, `skill_action` et `item_action`, rangées dans un dictionnaire `ACTIONS` : `{1: attack_action, 2: skill_action, 3: item_action}` ;
- `hero_turn` affiche le menu, gère « Se défendre » (4), puis appelle `ACTIONS[choice](hero, party, monsters)` ;
- `targets_for(kind, party, monsters)` remplace `skill_targets` : `kind` vaut `"ennemis"`, `"allié"`, `"K.O."` (un allié K.O. à choisir, ou une liste vide s'il n'y en a pas), ou `"ennemi"` ;
- `choose_option(labels, prompt) -> int | None` : une liste numérotée, avec `0. Retour` ;
- `report_defeated(targets, monsters)` : annonce les monstres vaincus ;
- `fight` reçoit la `Party` : `fight(party, monsters)`.

```text
Vaan : 1. Attaquer  2. Omnislash (12 PM)  3. Objet  4. Se défendre
> 3
  1. Potion
  2. Potion
  3. Potion
  4. Queue de phénix
  0. Retour
Objet : 4
Vaan utilise Queue de phénix sur Lulu : +260.
```

### 2. Les materias (≈ 30 min)

**Les materias** (`items/materia.py`) forment une famille : une classe abstraite et ses filles.

| Classe | Détail |
|---|---|
| `Materia` (`ABC`) | `__init__(name, cost, power)` ; l'attribut de classe `TARGET = "ennemi"` ; `cast(caster, target) -> int`, **abstraite** |
| `AttackMateria(Materia)` | `cast` : `caster.magic_attack(target, self.power)` |
| `HealMateria(Materia)` | `TARGET = "allié"` ; `cast` : `target.heal(caster.magic * self.power)` |

`cast` reçoit des `Fighter` : ajoutez au `Protocol` la propriété `magic` et la méthode `magic_attack(target, power)`.

**Une pièce d'équipement a des materias.** Dans `Equipment`, un paramètre `slots=0` (le nombre d'emplacements), une liste `materias`, et `attach(materia) -> bool` : `False` si tous les emplacements sont pris.

**Le catalogue** (`items/catalog.py`) :

| Fonction | Ce qu'elle fabrique |
|---|---|
| `mythril_sword()` | Épée de mythril : arme, 600 gils, FOR +8, 2 emplacements |
| `mythril_rod()` | Bâton de mythril : arme, 600 gils, MAG +8, 2 emplacements |
| `mythril_armor()` | Armure de mythril : armure, 600 gils, DÉF +10, RÉS +6, 1 emplacement |
| `fire()`, `ice()`, `thunder()` | Feu, Glace, Foudre : `AttackMateria`, 8 PM, puissance 12 |
| `cure()` | Soin : `HealMateria`, 10 PM, puissance 12 |

**Le héros délègue.** Dans `Hero` :
- la propriété `spells -> list[Materia]` : les materias montées sur **toutes** ses pièces. L'appelant n'a pas à savoir d'où viennent les sorts ;
- `can_cast(materia) -> bool` : la materia est dans ses sorts, et il a assez de PM ;
- `cast(materia, *targets) -> int` : paie les PM une fois, puis laisse la materia lancer le sort sur chaque cible. C'est la méthode modèle du jour 2.

**Le combat.** Une fonction `magic_action` : le joueur choisit un sort, puis sa cible. Dans `ACTIONS`, elle prend le numéro 3, et l'objet passe au 4 :
```text
Lulu : 1. Attaquer  2. Feu (8 PM)  3. Magie  4. Objet  5. Se défendre
> 3
  1. Glace (8 PM)
  2. Foudre (8 PM)
  0. Retour
Sort : 1
Lulu lance Glace sur Morbol : 290 dégâts.
```

### 3. La préparation et le coffre (≈ 20 min)

`Party` reçoit `materias: list[Materia]` : les materias montées nulle part.

Dans un nouveau module `game/preparation.py` :
- `choose_hero(party) -> Hero` ;
- `equip_from_bag(party)` : le joueur choisit une pièce du sac, puis un héros. La pièce qu'elle remplace retourne dans le sac ;
- `attach_materia(party)` : une materia de la réserve, un héros, puis une de ses pièces. Si la pièce est pleine, la materia reste dans la réserve ;
- `prepare(party)` : le menu, jusqu'au départ.

```text
Préparation : 1. Équiper  2. Monter une materia  0. Partir
```

Dans `adventure.py`, `open_chest(party)` : au sortir de la Forêt, un coffre. L'épée, le bâton et l'armure de mythril vont dans le sac ; Feu, Glace, Foudre et Soin dans la réserve de materias ; deux Éthers, une Queue de phénix et un Élixir dans les objets. Dans `run()`, après la Forêt : le coffre, puis la préparation.

### 4. La Grotte des cristaux (≈ 10 min)

Dans `bestiary.py`, trois espèces :

| Classe | `NAME` | PV | FOR | MAG | DÉF | RÉS | VIT | XP | GIL |
|---|---|---|---|---|---|---|---|---|---|
| `Tonberry` | Tonberry | 3630 | 60 | 13 | 26 | 20 | 3 | 240 | 200 |
| `Golem` | Golem de cristal | 3960 | 44 | 8 | 60 | 10 | 5 | 280 | 220 |
| `Behemoth` | Béhémoth | 17325 | 52 | 39 | 30 | 24 | 12 | 1200 | 1000 |

Le Golem a une DÉF énorme : contre lui, la magie, ou Brise-armure.

Dans `run()`, après la préparation, la Grotte :

```python
cave: list[list[Monster]] = [
    [Tonberry()],
    [Golem(), Golem("Golem B")],
    [Tonberry(), Golem()],
    [Behemoth()],
]
```

### Vérification
- [ ] `grep -r "import" src/final_classe/items` ne trouve que des imports de `items/` et de la bibliothèque standard.
- [ ] Une Queue de phénix sur un héros debout ne fait rien ; sur un héros K.O., il se relève avec la moitié de ses PV.
- [ ] Une Épée de mythril ne prend que deux materias : la troisième reste dans la réserve.
- [ ] Un héros sans materia voit « Aucune materia équipée ! », et rejoue.

---

## Les bonus

Chaque bonus est indépendant. Faites-les dans l'ordre qui vous plaît.

### ★ 1. L'accessoire
Un troisième emplacement : `Hero.accessory`, pris en compte par `equipment` et `equip`. Le coffre contient le **Ruban** : accessoire, 2000 gils, RÉS +12, VIT +2.

### ★ 2. Le Vol rapporte une potion
Quand Djidane vole des gils, il trouve aussi une Potion. Un héros a une liste `loot`, et `Party.reward` la vide dans le sac de l'équipe. Le texte du Vol devient : `"{user} vole {value} gils à {target}, et une potion s'il en a trouvé."`

### ★★ 3. Les invocations
`SummonMateria`, une fille d'`AttackMateria`, avec `TARGET = "ennemis"` : le sort frappe **tous** les ennemis. Ifrit, Shiva et Ramuh (30 PM, puissance 20) rejoignent le coffre. Aucune ligne de `battle.py` ne devrait changer.

### ★★ 4. Les faiblesses élémentaires
- `AttackMateria` a un `element` : `"feu"`, `"glace"` ou `"foudre"`. Les invocations aussi : Ifrit le feu, Shiva la glace, Ramuh la foudre ;
- `magic_attack(target, power, element=None)` multiplie les dégâts par `target.damage_multiplier(element)` ;
- `Character.damage_multiplier` renvoie 1 ; `Monster` la redéfinit : 2 si l'élément est sa `WEAKNESS` ;
- le Tonberry craint le feu, le Golem la foudre, le Béhémoth la glace.

### ★★★ 5. Retirer une materia
`Equipment.detach(materia) -> bool`, et une option « 3. Retirer une materia » dans la préparation : la materia retourne dans la réserve. On peut ainsi la déplacer d'un héros à l'autre.

### ★★★ 6. À vous de jouer
Une materia de votre invention (Poison, Rapidité…), un objet (Antidote, Mégalixir…), une pièce à trois emplacements… Toujours la même question : **est-ce que ça « est un », ou est-ce que ça « a un » ?**
