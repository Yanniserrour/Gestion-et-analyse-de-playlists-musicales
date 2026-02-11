# 🎸 Pink Floyd Data Manager 

## 📝 Présentation du Projet
Ce projet utilise la **Programmation Orientée Objet (POO)** pour gérer et analyser la discographie du groupe légendaire **Pink Floyd**. À partir d'un jeu de données CSV, nous structurons les morceaux en objets Python pour effectuer des calculs de durée complexes et gérer des playlists personnalisées.

---

## 🛠️ Architecture Technique

### 🏗️ Classes Principales
Le projet s'articule autour de trois classes interdépendantes :

1.  **`Duree`** : Gestion du temps (minutes/secondes).
    * Surcharge de l'opérateur `__add__` pour additionner des temps.
    * Méthode de classe pour convertir des formats bruts.
2.  **`Titre`** : Représentation d'un morceau (Nom, Album, Année, Objet Duree).
3.  **`PlayList`** : Conteneur dynamique pour manipuler des collections de titres.



### 📂 Traitement des Données
Le script automatise la lecture du fichier `pink_floyd_durees.csv` pour instancier les objets de la classe `Titre` de manière transparente.

---

## 🚀 Fonctionnalités Avancées

### Gestion des Playlists
Le projet simule des interactions entre différents utilisateurs (**Xuan**, **Bob** et **Inaya**) :
* **Intersection (`commun`)** : Identifier les titres partagés entre deux utilisateurs.
* **Playlists Exclusives** : Isoler les morceaux uniques à une collection.
* **Cumul de Durée** : Calcul automatique de la durée totale d'une playlist grâce à la logique de la classe `Duree`.

---

## 📊 Structure du Jeu de Données

| Champ | Type | Description |
| :--- | :--- | :--- |
| **Morceau** | `str` | Titre de la chanson |
| **Album** | `str` | Nom de l'album associé |
| **Année** | `int` | Année de sortie |
| **Durée** | `obj` | Instance de la classe `Duree` |

---

## 💻 Installation et Utilisation

### Prérequis
* **Python 3.8+**
* Le module natif `csv`

### Lancement
1. Placez le fichier `pink_floyd_durees.csv` dans le dossier racine.
2. Exécutez le script principal :
```bash
python pink_floyd_manager.py