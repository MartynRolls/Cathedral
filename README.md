# Cathedral

## Graphics
The game uses sprite stacking to give the board and pieces a 3d look. Below is the Cathedral, the Black Tower, and the White Castle pieces.

![output](https://github.com/user-attachments/assets/bb41c53c-a070-4296-be28-d1793957f50c)

The game is made up of 23 pieces. The Cathedral, and a set of 11 for each of the players (note blacks pieces are mirrored to whites). 

![output](https://github.com/user-attachments/assets/bbeb11f3-cc1a-458a-9a2a-67fd3e0971ba)

The pieces can be placed onto the board, which is rendered by creating a new sprite sheet, adding every placed piece onto the sprite sheet, and rendering the entire sheet as you would one piece.

![BoardExample](https://github.com/user-attachments/assets/08e84aa5-6193-4e79-9df3-7a1c9e409d34)


## Rules
This version of the game uses slightly varied rules from the original. The rules are as follows;

The White player starts by placing the Cathedral, followed by the Black player placing their first piece.

Turn then proceeds with each player placing a piece if they can. The game is over when no player can place another piece.

If a player fully encloses an area with their pieces and the walls (diagonals do not count), they may claim that territory.

If the enclosed area contains only one of the enemys pieces, that piece may be removed to claim the territory.

The territory may not be claimed if the enclosed space has more than one enemy piece, or contains the Cathedral.

When the game is over, the winner can be calculated by adding the points of the remaining pieces (the number of squares a piece would occupy). He who has the fewest points wins.

## Controls
Moving a piece: W/I, A/J, S/K, D/L for Up, Left, Right, and Down respectively.

Rotating a piece: Q/U and E/O to rotate Clockwise and Anticlockwise respectively.

Changing select piece: Shift + A/J/D/L to go to next or previous piece.

Rotating the board: Shift + Q/U/E/O to rotate Clockwise or Anticlockwise.
