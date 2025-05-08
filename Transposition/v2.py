def encrypt(plaintext, key):
    num_cols = len(key)
    num_rows = (len(plaintext) + num_cols - 1) // num_cols
    
    matrix = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    
    index = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if index < len(plaintext):
                matrix[row][col] = plaintext[index]
                index += 1
            else:
                matrix[row][col] = 'X'
    
    key_map = {}
    for i, k in enumerate(key):
        key_map[k] = i
    
    ciphertext = ''
    for k in sorted(key_map.keys()):
        col = key_map[k]
        for row in range(num_rows):
            if matrix[row][col] != 'X':
                ciphertext += matrix[row][col]
    
    return ciphertext

def decrypt(ciphertext, key):
    num_cols = len(key)
    num_rows = (len(ciphertext) + num_cols - 1) // num_cols
    
    col_lengths = [num_rows] * num_cols
    
    full_cols = len(ciphertext) % num_cols
    if full_cols == 0:
        full_cols = num_cols
    else:
        for i in range(full_cols, num_cols):
            col_lengths[i] = num_rows - 1
    
    key_map = {}
    for i, k in enumerate(key):
        key_map[k] = i
    
    matrix = [['' for _ in range(num_rows)] for _ in range(num_cols)]
    
    index = 0
    for k in sorted(key_map.keys()):
        col = key_map[k]
        for row in range(col_lengths[col]):
            if index < len(ciphertext):
                matrix[col][row] = ciphertext[index]
                index += 1
    
    plaintext = ''
    for row in range(num_rows):
        for col in range(num_cols):
            if row < len(matrix[col]) and matrix[col][row] and matrix[col][row] != 'X':
                plaintext += matrix[col][row]
    
    return plaintext

def display_matrix(plaintext, key):
    num_cols = len(key)
    
    print("\nPlaintext arranged in grid (row by row):")
    for i in range(0, len(plaintext), num_cols):
        row = plaintext[i:i+num_cols].ljust(num_cols)
        print(row)

    
plaintext = input("Enter the message to encrypt: ")
key_str = input("Enter the key (numbers separated by spaces): ")
    
try:
    key = [int(k) for k in key_str.split()]
        
    if not key or max(key) != len(key) or min(key) < 1 or len(set(key)) != len(key):
        print("Invalid key. Key must be a permutation of numbers from 1 to n.")
        
        
    display_matrix(plaintext, key)
        
    encrypted = encrypt(plaintext, key)
    print(f"\nEncrypted message: {encrypted}")
        
    decrypted = decrypt(encrypted, key)
    print(f"\nDecrypted message: {decrypted}")
    print(f"Original message: {plaintext}")
        
except ValueError:
    print("Invalid key format. Please enter numbers separated by spaces.")

