# Étape 01 : le héros et ses premiers combats

> **Chapitre** : 01, classes et objets
> **Point de départ** : votre projet, dans l'état de la démo (`Hero`, la fiche en couleurs, le prologue)
> **Durée** : le palier obligatoire en 1 h 30 environ, puis les bonus
> **Solution** (bonus compris) : [`solution/final-classe/`](solution/final-classe/)

Cinq ans après Nibelheim, un nouveau héros se lève. À la fin de cette étape, le joueur crée son héros, répartit ses points, et affronte un Flan au tour par tour : l'épée ou le sort Feu.

**La règle du projet** : `characters/` n'affiche rien et ne lit pas le clavier. Tout l'affichage et toutes les questions au joueur vivent dans `game/`.

---

## Le palier obligatoire

### 1. La classe Monster (≈ 15 min)

Dans `characters/monster.py`, écrivez la classe `Monster`, sur le modèle de `Hero`. Un monstre a **les mêmes statistiques** qu'un héros.

| Élément | Nom | Détail |
|---|---|---|
| `__init__` | `(name, hp, mp, strength, magic, defense, resistance)` | `ValueError` si les PV ou une statistique valent moins de 1 (les PM peuvent valoir 0) |
| Attributs | `name`, `strength`, `magic`, `defense`, `resistance`, `max_hp`, `max_mp` | Publics |
| Attributs | `_hp`, `_mp` | Les PV et les PM actuels, au maximum au départ |
| Propriétés | `hp`, `mp` | En lecture seule |
| Propriétés | `is_alive`, `hp_ratio` | Comme pour le héros |
| Méthode | `attack(target: Hero) -> int` | `FOR × 10 − DÉF de la cible × 5`, au minimum 1 et au maximum 9999 ; renvoie les PV perdus par la cible |
| Méthode | `take_damage(amount) -> int` | Comme pour le héros |

Réexportez `Monster` dans `characters/__init__.py`.

`Hero.attack` doit maintenant viser un héros **ou** un monstre : annotez `target: Hero | Monster`.

> 💡 `monster.py` importe `Hero`. `hero.py` ne peut donc pas importer `Monster` à son tour : les deux modules s'importeraient l'un l'autre. On importe `Monster` **pour l'éditeur seulement** :
> ```python
> from typing import TYPE_CHECKING
>
> if TYPE_CHECKING:  # pour l'éditeur seulement : monster.py importe déjà hero.py
>     from final_classe.characters.monster import Monster
> ```
> Au jour 2, une classe mère commune nous en débarrassera.

### 2. Le sort Feu (≈ 15 min)

Dans `Hero` :
- l'attribut de classe `FIRE_COST = 8` ;
- la propriété `can_cast_fire` : vrai s'il reste assez de PM ;
- la méthode `cast_fire(target) -> int` : elle retire 8 PM, inflige `MAG × 12 − RÉS de la cible × 5` (au minimum 1, au maximum 9999), et renvoie les PV perdus par la cible. S'il ne reste pas assez de PM, elle ne fait rien et renvoie 0.

### 3. La création du héros (≈ 25 min)

Dans un nouveau module `game/creation.py` :
- `ask_int(prompt, low, high) -> int` : redemande tant que la réponse n'est pas un nombre entre `low` et `high` ;
- `ask_name() -> str` : redemande tant que le nom est vide, et le renvoie avec une majuscule (`"vaan"` donne `"Vaan"`) ;
- `create_hero(name) -> Hero` : chaque statistique part à 10. Le joueur répartit **20 points** : il choisit les points de FOR, puis de MAG, puis de DÉF, sans dépasser ce qui reste. La RÉS reçoit le reste.

```text
Nom de votre héros : vaan
Chaque statistique vaut 10. Répartissez 20 points.
FOR (+0 à +20) : 5
MAG (+0 à +15) : 5
DÉF (+0 à +10) : 5
RÉS reçoit les 5 points restants.
```

### 4. Le combat contre un Flan (≈ 35 min)

- Dans `game/display.py`, ajoutez `monster_line(monster) -> str` : le nom du monstre et sa jauge de PV.
- Dans un nouveau module `game/battle.py`, écrivez `fight(hero, monster) -> bool`. Chaque tour :
  1. la fiche du héros et la ligne du monstre ;
  2. le menu `1. Attaquer  2. Feu (8 PM)` ;
  3. l'action du héros. Feu sans assez de PM affiche `Pas assez de PM !` et redemande, sans perdre le tour ;
  4. si le monstre est encore debout, il riposte.

  Le combat s'arrête quand l'un des deux tombe. `fight` renvoie `True` si le héros gagne.
