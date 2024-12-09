import numpy as np
import pickle
import os
import random

ALPHA = 1.0
ALPHA_DECAY = 0.99
ALPHA_MIN = 0.1

GAMMA = 0.99

TEMPERATURE = 1.0
TEMPERATURE_DECAY = 0.99
TEMPERATURE_MIN = 0.10

STATE = [10, 10]
ACTIONS = [0, 1, 2, 3]  # haut, droite, bas, gauche 


class QLearningAgent:
    def __init__(self):
        self.q_table = np.zeros((STATE[0], STATE[1], len(ACTIONS)))

    def categoriser_etat(self, state):
        """
        Transforme un état en version simple pour qu'il rentre dans la table
        """
        # limite l'état dans les bornes de la grille
        x = max(0, min(STATE[0] - 1, state[0]))
        y = max(0, min(STATE[1] - 1, state[1]))
        return x, y


    def choose_action(self, state, temperature):
        """
        Choisir une action basée sur les valeurs Q actuelles en utilisant la méthode Softmax
        """
        discrete_state = self.categoriser_etat(state)
        q_values = self.q_table[discrete_state]

        # normaliser pour éviter les overflows
        q_values = q_values - np.max(q_values)

        # calcul des probabilites avec Softmax
        exp_q = np.exp(q_values / max(temperature, 0.1))
        probabilities = exp_q / np.sum(exp_q)

        # vérification des probabilités valides
        if np.any(np.isnan(probabilities)):
            probabilities = np.ones(len(q_values)) / len(q_values)

        return np.random.choice(len(q_values), p=probabilities)


    def update_q_table(self, state, action, reward, next_state, done):
        """
        Mettre à jour la table Q en utilisant l'équation de mise à jour du Q-learning
        """
        # transforme l'état actuel et le suivant en une version simplifiée pour la table Q
        discrete_state = self.categoriser_etat(state)
        discrete_next_state = self.categoriser_etat(next_state)

        #prend la valeur actuelle de l'action dans cet état
        q_value = self.q_table[discrete_state][action]
        # Trouve la meilleure valeur possible pour l'état suivant
        max_next_q = np.max(self.q_table[discrete_next_state])

        #calcule la nouvelle estimation de la valeur Q
        cible = reward + (GAMMA * max_next_q * (1 - done))

        #Met à jour la valeur dans la table Q 
        self.q_table[discrete_state][action] += ALPHA * (cible - q_value)


