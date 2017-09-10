import cs50

import sys

def main():
    
    # Check whether command-line argument has 2 argument
    if len(sys.argv) != 2:      
        print("Usage: ./vigenere k")
        exit(1)
        
    keyword = sys.argv[1]    
    
    # Check whether keyword contains only alphabetical symbols    
    if keyword.isalpha() == False:
        print("Usage: ./vigenere k")
        exit(1)
    
    print("plaintext: ", end="")
    p = cs50.get_string()
    k = 0  #keyword letter tracker
    c = None  #ciphered letter
    
    if p != None:
        print("ciphertext: ", end="")
        # iterate over the plaintext
        for letter in p:  
            if letter.isalpha():
                n_keyword = make_mod(keyword[k])  #normalized keyword
                if letter.isupper():
                    c = ((((ord(letter) - 65) + n_keyword)%26) + 65)
                else:
                    c = ((((ord(letter) - 97) + n_keyword)%26) + 97)
                print("{}".format(chr(c)), end="")
                k = (k + 1) % len(keyword)
            else:
                print("{}".format(letter), end="")
                continue
    else:
        exit(1)
    print()  # last space for command line
    # Vigenere worked correctly   
    exit(0)

# Normalize keyword's letter
def make_mod(key):
    if key.isupper():
        return ord(key) % 65
    else:
        return ord(key) % 97

if __name__ == "__main__":
    main()        