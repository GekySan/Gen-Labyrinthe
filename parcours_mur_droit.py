import matplotlib.pyplot as plt
import random

# https://en.wikipedia.org/wiki/Maze-solving_algorithm#Hand_On_Wall_Rule

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

    def affichage(self, chemin=None):
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

      
        ax.plot([-0.5, 0.5], [self.tailleY-0.5, self.tailleY-0.5], 'g-')
        if chemin:
            for i in range(len(chemin)-1):
                x1, y1 = chemin[i]
                x2, y2 = chemin[i+1]
                ax.plot([x1-0.5, x2-0.5], [y1-0.5, y2-0.5], 'g-')
        ax.plot([self.tailleX-0.5, self.tailleX+0.5], [0.5, 0.5], 'g-')

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

    def parcours_main_droite(self):
        directions = ['S', 'O', 'N', 'E']

        direction_index = 3

        x, y = 1, self.tailleY
        chemin = [(x, y)]

        while (x, y) != (self.tailleX, 1):
            if self.peut_avancer(x, y, directions[(direction_index + 1) % 4]):
                direction_index = (direction_index + 1) % 4
                x, y = self.adjacent(x - 1, y - 1, directions[direction_index])
                x, y = x + 1, y + 1
            elif self.peut_avancer(x, y, directions[direction_index]):
                x, y = self.adjacent(x - 1, y - 1, directions[direction_index])
                x, y = x + 1, y + 1
            elif self.peut_avancer(x, y, directions[(direction_index - 1) % 4]):
                direction_index = (direction_index - 1) % 4
            else:
                direction_index = (direction_index + 2) % 4

            chemin.append((x, y))

        return chemin

    def peut_avancer(self, x, y, direction):
        if 0 < x <= self.tailleX and 0 < y <= self.tailleY:
            return not self.obtenir_etat_murs(x, y, direction)
        return False

labyrinthe_exemple = Labyrinthe(5, 8)
labyrinthe_exemple.generer_labyrinthe()
chemin_sortie = labyrinthe_exemple.parcours_main_droite()
print(chemin_sortie)
labyrinthe_exemple.affichage(chemin_sortie)