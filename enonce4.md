# Étape 04 : l'inventaire, Cid et Sephiroth

> **Chapitre** : 04, méthodes spéciales, dataclasses et Enum
> **Point de départ** : votre projet, dans l'état de la démo (`Stats`, `Slot`, `hero.gear`, `Equipment` et `Hit` en dataclasses)
> **Durée** : le palier obligatoire en 1 h 30 environ, puis les bonus
> **Solution** (bonus compris) : [`solution/final-classe/`](solution/final-classe/)

La Grotte est derrière vous. À la fin de cette étape, plus aucune chaîne « magique » ne traîne dans le projet, le sac sait se compter, Cid ouvre sa boutique, et l'équipe affronte Garland dans le Sanctuaire du Chaos, puis **Sephiroth** dans le Cratère Nord.

**Les règles du projet** :
- `items/` n'importe ni `characters/`, ni `game/` ;
- une valeur qui ne peut prendre que quelques formes est une `Enum`, jamais une chaîne ;
- on ne touche pas à la liste interne d'un `Inventory` depuis l'extérieur : on passe par ses méthodes.

---

## Le palier obligatoire

### 1. Element et Target (≈ 20 min)

Dans `items/kinds.py`, à côté de `Slot`, deux `Enum` :

| Enum | Membres et valeurs |
|---|---|
| `Element` | `FIRE = "feu"`, `ICE = "glace"`, `THUNDER = "foudre"` |
| `Target` | `ENEMY = "un ennemi"`, `ENEMIES = "tous les ennemis"`, `ALLY = "un allié"`, `KNOCKED_OUT = "un allié K.O."` |

Réexportez-les dans `items/__init__.py`, puis remplacez **toutes** les chaînes :
- **`Element`** : l'élément d'`AttackMateria`, les materias du catalogue, `WEAKNESS` des monstres, `magic_attack` et `damage_multiplier` (dans `Character`, `Monster` et le `Protocol` `Fighter`) ;
- **`Target`** : `SKILL_TARGET` des héros (le Moine vise `Target.ALLY`, le Ninja `Target.ENEMIES`), `TARGET` des materias et des objets (et du `Protocol` `Usable`), et `targets_for` dans le combat.

On compare un membre avec `is` : `if kind is Target.ENEMIES:`.

### 2. L'inventaire (≈ 20 min)

Dans un nouveau module `items/inventory.py`, la classe `Inventory` :

| Élément | Détail |
|---|---|
| `__init__(*items)` | Range les objets dans une liste interne, `_items` |
| `add(*items)` | Ajoute un ou plusieurs objets |
| `take(name) -> Usable \| None` | Retire et renvoie le premier objet de ce nom, ou `None` |
| `counts() -> dict[str, int]` | Le nombre d'exemplaires de chaque objet : `{"Potion": 3, "Queue de phénix": 1}` |
| `__len__` | `len(sac)` : le nombre d'objets |
| `__iter__` | `for item in sac` : délègue à la liste interne |
| `__contains__(name)` | `"Potion" in sac` : vrai s'il en reste au moins un |

`Party.items` devient un `Inventory`. Partout où le code ajoutait ou retirait un objet de la liste (`reward`, `open_chest`, le combat), il passe par `add` et `take`.

Dans le combat, le menu des objets affiche une ligne par sorte d'objet :
```text
Lulu : 1. Attaquer  2. Feu (8 PM)  3. Magie  4. Objet  5. Se défendre
> 4
  1. Potion x3
  2. Queue de phénix x1
  0. Retour
```

Si personne n'a besoin de l'objet (une Queue de phénix sans allié K.O.), il retourne dans le sac.

### 3. La boutique de Cid (≈ 25 min)

**L'affichage d'une pièce.**
- Dans `Stats`, `bonus_text() -> str` : les seuls bonus non nuls, `"FOR +8, RÉS +6"`.
- Dans `Equipment`, `__str__` : `Épée de mythril (arme, FOR +8, 2 emplacements)`.
- Dans `Equipment`, `__lt__` : une pièce est « plus petite » qu'une autre si elle coûte moins cher.

