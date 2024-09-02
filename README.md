# AI-Powered Flappy Bird with NEAT Algorithm

This repository contains the source code for an AI-powered Flappy Bird game, where the AI uses the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to learn how to navigate through dynamically moving pipes. The AI continuously evolves to improve its performance over multiple generations, aiming to achieve the highest possible score.

![Flappy Bird AI Demo](flappy_bird_demo.gif)

## Key Features
- **NEAT Algorithm**: Implements the NEAT algorithm to evolve the neural network controlling the bird, enabling it to adapt and improve over time through multiple generations.
- **Dynamic Pipes**: Pipes move vertically with varying speeds, increasing the complexity and challenge for the AI for an added twist.
- **Custom Graphics & Sounds**: Includes custom bird animations, background, and sound effects to enhance the gameplay experience.
- **Fitness Evaluation**: The AI’s fitness is evaluated based on its ability to avoid obstacles and score points, with positive rewards for passing pipes and surviving and negative rewards for collisions.
- **Visualization**: Displays real-time game progress, including the bird’s position, pipe positions, score, current generation, and more.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/flappy-bird-neat.git
    ```
2. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the game:
    ```bash
    python flappy_bird_ai.py
    ```

## How It Works
- **Bird**: The bird is controlled by a neural network that decides whether it should flap based on inputs like its vertical distance from the pipes.
- **Pipes**: The pipes move horizontally across the screen and vary in vertical position as well to create a dynamic and challenging environment.
- **NEAT Algorithm**: The AI evolves over generations, with each genome in the population representing a different neural network. The fitness of each genome is determined by how long its bird survives and how many pipes it successfully passes.

## Files Included
- **`flappy_bird_ai.py`**: Main game file containing the logic for the AI, bird, pipes, and game loop.
- **`neat-config.txt`**: Configuration file for the NEAT algorithm.

## NEAT Configuration
The NEAT algorithm configuration is handled through the `neat-config.txt` file, where you can adjust parameters such as population size, mutation rates, and fitness thresholds.

## How to Play
- Run the game and watch as the AI learns to navigate the obstacles.
- Observe the evolution of the AI through multiple generations and how it improves over time.

## Future Improvements
- **Game Revision**: In the future I'll be using this as a frame to create a new version of this with more difficult obstacles for the AI to adapt to, currently in development!

---

Try and test it out!
