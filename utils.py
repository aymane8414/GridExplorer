import pygame
import numpy as np
import random
import pickle
import os
import matplotlib.pyplot as plt
import io

BLACK = (0, 0, 0)
RED = (255, 0, 0)

def generate_random_obstacles(num_obstacles, width, height, cellule_size):
    """
    Crée un ensemble d'obstacles aléatoires sur la carte, sans bloquer le point de départ et l'arrivée
    """
    obstacles = set()
    while len(obstacles) < num_obstacles:
        x = random.randint(0, width // cellule_size - 1)
        y = random.randint(0, height // cellule_size - 1)
        if (x, y) != (0, 0) and (x, y) != (width // cellule_size - 1, height // cellule_size - 1):
            obstacles.add((x, y))
    return obstacles

def draw_grid(screen, cellule_size):
    """
    Dessine la grille sur l'écran
    """
    for x in range(0, screen.get_width(), cellule_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, screen.get_height()))
    for y in range(0, screen.get_height(), cellule_size):
        pygame.draw.line(screen, BLACK, (0, y), (screen.get_width(), y))

def draw_obstacles(screen, obstacles, cellule_size):
    """
    Dessine les obstacles sur la grille en rouge

    """
    for (x, y) in obstacles:
        color = (255, 255, 255) if (x, y) in [(0, 8), (0, 9), (1, 8), (1, 9), (2, 8), (2, 9)] else RED
        pygame.draw.rect(screen, color, (x * cellule_size, y * cellule_size, cellule_size, cellule_size))



def draw_text(surface, text, size, color, x, y):
    """
    Dessine texte à l'emplacement donné sur la carte
    """
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))



def generate_map_image_with_curve(car, obstacles, scores, grille_reward, file_name="map_with_curve.png"):
    """
    Crée une image combinant une carte avec obstacles et une courbe des scores
    """
    pygame.init()

    # Dimensions de la carte
    map_width, height = 500, 500
    cellule_size = map_width // 10
    curve_width = 500 
    total_width = map_width + curve_width

    # Créer une surface pour dessiner
    screen = pygame.Surface((total_width, height), pygame.SRCALPHA)
    screen.fill((255, 255, 255, 255))  # Fond blanc opaque

    # Dessiner la grille
    for x in range(0, map_width, cellule_size):
        pygame.draw.line(screen, (0, 0, 0, 255), (x, 0), (x, height))
    for y in range(0, height, cellule_size):
        pygame.draw.line(screen, (0, 0, 0, 255), (0, y), (map_width, y))

    # Liste des cases à exclure pour l'affichage des scores
    excluded_cells = [(0, 8), (0, 9), (1, 8), (1, 9), (2, 8), (2, 9)]

    # Dessiner les cases selon leur état
    font = pygame.font.Font(None, 24)  # Police par défaut, taille 24
    for y in range(10):
        for x in range(10):
            # Case départ
            if (x, y) == (0, 0):
                pygame.draw.rect(screen, (0, 0, 255, 100), (x * cellule_size, y * cellule_size, cellule_size, cellule_size))
            # Case visitée 
            elif car.nb_visites[y][x] > 0:
                # Créer une surface transparente temporaire
                temp_surface = pygame.Surface((cellule_size, cellule_size), pygame.SRCALPHA)
                temp_surface.fill((0, 0, 255, 50))  # Opacité réduite
                screen.blit(temp_surface, (x * cellule_size, y * cellule_size))
            # Obstacles
            elif (x, y) in obstacles:
                pygame.draw.rect(screen, (255, 0, 0, 255), (x * cellule_size, y * cellule_size, cellule_size, cellule_size)) 
            # Case normale ou finale
            elif (x, y) == (9, 9):  # Case finale
                pygame.draw.rect(screen, (0, 255, 0, 255), (x * cellule_size, y * cellule_size, cellule_size, cellule_size))

            # Dessiner le texte des rewards sauf pour les cases exclues
            if (x, y) not in excluded_cells:
                value = grille_reward[y][x]
                value_text = f"{value:.2f}"
                text_surface = font.render(value_text, True, (0, 0, 0))  # Texte noir
                text_x = x * cellule_size + cellule_size // 4
                text_y = y * cellule_size + cellule_size // 4
                screen.blit(text_surface, (text_x, text_y))

    # Générer la courbe des scores
    fig, ax = plt.subplots(figsize=(6.5, 5)) 

    # Lissage des scores (optionnel)
    smoothed_scores = np.convolve(scores, np.ones(10) / 10, mode='valid')

    episodes = range(1, len(smoothed_scores) + 1)
    ax.plot(episodes, smoothed_scores, label="Score (lissé)", color="blue")
    ax.set_xlabel("Épisodes")
    ax.set_ylabel("Score")
    ax.set_title("Évolution du score par épisode")
    ax.legend()

    # Ajustement de l'échelle des axes
    y_min, y_max = min(scores), max(scores)
    margin = (y_max - y_min) * 0.1  # 10% de marge en haut et en bas
    ax.set_ylim(y_min - margin, y_max + margin)  # Ajouter une marge
    ax.set_xticks(range(0, len(scores) + 1, max(1, len(scores) // 10)))  # Espacement des ticks X
    ax.grid(True)

    plt.tight_layout()

    # Convertir la courbe matplotlib en surface pygame
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    curve_surface = pygame.image.load(buf)
    buf.close()

    # Dessiner la courbe sur la surface principale
    screen.blit(curve_surface, (map_width, 0))

    # Dessiner le texte en bas à gauche
    episode_text = f"Épisodes: {len(scores)}"
    best_score_text = f"Score: {max(scores):.2f}"
    text_surface_episode = font.render(episode_text, True, (0, 0, 0)) 
    text_surface_best_score = font.render(best_score_text, True, (0, 0, 0)) 

    # Texte en bas à gauche
    screen.blit(text_surface_episode, (10, height - 50)) 
    screen.blit(text_surface_best_score, (10, height - 30)) 

    # Sauvegarder l'image
    pygame.image.save(screen, file_name)
    print(f"Carte générée avec courbe : {file_name}")




def draw_grid(screen, cellule_size, grille_reward, obstacles):
    for x in range(0, screen.get_width(), cellule_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, screen.get_height()))
    for y in range(0, screen.get_height(), cellule_size):
        pygame.draw.line(screen, BLACK, (0, y), (screen.get_width(), y))

    font = pygame.font.Font(None, 20)
    for row in range(10):
        for col in range(10):
            if (col, row) in obstacles:
                continue  # Ne pas afficher les rewards sur les obstacles

            # Afficher les rewards dans les cases
            reward_text = font.render(f"{grille_reward[row][col]:.1f}", True, (0, 0, 255))
            screen.blit(
                reward_text,
                (col * cellule_size + cellule_size // 4, row * cellule_size + cellule_size // 4),
            )