**La boutique.** Dans un nouveau module `items/shop.py`, la classe `Shop` :
- `__init__(merchant, stock)` : le nom du marchand, et la liste des pièces à vendre ;
- la propriété `shelf` : l'étal, `sorted(self.stock)`.

**Le catalogue** s'enrichit des pièces de Cid :

| Fonction | Pièce |
|---|---|
| `diamond_sword()` | Épée de diamant : arme, 1500 gils, FOR +14, 2 emplacements |
| `diamond_rod()` | Bâton de diamant : arme, 1500 gils, MAG +14, 2 emplacements |
| `diamond_armor()` | Armure de diamant : armure, 1500 gils, DÉF +16, RÉS +10, 2 emplacements |
| `power_gauntlets()` | Gantelets de force : accessoire, 1000 gils, FOR +8 |
| `rune_bracelet()` | Bracelet runique : accessoire, 1000 gils, MAG +8 |
| `crystal_sword()` | Épée de cristal : arme, 4000 gils, FOR +22, 3 emplacements |
| `crystal_rod()` | Bâton de cristal : arme, 4000 gils, MAG +22, 3 emplacements |
| `crystal_armor()` | Armure de cristal : armure, 4000 gils, DÉF +24, RÉS +16, 2 emplacements |

**Acheter.** Dans `Party`, `buy(item) -> bool` : `False` s'il manque des gils ; sinon les gils sont payés, et la pièce rejoint le sac.

**Le menu.** Dans un nouveau module `game/shop.py` :
- `buy(shop, party)` : l'étal numéroté, avec les prix. La pièce achetée quitte l'étal ;
- `visit(shop, party)` : le menu, jusqu'au départ.

```text
Cid : « Approchez ! Du solide, et pas cher. »

Bourse : 3320 gils   1. Acheter  0. Partir
> 1
  1. Cotte de mailles (armure, DÉF +8, RÉS +2)  300 gils
  2. Gantelets de force (accessoire, FOR +8)  1000 gils
  3. Bracelet runique (accessoire, MAG +8)  1000 gils
  4. Épée de diamant (arme, FOR +14, 2 emplacements)  1500 gils
  …
```

Dans `adventure.py`, `first_shop() -> Shop` : deux Épées de diamant, un Bâton de diamant, trois Armures de diamant, les Gantelets, le Bracelet et une Cotte de mailles. Après la Grotte, l'équipe passe chez Cid, puis par la préparation.

### 4. Le Sanctuaire du Chaos et le Cratère Nord (≈ 25 min)

Dans `bestiary.py`, quatre espèces :

| Classe | `NAME` | PV | FOR | MAG | DÉF | RÉS | VIT | XP | GIL | Faiblesse | Particularité |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `Chimera` | Chimère | 4500 | 56 | 26 | 34 | 26 | 14 | 500 | 450 | glace | |
| `Lich` | Liche | 3900 | 17 | 42 | 30 | 40 | 11 | 500 | 450 | feu | Elle attaque à la magie : `magic_attack(target, 12)` |
| `Garland` | Garland | 19500 | 63 | 34 | 44 | 36 | 13 | 2400 | 3000 | aucune | Boss du Sanctuaire |
| `RedDragon` | Dragon rouge | 9000 | 66 | 42 | 46 | 30 | 15 | 1200 | 1000 | glace | Sous la moitié de ses PV, le **Souffle de feu** frappe toute l'équipe : `magic_attack(hero, 10)` |

**Sephiroth** change aussi. On le croise au prologue, et il doit y rester imbattable ; mais l'équipe du Cratère doit pouvoir le vaincre. Ses nouvelles stats : PV 30000, FOR 60, MAG 51, DÉF 45, RÉS 40, VIT 30, XP 0. Le Cloud du prologue ne lui fait toujours qu'un dégât par coup.

