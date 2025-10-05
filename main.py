class Duree:
    def __init__(self, heure, minute, seconde):
        # Normalisation des valeurs : conversion des secondes et minutes excédentaires
        total_secondes = seconde + minute * 60 + heure * 3600
        
        self.heure = total_secondes // 3600
        self.min = (total_secondes % 3600) // 60
        self.sec = total_secondes % 60
    
    def __repr__(self):
        return f'Duree({self.heure}, {self.min}, {self.sec})'
    
    def __gt__(self, autre_duree):
        # Comparaison en convertissant tout en secondes
        self_total = self.heure * 3600 + self.min * 60 + self.sec
        autre_total = autre_duree.heure * 3600 + autre_duree.min * 60 + autre_duree.sec
        return self_total > autre_total
    
    def __lt__(self, autre_duree):
        # Comparaison en convertissant tout en secondes
        self_total = self.heure * 3600 + self.min * 60 + self.sec
        autre_total = autre_duree.heure * 3600 + autre_duree.min * 60 + autre_duree.sec
        return self_total < autre_total
    
    def __eq__(self, autre_duree):
        # Comparaison en convertissant tout en secondes
        self_total = self.heure * 3600 + self.min * 60 + self.sec
        autre_total = autre_duree.heure * 3600 + autre_duree.min * 60 + autre_duree.sec
        return self_total == autre_total
    
    def __add__(self, d):
        """Crée une durée en sommant la durée appelante et la durée d"""
        total_secondes = (self.heure + d.heure) * 3600 + (self.min + d.min) * 60 + (self.sec + d.sec)
        nouvelle_heure = total_secondes // 3600
        nouvelle_minute = (total_secondes % 3600) // 60
        nouvelle_seconde = total_secondes % 60
        return Duree(nouvelle_heure, nouvelle_minute, nouvelle_seconde)
    
    @classmethod
    def duree(cls, duree_str, delimiter=':'):
        h, m, s = 0, 0, 0
        if delimiter in duree_str:
            duree_liste = duree_str.strip().split(delimiter)
            if len(duree_liste) == 3:
                h, m, s = duree_liste
            elif len(duree_liste) == 2:
                # Format mm:ss (minutes:secondes)
                m, s = duree_liste
                h = 0
            elif len(duree_liste) == 1:
                s = duree_liste[0]
                h, m = 0, 0
            
            # Vérification que tous les éléments sont des chiffres
            if str(h).isdigit() and str(m).isdigit() and str(s).isdigit():
                h, m, s = int(h), int(m), int(s)
            else:
                h, m, s = 0, 0, 0
        return cls(h, m, s)


class Titre:
    def __init__(self, annee, album, titre, duree):
        self.annee = annee
        self.album = album
        self.titre = titre
        self.duree = duree


def lecture(filename, delimiter=';'):
    """Lit le fichier texte contenant les titres au format csv et retourne une liste de Titre"""
    liste_de_titres = []
    try:
        with open(filename, 'r', encoding='utf-8') as datas:
            for line in datas:
                line = line.strip()
                if line:  # Ignorer les lignes vides
                    elements = line.split(delimiter)
                    if len(elements) >= 4:
                        annee, album, titre, duree_str = elements[:4]
                        duree_obj = Duree.duree(duree_str)
                        titre_obj = Titre(annee.strip(), album.strip(), titre.strip(), duree_obj)
                        liste_de_titres.append(titre_obj)
    except FileNotFoundError:
        print(f"Fichier {filename} non trouvé")
    return liste_de_titres


# Création de la constante PINK_FLOYD
PINK_FLOYD = lecture('pink_floyd_durees.csv')


class PlayList:
    def __init__(self, base, ids):
        self.base = base
        self.ids = set(ids)
    
    def titre(self, id_titre):
        """Prend un numéro de titre (un id) et renvoie le Titre correspondant de la playlist"""
        if id_titre in self.ids and 0 <= id_titre < len(self.base):
            return self.base[id_titre]
        return None
    
    def duree(self):
        """Renvoie la durée totale (sous la forme d'un objet Duree) de la playlist"""
        duree_totale = Duree(0, 0, 0)
        for id_titre in self.ids:
            if 0 <= id_titre < len(self.base):
                duree_totale = duree_totale + self.base[id_titre].duree
        return duree_totale
    
    def commun(self, playlist):
        """Prend une autre PlayList en paramètre et crée une troisième PlayList constituée des Titres communs"""
        ids_communs = self.ids.intersection(playlist.ids)
        return PlayList(self.base, ids_communs)
    
    def __str__(self):
        """Permet d'afficher une PlayList"""
        result = []
        # Trier les ids pour un affichage ordonné
        ids_tries = sorted(self.ids)
        for id_titre in ids_tries:
            if 0 <= id_titre < len(self.base):
                titre_obj = self.base[id_titre]
                duree_str = f"[{titre_obj.duree.min:02d}:{titre_obj.duree.sec:02d}]"
                if titre_obj.duree.heure > 0:
                    duree_str = f"[{titre_obj.duree.heure:02d}:{titre_obj.duree.min:02d}:{titre_obj.duree.sec:02d}]"
                else:
                    duree_str = f"[{titre_obj.duree.min:02d}:{titre_obj.duree.sec:02d}]"
                
                ligne = f"{id_titre:3d} {duree_str} {titre_obj.titre} ({titre_obj.album}, {titre_obj.annee})"
                result.append(ligne)
        return '\n'.join(result)


