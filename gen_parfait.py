import matplotlib.pyplot as plt
import random

# https://fr.wikipedia.org/wiki/Mod%C3%A9lisation_math%C3%A9matique_d%27un_labyrinthe#Fusion_al%C3%A9atoire_de_chemins

class Cellule:
    def __init__(self):
        self.murs = {'N': True, 'E': True, 'S': True, 'O': True}

class Labyrinthe:
    def __init__(self, tailleX, tailleY):
        self.tailleX = tailleX
        self.tailleY = tailleY
        self.cellules = [[Cellule() for _ in range(tailleY)] for _ in range(tailleX)]

    def obtenir_etat_murs(self, x, y, direction=None):
        if x > 0 and y > 0:
            if direction is None:
                return self.cellules[x-1][y-1].murs
            else:
                return self.cellules[x-1][y-1].murs.get(direction, True)

    def modifier_etat_murs(self, x, y, etat, direction=None):
        if x > 0 and y > 0:
            if direction is None:
                for dir in self.cellules[x-1][y-1].murs:
                    self.cellules[x-1][y-1].murs[dir] = etat
            else:
                if direction in self.cellules[x-1][y-1].murs:
                    self.cellules[x-1][y-1].murs[direction] = etat

    def enlever_murs(self, x, y, direction=None):
        self.modifier_etat_murs(x, y, False, direction)

        if direction == 'N' and y < self.tailleY:
            self.modifier_etat_murs(x, y+1, False, 'S')
        elif direction == 'S' and y > 0:
            self.modifier_etat_murs(x, y-1, False, 'N')
        elif direction == 'E' and x < self.tailleX:
            self.modifier_etat_murs(x+1, y, False, 'O')
        elif direction == 'O' and x > 0:
            self.modifier_etat_murs(x-1, y, False, 'E')

    def affichage(self):
        fig, ax = plt.subplots(figsize=(self.tailleX, self.tailleY))
        ax.set_xlim(-1, self.tailleX + 1)
        ax.set_ylim(-1, self.tailleY + 1)
        ax.set_aspect('equal')

        self.enlever_murs(1, self.tailleY, 'O')
        self.enlever_murs(self.tailleX, 1, 'E')

        for x in range(self.tailleX):
            for y in range(self.tailleY):
                cellule = self.cellules[x][y]

                if cellule.murs['N']:
                    ax.plot([x, x + 1], [y + 1, y + 1], 'r-')
                if cellule.murs['S']:
                    ax.plot([x, x + 1], [y, y], 'r-')
                if cellule.murs['E']:
                    ax.plot([x + 1, x + 1], [y, y + 1], 'r-')
                if cellule.murs['O']:
                    ax.plot([x, x], [y, y + 1], 'r-')

        ax.plot([-.5, self.tailleX], [self.tailleY, self.tailleY], 'b-')
        ax.plot([-.5, 0], [self.tailleY-1, self.tailleY-1], 'b-')
        ax.plot([0, 0], [self.tailleY-1, 0], 'b-')
        ax.plot([0, self.tailleX+.5], [0, 0], 'b-')
        ax.plot([self.tailleX, self.tailleX+.5], [1, 1], 'b-')
        ax.plot([self.tailleX, self.tailleX], [1, self.tailleY], 'b-')

        plt.show()

    def initialiser_zones(self):
        zone_id = 0
       
        for x in range(self.tailleX): 
            for y in range(self.tailleY):
                self.cellules[x][y].zone = zone_id
                zone_id += 1

    def fusionner_zones(self, zone1, zone2):
        for x in range(self.tailleX):
            for y in range(self.tailleY):
                if self.cellules[x][y].zone == zone2:
                    self.cellules[x][y].zone = zone1

    def choisir_mur_a_enlever(self):
        while True:
            x, y = random.randint(0, self.tailleX - 1), random.randint(0, self.tailleY - 1)
            directions = ['N', 'E', 'S', 'O']
            random.shuffle(directions)
            for direction in directions:
                nx, ny = self.adjacent(x, y, direction)
                if 0 <= nx < self.tailleX and 0 <= ny < self.tailleY and self.cellules[x][y].zone != self.cellules[nx][ny].zone:
                    return x, y, direction

    def adjacent(self, x, y, direction):
        if direction == 'N':
            return x, y + 1
        elif direction == 'E':
            return x + 1, y
        elif direction == 'S':
            return x, y - 1
        elif direction == 'O':
            return x - 1, y

    def verifier_zones_uniques(self):
        zone_initiale = self.cellules[0][0].zone
        for x in range(self.tailleX):
            for y in range(self.tailleY):
                if self.cellules[x][y].zone != zone_initiale:
                    return False
        return True

    def generer_labyrinthe(self):
        self.initialiser_zones()
        while not self.verifier_zones_uniques():
            x, y, direction = self.choisir_mur_a_enlever()
            self.enlever_murs(x + 1, y + 1, direction)
            nx, ny = self.adjacent(x, y, direction)
            self.fusionner_zones(self.cellules[x][y].zone, self.cellules[nx][ny].zone)

labyrinthe_exemple = Labyrinthe(5, 8)
labyrinthe_exemple.generer_labyrinthe()
labyrinthe_exemple.affichage()