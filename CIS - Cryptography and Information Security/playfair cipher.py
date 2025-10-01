# Playfair Cipher - Simple Encryption
# ----------------------------------------------------
# Rules:
# 1. Create a 5x5 matrix from a keyword (I and J are treated the same).
# 2. Split the message into pairs (digraphs).
#    - If both letters are the same, insert 'X' between them.
#    - If odd number of letters, add 'X' at the end.
# 3. Encrypt each pair:
#    - Same row → replace each with letter to the right (wrap around).
#    - Same column → replace each with letter below (wrap around).
#    - Rectangle → replace with letters in same row, but at other pair's column.
# ----------------------------------------------------


# --------- Step 1: Create 5x5 key matrix ---------
def generate_matrix(key):
    # Convert to uppercase and replace J with I (Playfair uses 25 letters)
    key = key.upper().replace("J", "I")
    result = ""
    # Add key + all alphabets (A-Z without J) → remove duplicates
    for ch in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in result:
            result += ch
    # Convert string into a 5x5 matrix
    return [list(result[i:i+5]) for i in range(0, 25, 5)]


# --------- Step 2: Find position of a letter in the matrix ---------
def pos(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j   # row, column


# --------- Step 3: Prepare message into pairs ---------
def prepare(msg):
    msg = msg.upper().replace("J", "I").replace(" ", "")
    i, pairs = 0, []
    while i < len(msg):
        a = msg[i]
        # Take next letter if exists, else use 'X' as padding
        b = msg[i+1] if i+1 < len(msg) else "X"

        if a == b:
            # If both letters same → insert 'X' after first letter
            pairs.append(a + "X")
            i += 1
        else:
            # Otherwise take them as a pair
            pairs.append(a + b)
            i += 2
    return pairs


# --------- Step 4: Encrypt pairs ---------
def encrypt(msg, matrix):
    cipher = ""
    for a, b in prepare(msg):
        r1, c1 = pos(matrix, a)   # position of first letter
        r2, c2 = pos(matrix, b)   # position of second letter

        if r1 == r2:
            # Same row → replace each with letter to its right
            cipher += matrix[r1][(c1+1) % 5] + matrix[r2][(c2+1) % 5]

        elif c1 == c2:
            # Same column → replace each with letter below
            cipher += matrix[(r1+1) % 5][c1] + matrix[(r2+1) % 5][c2]

        else:
            # Rectangle rule → swap columns
            cipher += matrix[r1][c2] + matrix[r2][c1]

    return cipher


# --------- Main Program ---------
key = input("Enter key: ")      # Example: "MONARCHY"
matrix = generate_matrix(key)   # Build 5x5 key matrix
msg = input("Enter message: ")  # Example: "BALLOON"
print("Encrypted:", encrypt(msg, matrix))