Dans `adventure.py` :
- `second_shop() -> Shop` : deux Épées de cristal, un Bâton de cristal, trois Armures de cristal ;
- `run()` : après la première visite chez Cid, le Sanctuaire du Chaos, puis la seconde visite, la préparation, et le Cratère Nord :

```python
chaos: list[list[Monster]] = [
    [Chimera()],
    [Lich(), Lich("Liche B")],
    [Chimera(), Lich()],
    [Garland()],
]
crater: list[list[Monster]] = [
    [RedDragon()],
    [Chimera(), RedDragon("Dragon rouge B")],
    [Sephiroth()],
]
```

Si l'équipe traverse le Cratère : `Sephiroth est vaincu. Le monde est sauvé !`

### Vérification
- [ ] `grep -rn '"feu"\|"allié"\|"ennemis"' src/` ne trouve plus que les valeurs des `Enum`.
- [ ] `len(party.items)` vaut 4 au départ, et `"Potion" in party.items` vaut `True`.
- [ ] L'étal de Cid est rangé du moins cher au plus cher.
- [ ] Un achat sans assez de gils est refusé, et la bourse ne change pas.

---

## Les bonus

Chaque bonus est indépendant. Faites-les dans l'ordre qui vous plaît.

### ★ 1. Vendre à Cid
`Party.sell(item) -> int` : la pièce quitte le sac, et l'équipe gagne la moitié de son prix. Dans le menu de Cid, une option `2. Vendre` ; Cid remet la pièce vendue sur son étal.

### ★ 2. Cid vend des objets
Chaque objet a un attribut de classe `PRICE` (Potion 50, Éther 150, Queue de phénix 300, Élixir 3000), et `Usable` l'exige. `Shop` reçoit un paramètre `goods: list[type[Usable]]` : des **classes** d'objets, comme `JOBS` au jour 2. Cid vend la Potion, l'Éther et la Queue de phénix, sans limite : chaque achat crée un objet neuf, `kind()`. Une option `3. Objets` dans le menu.

### ★★ 3. Bahamut
`bahamut()` dans le catalogue : une `SummonMateria` **sans élément**, 60 PM, puissance 30. Garland la laisse tomber quand il est vaincu : `Garland laisse tomber une materia rouge : Bahamut !`

### ★★ 4. Les armes légendaires
Au pied du Cratère, chaque héros reçoit l'arme légendaire de son job ; l'ancienne retourne dans le sac. Dans le catalogue, une fonction par arme, et un dictionnaire `SIGNATURES: dict[str, Callable[[], Equipment]]`, du nom du job vers la fonction :

| Job | Arme | Bonus | Emplacements |
|---|---|---|---|
| Soldat | Ultima Weapon | FOR +30 | 4 |
| Mage noir | Poupée Mog | MAG +30 | 4 |
| Chevalier | Excalibur | FOR +26, DÉF +10 | 3 |
| Moine | Griffes runiques | FOR +22, MAG +12 | 3 |
| Voleur | Dague d'Orichalque | FOR +24, VIT +6 | 3 |
| Samouraï | Masamune | FOR +32 | 3 |
| Archer | Arc Yoichi | FOR +28, VIT +2 | 3 |
| Ninja | Conformeur | FOR +24, VIT +4 | 3 |

### ★★★ 5. Le second souffle de Sephiroth
Sous la moitié de ses PV, Sephiroth change de rythme : un tour sur deux, il attaque, et annonce `Sephiroth déploie une aile noire…` ; l'autre tour, la **Supernova** frappe toute l'équipe (`magic_attack(hero, 14)`). Il lui faut un compteur de tours, et une redéfinition de `act` et de `warning`.

### ★★★ 6. À vous de jouer
Un `__str__` pour les materias, un `__lt__` pour trier le sac par prix, une `Enum` pour les zones, un boss caché après Sephiroth… Toujours la même question : **quelle méthode spéciale Python appelle-t-il ici ?**
