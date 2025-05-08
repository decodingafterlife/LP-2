def encrypt(message, key):

    num_rows = (len(message) + key - 1) // key
    
    matrix = [['' for _ in range(key)] for _ in range(num_rows)]
    
    char_index = 0
    for row in range(num_rows):
        for col in range(key):
            if char_index < len(message):
                matrix[row][col] = message[char_index]
                char_index += 1
    
    ciphertext = ''
    for col in range(key):
        for row in range(num_rows):
            if matrix[row][col]:
                ciphertext += matrix[row][col]
    
    return ciphertext

def decrypt(ciphertext, key):
    num_rows = (len(ciphertext) + key - 1) // key
    
    cols_with_extra_char = len(ciphertext) % key
    if cols_with_extra_char == 0:
        cols_with_extra_char = key
    
    matrix = [['' for _ in range(num_rows)] for _ in range(key)]
    
    char_index = 0
    for col in range(key):
        col_height = num_rows if col < cols_with_extra_char else num_rows - 1
        
        for row in range(col_height):
            if char_index < len(ciphertext):
                matrix[col][row] = ciphertext[char_index]
                char_index += 1
    
    plaintext = ''
    for row in range(num_rows):
        for col in range(key):
            if row < len(matrix[col]) and matrix[col][row]:
                plaintext += matrix[col][row]
    
    return plaintext

message = input("Enter the message: ")
key = int(input("Enter the key (number of columns): "))
    
if key <= 0:
    print("Key must be a positive integer.")
elif key >= len(message):
    print("Warning: Key should be smaller than message length for effective encryption.")
    
encrypted_message = encrypt(message, key)
print(f"\nEncrypted message: {encrypted_message}")
    
decrypted_message = decrypt(encrypted_message, key)
print(f"Decrypted message: {decrypted_message}")

