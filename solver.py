# Import from setup module
import time, os, threading
from setup import matrix, Piece, pieces, impossible_patterns

elapsed = 0

def can_fit(matrix, piece_orientation, position):
    x, y = position
    for i in range(4):
        for j in range(4):
            if piece_orientation[i][j] != 0:
                # Check bounds
                if (x + i >= len(matrix)) or (y + j >= len(matrix[0])):
                    return False
                # Check if the cell in the matrix is empty (0)
                if matrix[x + i][y + j] != 0:
                    return False
    return True

def has_impossible_pattern(matrix, impossible_patterns):
    for pattern in impossible_patterns:
        pat_rows = len(pattern)
        pat_cols = len(pattern[0])
        mat_rows = len(matrix)
        mat_cols = len(matrix[0])
        for i in range(mat_rows - pat_rows + 1):
            for j in range(mat_cols - pat_cols + 1):
                match = True
                for x in range(pat_rows):
                    for y in range(pat_cols):
                        # NXOR: True if both are 0 or both are not 0
                        a = matrix[i + x][j + y]
                        b = pattern[x][y]
                        if not ((a == 0 and b == 0) or (a != 0 and b != 0)):
                            match = False
                            break
                    if not match:
                        break
                if match:
                    return True
    return False

def place_piece(matrix, piece_orientation, position, piece_id):
    x, y = position
    for i in range(4):
        for j in range(4):
            if piece_orientation[i][j] != 0:
                matrix[x + i][y + j] = piece_id

def remove_piece(matrix, piece_orientation, position):
    x, y = position
    for i in range(4):
        for j in range(4):
            if piece_orientation[i][j] != 0:
                matrix[x + i][y + j] = 0

def print_matrix_no_border(matrix,pieces,call=''):
    # Clear the terminal before printing subsequent sequences
    if call != 'first' and call != 'last':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\rSolving puzzle...")
    if call == 'last':
        print("\rSolved!")
    id_to_color = {piece.ID: piece.color for piece in pieces}
    for i in range(2, 7):
        colored_row = []
        for j in range(2, 13):
            cell = matrix[i][j]
            if cell == 0:
                colored_row.append('\033[0m  ')
            else:
                color = id_to_color.get(cell, (255, 255, 255))
                r, g, b = color
                colored_row.append(f'\033[48;2;{r};{g};{b}m  \033[0m')
        print(''.join(colored_row))
    global elapsed
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    print(f"Elapsed time: {minutes:02d}:{seconds:02d}")

def solve(matrix, available_pieces, pieces, depth=0):
    if not available_pieces:
        print("\nSolution found:")
        print_matrix_no_border(matrix,pieces,call='last')
        return True

    for idx, piece_idx in enumerate(available_pieces):
        piece = pieces[piece_idx - 1]
        for orientation_idx, orientation in enumerate(piece.orientations):
            for x in range(2, 7):
                for y in range(2, 13):
                    pos = (x, y)
                    if can_fit(matrix, orientation, pos):
                        place_piece(matrix, orientation, pos, piece.ID)
                        # Check for impossible patterns
                        if has_impossible_pattern(matrix, impossible_patterns):
                            remove_piece(matrix, orientation, pos)
                            continue
                        # Recurse with this piece removed from available_pieces
                        if solve(matrix, available_pieces[:idx] + available_pieces[idx+1:], pieces, depth+1):
                            return True
                        remove_piece(matrix, orientation, pos)
             
        print_matrix_no_border(matrix,pieces)
        print()
        return False

def elapsed_timer(stop_event):
    global elapsed
    start = time.time()
    while not stop_event.is_set():
        elapsed = time.time() - start
        time.sleep(0.2)
    elapsed = time.time() - start

# # Setup puzzle - No.1 (Starter)
# place_piece(matrix, pieces[4].orientations[0], (2,2), 5)    # purple
# place_piece(matrix, pieces[9].orientations[4], (2,3), 'a')  # olive
# place_piece(matrix, pieces[6].orientations[0], (2,6), 7)    # turquoise 
# place_piece(matrix, pieces[2].orientations[6], (2,8), 3)    # blue
# place_piece(matrix, pieces[0].orientations[0], (4,2), 1)    # red 
# place_piece(matrix, pieces[1].orientations[0], (3,4), 2)    # green
# place_piece(matrix, pieces[11].orientations[3], (5,5), 'c') # orange
# place_piece(matrix, pieces[10].orientations[0], (4,6), 'b') # yellow
# place_piece(matrix, pieces[8].orientations[1], (5,8), 9)    # dark blue
# available_pieces = [4,6,8]

# Setup puzzle - No.32 (Master)
place_piece(matrix, pieces[8].orientations[1], (2,2), 9)    # dark blue
place_piece(matrix, pieces[9].orientations[0], (2,4), 'a')  # olive
place_piece(matrix, pieces[10].orientations[2], (3,6), 'b') # yellow
place_piece(matrix, pieces[11].orientations[0], (2,8), 'c') # orange
available_pieces = [8,1,7,5,6,4,3,2]

# # Setup puzzle - No.37 (Wizard)
# place_piece(matrix, pieces[2].orientations[0], (2,2), 3)    # blue
# place_piece(matrix, pieces[5].orientations[6], (4,4), 6)    # pink
# available_pieces = [1,2,4,5,7,8,9,10,11,12]


if __name__ == "__main__":
    print("Puzzle to be solved:")
    print_matrix_no_border(matrix,pieces,call='first')
    time.sleep(4)
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=elapsed_timer, args=(stop_event,))
    timer_thread.start()
    try:
        if solve(matrix, available_pieces, pieces) == False:
            print("Solution not found.")
    finally:
        stop_event.set()
        timer_thread.join()




