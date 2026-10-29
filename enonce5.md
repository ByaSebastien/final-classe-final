# Étape 05 : la sauvegarde

> **Chapitre** : 05, classmethod, JSON, exceptions et couches
> **Point de départ** : votre projet, dans l'état de la démo (`to_dict` et `from_dict` pour `Stats`, les materias, `Equipment` et `Hero`)
> **Durée** : le palier obligatoire en 1 h 30 environ, puis les bonus
> **Solution** (bonus compris) : [`solution/final-classe/`](solution/final-classe/)

Sephiroth est vaincu… mais il faut tout recommencer à chaque partie. À la fin de cette étape, la partie se sauvegarde après chaque zone, le menu de départ propose « Continuer », et une sauvegarde absente ou abîmée donne un message clair, jamais une trace d'erreur.

**Les règles du projet** :
- seul le package `storage/` touche au disque ;
- le domaine (`stats`, `items`, `characters`) se décrit avec `to_dict`, sans savoir où ira le dictionnaire ;
- le jeu n'attrape qu'une erreur de sauvegarde : `SaveError`.

---

## Le palier obligatoire

### 1. Le sac et l'équipe (≈ 20 min)

**Les objets** sont sauvés par leur nom. À la fin de `items/consumables.py`, un dictionnaire `ITEMS: dict[str, type[Usable]]`, du nom de chaque objet vers sa classe.

**`Inventory`** :
- `to_dict() -> dict[str, int]` : le nombre d'exemplaires de chaque objet, `{"Potion": 3, "Queue de phénix": 1}` ;
- `from_dict(data)`, une `@classmethod` : recrée chaque objet avec `ITEMS[name]()`, autant de fois qu'il le faut.

**`Party`** :
- `to_dict()` : `heroes`, `gil`, `bag`, `materias` et `items`, chacun traduit par son propre `to_dict` ;
- `from_dict(data)`, une `@classmethod` : `JOBS_BY_NAME[hero["job"]].from_dict(hero)` recrée chaque héros dans son job, puis l'équipe retrouve ses gils, son sac, ses materias (`materia_from_dict`) et ses objets.

Vérifiez l'aller-retour dans un `essai.py` : `Party.from_dict(party.to_dict()).to_dict() == party.to_dict()`.

### 2. Le fichier (≈ 20 min)

Un nouveau package, `storage/`, avec un module `save.py` :
- `SAVES = Path("sauvegardes")`, le dossier, et `SAVE = SAVES / "partie.json"`, le fichier ;
- `save_game(party, zone)` : écrit `{"zone": zone, "party": party.to_dict()}` en JSON (`indent=2`, `ensure_ascii=False`, `encoding="utf-8"`). Le dossier est créé s'il n'existe pas ;
- `load_game() -> tuple[Party, int]` : relit le fichier, et renvoie l'équipe et la zone où reprendre.

`storage/__init__.py` réexporte `save_game` et `load_game`. Ouvrez le fichier écrit dans PyCharm : il se lit comme un texte.

### 3. SaveError (≈ 15 min)

Dans `storage/errors.py`, une exception `SaveError`, fille d'`Exception`.

`load_game` transforme chaque problème en `SaveError`, avec `raise … from error` :

| Problème | L'erreur d'origine | Le message |
|---|---|---|
| Pas de fichier | `FileNotFoundError` | `Aucune sauvegarde.` |
| Le fichier n'est pas du JSON | `json.JSONDecodeError` | `La sauvegarde partie.json est abîmée.` |
| Une clé manque, un job inconnu… | `KeyError`, `ValueError`, `TypeError` | `La sauvegarde partie.json est incomplète.` |

Réexportez `SaveError` dans `storage/__init__.py`.

### 4. Les zones comme données (≈ 35 min)

Pour reprendre une partie, le jeu doit savoir **où** il en est. Les zones deviennent des données.

**Dans un nouveau module `game/zones.py`** :
- `Zone`, une dataclass gelée : `name: str`, `waves: Callable[[], list[list[Monster]]]` (une fonction qui crée des monstres neufs), et `before: Callable[[Party], None] | None = None` (ce qui précède la zone) ;
- une fonction par zone pour les vagues : `plains()`, `forest()`, `cave()`, `chaos()`, `crater()` ;
- une fonction par étape intermédiaire : `before_forest` (le marchand ambulant), `before_cave` (le coffre et la préparation), `before_chaos` (Cid, la préparation, Garland) et `before_crater` (Bahamut, les armes légendaires, Cid, la préparation, Sephiroth) ;
- `equip_starters`, `open_chest`, `first_shop`, `second_shop` et `give_signatures` déménagent d'`adventure.py` vers `zones.py` ;
- `ZONES: list[Zone]`, les cinq zones dans l'ordre.

**Dans `game/adventure.py`** :
- `new_game() -> Party` : le prologue, la création et le recrutement ;
- `start_game() -> tuple[Party, int]` : le menu `1. Nouvelle partie  2. Continuer`. Si le chargement lève une `SaveError`, le jeu affiche son message, et une nouvelle partie commence ;
- `run()` : une boucle sur `ZONES`, à partir de la zone où reprendre. Avant chaque zone, son `before` s'il y en a un ; après chaque zone traversée (sauf la dernière), `save_game(party, index + 1)`.

```text
1. Nouvelle partie  2. Continuer
> 2
Partie chargée : La Grotte des cristaux.
Un coffre ! Équipement, materias et objets rejoignent le sac.
```

### Vérification
- [ ] Après les Plaines, `sauvegardes/partie.json` existe, et se lit dans PyCharm.
- [ ] « Continuer » reprend à la zone suivante, avec les mêmes niveaux, le même équipement et les mêmes objets.
- [ ] Un fichier vidé, ou rempli de n'importe quoi, donne un message, puis une nouvelle partie.
- [ ] `grep -rn "write_text\|read_text" src/` ne trouve rien en dehors de `storage/`.

---

## Les bonus

Chaque bonus est indépendant. Faites-les dans l'ordre qui vous plaît.

### ★ 1. Le résumé de la sauvegarde
La sauvegarde garde sa date : `datetime.now().isoformat(sep=" ", timespec="minutes")`. Une fonction `peek()` lit le fichier sans recréer l'équipe. Avant le menu, le jeu affiche un résumé :
```text
Sauvegarde : 2026-10-25 14:32  La Grotte des cristaux  (Vaan niv. 6, Lulu niv. 6, Basch niv. 6)
```

### ★ 2. Trois emplacements
`partie-1.json` à `partie-3.json`, avec `slot_path(slot)`. Au départ, le jeu affiche les trois emplacements, chacun avec son résumé ou la raison de son absence, et le joueur en choisit un.

### ★★ 3. La version du format
Chaque sauvegarde porte `"version": 1`. Une sauvegarde d'une autre version est refusée : `La sauvegarde partie-1.json vient d'une autre version du jeu.`

### ★★ 4. Reprendre entre deux vagues
Après chaque vague gagnée, la partie est aussi sauvegardée, avec le numéro de la vague suivante (`"wave"`). « Continuer » reprend au milieu de la zone, sans refaire son `before`. Les PV et les PM n'ont pas besoin d'être sauvés : l'équipe se repose après chaque vague.

### ★★★ 5. À vous de jouer
Une sauvegarde de secours (`.bak`) avant d'écraser l'ancienne, un écran de fin avec le temps de jeu, un `__eq__` sur `Party` pour vérifier l'aller-retour… Toujours la même question : **dans quelle couche ce code doit-il vivre ?**