# IDs des trois amis
XUAN = {60, 45, 107, 10, 51, 5, 30, 83, 94, 22, 4, 136, 145, 52, 133, 125, 86, 31, 87, 118, 82, 32, 43, 3, 27, 97, 150, 79, 152, 114, 54, 53, 93, 80, 141, 18, 115, 105, 72, 142, 81, 149, 17, 104, 102, 39, 11, 36, 91, 147, 134, 84, 117, 15, 128, 89, 50, 113, 33, 61, 124, 23, 59, 40, 111, 26, 100, 112, 19, 135, 123, 44, 119, 62, 155, 78, 7, 110, 157, 98, 99, 34, 65, 58, 139, 77, 47, 46, 8, 88, 1, 49, 95, 16, 41}

BOB = {129, 134, 58, 65, 67, 0, 102, 140, 74, 34, 85, 73, 28, 40, 56, 101, 12, 25, 35, 68, 39, 55, 124, 37, 26, 49, 59, 146, 108, 36, 106, 21, 3, 117, 123, 143, 100, 64, 9, 22, 156, 76, 19, 4, 122, 79, 109, 62, 113, 142, 89, 152, 1, 128, 43, 81, 126, 94, 135, 118, 7, 136, 141, 93, 11, 114, 20, 95, 155, 53, 138, 42, 2, 78, 61, 10, 32, 132, 5, 110, 125, 72, 45, 111, 92, 88, 145, 121, 149, 150, 51, 41, 57, 69, 98, 63, 104, 47, 90, 48, 24, 120, 31, 130, 70}

INAYA = {57, 41, 29, 83, 72, 2, 38, 25, 132, 60, 14, 136, 140, 127, 152, 54, 13, 17, 16, 116, 119, 101, 133, 129, 95, 130, 18, 63, 15, 64, 156, 52, 39, 123, 10, 73, 157, 107, 7, 58, 103, 75, 154, 61, 86, 137, 87, 111, 12, 47, 24, 23, 8, 117, 35, 108, 150, 118, 44, 42, 26, 55, 3, 32, 30, 59, 97, 74, 67, 99, 69, 88, 135, 131, 46, 53, 128, 112, 145, 125, 82, 147, 71, 68, 93, 113, 36, 4, 141, 65, 40, 50, 20, 94, 19, 122, 56, 11, 49, 76, 34, 153, 79, 9, 0, 5, 28, 70, 138, 151, 110, 144, 77, 33, 22, 100, 90, 143, 155, 126}

# Création des playlists des trois amis
xuan = PlayList(PINK_FLOYD, XUAN)
bob = PlayList(PINK_FLOYD, BOB)
inaya = PlayList(PINK_FLOYD, INAYA)

# Playlist commune aux trois personnes
commune_trois = xuan.commun(bob).commun(inaya)

# Playlist des morceaux de Bob que ne possèdent pas ses deux amies
# Bob - (Xuan ∪ Inaya)
morceaux_xuan_inaya = XUAN.union(INAYA)
morceaux_bob_seul = BOB - morceaux_xuan_inaya
bob_seul = PlayList(PINK_FLOYD, morceaux_bob_seul)

# Fonctions utiles pour les tests et le quiz
def afficher_playlist(playlist, nom=""):
    """Affiche une playlist avec son nom"""
    if nom:
        print(f"\n=== {nom} ===")
    print(playlist)
    print(f"Durée totale: {playlist.duree()}")
    print(f"Nombre de titres: {len(playlist.ids)}")

def statistiques():
    """Affiche les statistiques des playlists"""
    print("=== STATISTIQUES ===")
    print(f"Total de titres dans la base: {len(PINK_FLOYD)}")
    print(f"Titres de Xuan: {len(xuan.ids)}")
    print(f"Titres de Bob: {len(bob.ids)}")
    print(f"Titres d'Inaya: {len(inaya.ids)}")
    print(f"Titres communs aux trois: {len(commune_trois.ids)}")
    print(f"Titres uniques à Bob: {len(bob_seul.ids)}")

