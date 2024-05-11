# MapleOmok
MapleOmok is a recreation of the MapleStory Omok mini-game written in python/pygame.

## Installation (Development)
1. Install [Python 3.11+](https://www.python.org/downloads/) (Make sure to `check` "Add python.exe to PATH")
   
   ![image](https://github.com/Bratah123/MapleOmok/assets/58405975/36cab769-e5a3-4ad5-ad0e-b46395a194f7)

2. Run `start.bat` file in the project file.

## User Interactability
When you first launch the game, you can click "Play Game" and you'll be tossed into the game with an AI with a minimax depth of 5.
In order to win the game, you must match 5-in-a-row much like tic-tac-toe's 3-in-a-row.

See [Gallery](https://github.com/Bratah123/MapleOmok/?tab=readme-ov-file#gallery) section for visual images of the game and buttons.

## Code Structure
The current code structure follows a Component-Scene System. This means that Scenes contains components to be rendered and Components represent those objects that are rendered into the game.
Here is a diagram showing that visually. It is good to note that Components can contain other components.

![image](https://github.com/Bratah123/MapleOmok/assets/58405975/af85e246-dfa4-4124-81fe-d8d9ce8e4f11)

- The [assets](https://github.com/Bratah123/MapleOmok/tree/main/assets) folder contains all images, fonts, sounds related to the game and are used to be rendered into the game for visual effects.
- The [components](https://github.com/Bratah123/MapleOmok/tree/main/components) folder contain all the Abstract classes for defining said Components of the game.
- The [interactables](https://github.com/Bratah123/MapleOmok/tree/main/interactables) folder contains a button class which is re-used throughout the game to create interactable buttons given a callback.
- The [scenes](https://github.com/Bratah123/MapleOmok/tree/main/scenes) folder contains all the various scenes which HOLD the components and are rendered in the main game loop.

Finally, the most important folder is the [game](https://github.com/Bratah123/MapleOmok/tree/main/game) folder which contains the entire logic of the game AND the AI code.
The minimax feature can be found in [opponent_ai.py](https://github.com/Bratah123/MapleOmok/blob/main/game/opponent_ai.py) file and contains the actual minimax algorithm and evaluation functions.
And any further optimization techinques (1D Array, Proximity Searching, etc...) can be found in [omok_board.py](https://github.com/Bratah123/MapleOmok/blob/main/game/omok_board.py) mainly in the `def __init__()`
method which instantiates many of the data structures used in creating this project.

## Gallery
![MainMenu](https://github.com/Bratah123/MapleOmok/assets/58405975/b70e308b-5cbe-45d9-ad2e-ac3adeef8133)
![Game](https://github.com/Bratah123/MapleOmok/assets/58405975/c8a3e845-6ea5-4d1d-b972-13efdbd5c301)
![WinScene](https://github.com/Bratah123/MapleOmok/assets/58405975/67794cd1-3130-477b-b3dd-2049326649a5)

## Project Report / Data / Evaluation
You can find it [here](https://docs.google.com/document/d/1qyXtqORrGSsi6rD4w9Txq-F9oyzOISQvCNm3jnmliVQ/edit?usp=sharing)

![Winrate](https://github.com/Bratah123/MapleOmok/assets/58405975/babcf4a1-d0dc-4bc6-8c6b-9153648c245a)
![image](https://github.com/Bratah123/MapleOmok/assets/58405975/c6f7688d-ac2b-4131-80af-599883040cff)
