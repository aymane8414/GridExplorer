import pygame

GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Car:
    def __init__(self, cellule_size):
        self.cellule_size = cellule_size
        self.x, self.y = 0, 0
        self.sensors = [0, 0, 0, 0] #haut, droite, bas, gauche
        self.nb_visites = [[0 for _ in range(10)] for _ in range(10)] #matrice pour suivre les visites

    def update_sensors(self, obstacles, grid_size):
        """
        Mettre à jour les capteurs pour détecter les obstacles autour de la voiture
        """
        grid_width, grid_height = grid_size

        #haut
        self.sensors[0] = 1 if self.y - 1 < 0 or (self.x, self.y - 1) in obstacles else 0
        # droite
        self.sensors[1] = 1 if self.x + 1 >= grid_width or (self.x + 1, self.y) in obstacles else 0
        # bas
        self.sensors[2] = 1 if self.y + 1 >= grid_height or (self.x, self.y + 1) in obstacles else 0
        # gauche
        self.sensors[3] = 1 if self.x - 1 < 0 or (self.x - 1, self.y) in obstacles else 0

    def move(self, action, obstacles, cellule_size, score, grille_reward):
        """
        Déplacer la voiture selon une action et retourner la récompense, si c'est terminé et le score
        """
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][action]
        new_x, new_y = self.x + dx, self.y + dy

        # Vérifier les bords de la grille
        if new_x < 0 or new_y < 0 or new_x >= 10 or new_y >= 10:
            return -1000, True, score  # sortir de la grille

        # Vérifier les obstacles ou les cases bloquées
        if (new_x, new_y) in obstacles:
            return -100, True, score  # obstacle

        # Vérifier la case finale
        if (new_x, new_y) == (9, 9):
            self.x, self.y = new_x, new_y
            self.nb_visites[new_y][new_x] += 1
            return grille_reward[new_y][new_x], True, score  # Récompense pour la fin

        # Déplacement normal
        self.x, self.y = new_x, new_y
        reward = grille_reward[new_y][new_x]  # Récupérer le reward de la case
        self.nb_visites[new_y][new_x] += 1  # Compter la visite
        return reward, False, score  # Retourne le score mis à jour




    def get_state(self):
        return (self.x, self.y)

    def reset(self):
        self.x, self.y = 0, 0
        self.nb_visites = [[0 for _ in range(10)] for _ in range(10)]

    def draw(self, screen):
        """
        Dessiner la voiture et les capteurs
        """
        
        # Dessiner la voiture
        pygame.draw.rect(screen, GREEN, 
                        (self.x * self.cellule_size, 
                        self.y * self.cellule_size, 
                        self.cellule_size, 
                        self.cellule_size))

        # Dessiner les capteurs
        sensor_color_active = RED  # Rouge si actif
        sensor_color_inactive = (0, 255, 0)  # Vert si inactif
        sensor_length = self.cellule_size // 2 

        # Centre de la voiture
        cx = self.x * self.cellule_size + self.cellule_size // 2
        cy = self.y * self.cellule_size + self.cellule_size // 2

        # Capteur haut
        pygame.draw.line(screen, 
                        sensor_color_active if self.sensors[0] else sensor_color_inactive,
                        (cx, cy - self.cellule_size // 2),
                        (cx, cy - self.cellule_size // 2 - sensor_length), 2)

        # Capteur droite
        pygame.draw.line(screen, 
                        sensor_color_active if self.sensors[1] else sensor_color_inactive,
                        (cx + self.cellule_size // 2, cy),
                        (cx + self.cellule_size // 2 + sensor_length, cy), 2)

        # Capteur bas
        pygame.draw.line(screen, 
                        sensor_color_active if self.sensors[2] else sensor_color_inactive,
                        (cx, cy + self.cellule_size // 2),
                        (cx, cy + self.cellule_size // 2 + sensor_length), 2)

        # Capteur gauche
        pygame.draw.line(screen, 
                        sensor_color_active if self.sensors[3] else sensor_color_inactive,
                        (cx - self.cellule_size // 2, cy),
                        (cx - self.cellule_size // 2 - sensor_length, cy), 2)