# Tests pour vérifier le bon fonctionnement
if __name__ == "__main__":
    print("=== TESTS DUREE ===")
    d0 = Duree(5, 34, 12)
    d1 = Duree(0, 70, 60)
    print(f"d0 = {d0}")
    print(f"d1 = {d1}")
    print(f"d0 + d1 = {d0 + d1}")
    
    print(f"\nTest de création depuis string:")
    d2 = Duree.duree('6:19:20')
    d3 = Duree.duree('0:234:7665')
    print(f"Duree.duree('6:19:20') = {d2}")
    print(f"Duree.duree('0:234:7665') = {d3}")
    
    print(f"\n=== TESTS COMPARAISON ===")
    print(f"d0 > d1: {d0 > d1}")
    print(f"d0 < d1: {d0 < d1}")
    print(f"d0 == d1: {d0 == d1}")
    
    print(f"\n=== INFORMATIONS BASE PINK FLOYD ===")
    if PINK_FLOYD:
        print(f"Nombre de titres chargés: {len(PINK_FLOYD)}")
        print("Premier titre:", PINK_FLOYD[0].titre if PINK_FLOYD else "Aucun")
        print("Dernier titre:", PINK_FLOYD[-1].titre if PINK_FLOYD else "Aucun")
    else:
        print("Attention: le fichier pink_floyd_durees.csv n'a pas pu être chargé.")
        print("Assurez-vous que le fichier est présent dans le répertoire courant.")
    
    statistiques()
    
    # Exemple d'affichage d'une petite playlist
    if PINK_FLOYD:
        print(f"\n=== EXEMPLE PLAYLIST ===")
        small = PlayList(PINK_FLOYD, {0, 1, 2} if len(PINK_FLOYD) > 2 else {0})
        afficher_playlist(small, "Petite playlist d'exemple")


# Code pour répondre aux questions du quiz
# Colle ce code à la fin de ton script principal

print("=== RÉPONSES AUX QUESTIONS DU QUIZ ===\n")

# Q3. Que donne Duree(0, 23, 56) + Duree(1, 36, 32) ?
print("Q3. Duree(0, 23, 56) + Duree(1, 36, 32)")
resultat_q3 = Duree(0, 23, 56) + Duree(1, 36, 32)
print(f"Réponse Q3: {resultat_q3}")
print()

# Q4. Que vaut PINK_FLOYD[56].titre ?
print("Q4. PINK_FLOYD[56].titre")
if len(PINK_FLOYD) > 56:
    titre_56 = PINK_FLOYD[56].titre
    print(f"Réponse Q4: {titre_56}")
else:
    print("Erreur: Index 56 non disponible dans la base")
print()

# Q5. Quelle est la durée totale des titres de cette base ?
print("Q5. Durée totale des titres de la base")
# Créer une playlist avec tous les indices
tous_les_indices = set(range(len(PINK_FLOYD)))
playlist_complete = PlayList(PINK_FLOYD, tous_les_indices)
duree_totale = playlist_complete.duree()
print(f"Réponse Q5: {duree_totale}")
print()

# Q6. Combien de titres les trois ami-es ont en commun ?
print("Q6. Nombre de titres communs aux trois ami-es")
nb_communs = len(commune_trois.ids)
print(f"Réponse Q6: {nb_communs}")
print()

# Q7. De quel album est tiré le titre commun le plus long en durée ?
print("Q7. Album du titre commun le plus long")
if commune_trois.ids:
    titre_plus_long = None
    duree_max = Duree(0, 0, 0)
    
    for id_titre in commune_trois.ids:
        if 0 <= id_titre < len(PINK_FLOYD):
            titre_actuel = PINK_FLOYD[id_titre]
            if titre_actuel.duree > duree_max:
                duree_max = titre_actuel.duree
                titre_plus_long = titre_actuel
    
    if titre_plus_long:
        print(f"Titre le plus long: {titre_plus_long.titre}")
        print(f"Durée: {titre_plus_long.duree}")
        print(f"Réponse Q7: {titre_plus_long.album}")
    else:
        print("Aucun titre commun trouvé")
else:
    print("Aucun titre commun")
print()

# Q8. Bob possède 10 titres que ni Xuan, ni Inaya n'ont. Quelle année est la plus représentée ?
print("Q8. Année la plus représentée dans les titres uniques de Bob")
print(f"Titres uniques de Bob: {len(bob_seul.ids)}")

# Compter les années
compteur_annees = {}
for id_titre in bob_seul.ids:
    if 0 <= id_titre < len(PINK_FLOYD):
        annee = PINK_FLOYD[id_titre].annee
        compteur_annees[annee] = compteur_annees.get(annee, 0) + 1

if compteur_annees:
    # Trouver l'année la plus fréquente
    annee_max = max(compteur_annees, key=compteur_annees.get)
    print(f"Répartition par année: {compteur_annees}")
    print(f"Réponse Q8: {annee_max} (avec {compteur_annees[annee_max]} titres)")
    
    # Afficher les titres uniques de Bob pour vérification
    print(f"\nTitres uniques de Bob:")
    for id_titre in sorted(bob_seul.ids):
        if 0 <= id_titre < len(PINK_FLOYD):
            titre = PINK_FLOYD[id_titre]
            print(f"  {id_titre}: {titre.titre} ({titre.album}, {titre.annee})")
else:
    print("Aucun titre unique trouvé")

print("\n" + "="*50)
print("RÉSUMÉ DES RÉPONSES:")
print("="*50)
print(f"Q3: {resultat_q3}")
if len(PINK_FLOYD) > 56:
    print(f"Q4: {PINK_FLOYD[56].titre}")
print(f"Q5: {duree_totale}")
print(f"Q6: {nb_communs}")
if commune_trois.ids and titre_plus_long:
    print(f"Q7: {titre_plus_long.album}")
if compteur_annees:
    print(f"Q8: {annee_max}")