- Dans `game/adventure.py`, la fonction `flan()` crée le Flan : **450 PV, 0 PM, FOR 14, MAG 1, DÉF 18, RÉS 4**. `run()` affiche l'écran titre et le prologue, crée le héros, puis lance le combat.

### Résultat attendu

```text
Combat : Vaan contre Flan

--- Tour 1 ---
Vaan
  PV  600/600  ██████████
  PM   60/60   ██████████
  FOR 15  MAG 15  DÉF 15  RÉS 15
Flan     PV  450/450  ██████████
1. Attaquer  2. Feu (8 PM)
> 2
Vaan lance Feu sur Flan : 160 dégâts.
Flan attaque Vaan : 65 dégâts.
…
--- Tour 3 ---
…
> 2
Vaan lance Feu sur Flan : 130 dégâts.
Flan est vaincu !

Victoire !
L'aventure peut commencer !
```

### Vérification
- [ ] `Monster("Flan", hp=450, mp=0, strength=0, magic=1, defense=18, resistance=4)` lève une `ValueError`.
- [ ] À l'épée, le Flan perd 60 PV par coup (avec 15 en FOR) : sa DÉF le protège. Avec Feu, il en perd 160.
- [ ] Après 7 Feu, il reste 4 PM : le 8e affiche `Pas assez de PM !`.
- [ ] `characters/` n'importe pas `rich`.

---

## Les bonus

Chaque bonus est indépendant. Faites-les dans l'ordre qui vous plaît.

### ★ 1. Les potions
- `Hero.POTION_HEAL = 200`, et l'attribut `potions` : 3 au départ.
- `drink_potion() -> int` : retire une potion et rend 200 PV (sans dépasser le maximum). Renvoie les PV rendus, ou 0 s'il n'y a plus de potion.
- Le menu devient `1. Attaquer  2. Feu (8 PM)  3. Potion (x3)`. Sans potion : `Plus de potion !`, et le joueur rejoue.

### ★ 2. Le bilan du combat
À la fin de chaque combat, `fight` affiche le nombre de tours, les dégâts infligés et les dégâts reçus :
```text
Bilan : 3 tours, 450 dégâts infligés, 130 dégâts reçus.
```

### ★★ 3. L'XP, les niveaux et les gils
- `Hero` gagne `level` (1), `xp` (0) et `gil` (0), et la propriété `xp_to_next` : `level × 100`.
- `gain_xp(amount) -> int` ajoute l'XP. Tant qu'elle atteint `xp_to_next`, le héros monte d'un niveau : +60 PV max, +2 dans chaque statistique. Renvoie le nombre de niveaux gagnés.
- `Monster` reçoit deux paramètres de plus, avec une valeur par défaut : `xp=0` et `gil=0`. Le Flan rapporte 30 XP et 50 gils.
- Après une victoire, `reward(hero, monsters)` affiche le butin et la montée de niveau :
```text
Butin : +80 XP, +120 gils
Vaan passe au niveau 2 !
```

### ★★ 4. Les Plaines de Dalmasca
- Une fonction `wolf()` : le Loup, **380 PV, 0 PM, FOR 16, MAG 1, DÉF 6, RÉS 8**, 40 XP, 60 gils. Il mord fort, mais se protège mal : l'épée lui convient.
- `run()` enchaîne trois combats : un Flan, un Loup, puis un Flan.
- Entre deux combats, le héros se repose : la méthode `rest()` lui rend tous ses PV et ses PM.
- À la fin : `Les Plaines de Dalmasca sont traversées !`

### ★★★ 5. Plusieurs monstres à la fois
- `fight(hero, monsters)` reçoit une **liste** de monstres. Chaque monstre debout riposte.
- `choose_target(monsters) -> Monster` : s'il reste plusieurs monstres debout, le joueur choisit sa cible.
```text
  1. Loup A   PV  380/380  ██████████
  2. Loup B   PV  380/380  ██████████
Cible : 2
Vaan lance Feu sur Loup B : 140 dégâts.
```
- Les Plaines deviennent trois vagues : `[Flan]`, `[Loup A, Loup B]`, puis `[Flan, Loup]`.

### ★★★ 6. À vous de jouer
Un sort Glace, une fuite, un coup critique, un monstre de votre invention… Toujours la même règle : la logique dans `characters/`, l'affichage dans `game/`.
