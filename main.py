import pygame
import os
from car import Car
from q_learning import *
from utils import *

pygame.init()

WIDTH, HEIGHT = 500, 500
CELL_SIZE = WIDTH // 10
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PROJET IA - Q Learning")


OBSTACLES = generate_random_obstacles(10, WIDTH, HEIGHT, CELL_SIZE)
OBSTACLES.update([(0, 8), (0, 9), (1, 8), (1, 9), (2, 8), (2, 9)])  #cases inexplorables 


def main():
    global OBSTACLES, ALPHA, TEMPERATURE

    clock = pygame.time.Clock()
    car = Car(CELL_SIZE)
    agent = QLearningAgent()

    score,best_score = 0,0
    episode =1
    scores = []

    success_count = 0  
    running = True

    REWARD_GRID = [[random.uniform(-0.5, -1) for _ in range(10)] for _ in range(10)]

    # Supprimer rewards des obstacles et de la case finale
    for (ox, oy) in OBSTACLES:
        REWARD_GRID[oy][ox] = 0  # Reward pour les obstacles
    REWARD_GRID[9][9] = 100  # Reward pour case finale

    while running:
        draw_grid(screen, CELL_SIZE, REWARD_GRID, OBSTACLES)

        state = car.get_state()

        # mmettre à jour les capteurs
        car.update_sensors(OBSTACLES, (10, 10))

        # Choisir une action
        action = agent.choose_action(state, TEMPERATURE)

        # Déplacer la voiture
        reward, done, score = car.move(action, OBSTACLES, CELL_SIZE, score, REWARD_GRID)

        next_state = car.get_state()

        # Mettre à jour la table Q
        agent.update_q_table(state, action, reward, next_state, done)
        score += reward

        if done:

            TEMPERATURE = max(TEMPERATURE_MIN, TEMPERATURE * TEMPERATURE_DECAY)
            ALPHA = max(ALPHA_MIN, ALPHA * ALPHA_DECAY)

            if reward == 100 and TEMPERATURE_MIN == round(TEMPERATURE, 2):
                success_count += 1
                if success_count == 10 :
                    generate_map_image_with_curve(car, OBSTACLES, scores, REWARD_GRID, "map_with_curve.png")

                    running = False  # Terminer après avoir généré l'image
            else:
                success_count = 0

            if score > best_score:
                best_score = score

            scores.append(score)
            car.reset()

            scores.append(score)
            episode += 1
            score = 0

        screen.fill(WHITE)
        draw_grid(screen, CELL_SIZE, REWARD_GRID, OBSTACLES)


        # Dessiner la case finale
        pygame.draw.rect(screen, (0, 255, 0), (9 * CELL_SIZE, 9 * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Vert

        draw_obstacles(screen, OBSTACLES, CELL_SIZE)

        car.draw(screen)
        draw_text(screen, f"Épisode: {episode}", 18, BLACK, 10, HEIGHT - 80)
        draw_text(screen, f"Score: {score:.2f}", 18, BLACK, 10, HEIGHT - 60)
        draw_text(screen, f"Meilleur score: {best_score:.2f}", 18, BLACK, 10, HEIGHT - 40)
        draw_text(screen, f"TEMPERATURE: {TEMPERATURE:.2f}", 18, BLACK, 10, HEIGHT -20)
        draw_text(screen, f"ALPHA: {ALPHA:.2f}", 18, BLACK, 10, HEIGHT -10)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()



if __name__ == "__main__":
    main()
