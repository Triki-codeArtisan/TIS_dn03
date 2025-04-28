import numpy as np

# def main():
#     # Example input
#     vhod = [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0]  # Example binary sequence
#     n = 8  # Example codeword length

#     # Call the function
#     izhod, crc = naloga3(vhod, n)

#     # Print the results
#     print("Dekodirano sporočilo:", izhod)

def makeRows(i: int, m: int) -> list:
    # Binary representation of i
    bin_str = bin(i)[2:]  # Remove '0b' prefix
    
    # Pad the binary string to length m
    if len(bin_str) < m:
        bin_str = bin_str.zfill(m)  # padding with 0
    elif len(bin_str) > m:
        print("error - bit vector too long")

    # Check if exactly one 1 bit (Hamming weight check)
    has_one_bit = i & (i - 1) == 0 and i != 0  # This checks if the number has exactly one bit set

    # Convert binary string to list of 0s and 1s
    bit_list = [int(bit) for bit in bin_str]

    return bit_list, has_one_bit

def make_Ht(n, m):  
    matrix = np.zeros((n-1 -m, m), dtype=np.uint8) # vrstice, stolpci 
    cntr = 0
    for i in range(1, n):
        row, exactly_1 = makeRows(i, m)
        if not exactly_1:
            matrix[cntr] = row # np avtomatsko pretvori v array
            cntr += 1
    
    Ht = np.concatenate( (matrix, np.eye(m, dtype=np.uint8)), axis=0 )
    return Ht

def getSindrom(y, Ht, n, m):
    s = []
    for bit in range(m):
        sum = 0
        for i in range(n-1):
            clen = np.bitwise_and(Ht[i][bit], y[i])  
            sum += clen
        
        s.append(sum%2)
    return s

def findErrRow(Ht, s):
    for i in range(Ht.shape[0]):
        if np.array_equal(s, Ht[i]):
            return i  
    print("err: row not found")
    return None 

def naloga3(vhod: list, n: int) -> tuple[list, str]:
    """
    Izvedemo dekodiranje binarnega niza `vhod`, zakodiranega 
    z razsirjenim Hammingovim kodom dolzine `n` in poslanega 
    po zasumljenem kanalu.
    Nad `vhod` izracunamo vrednost `crc` po standardu CRC-8/LTE.

    Parameters
    ----------
    vhod : list
        Sporocilo y, predstavljeno kot seznam bitov (stevil tipa int) 
    n : int
        Stevilo bitov v kodni besedi
    
    Returns
    -------
    (izhod, crc) : tuple[list, str]
        izhod : list
            Odkodirano sporocilo y (seznam bitov - stevil tipa int)
        crc : str
            Vrednost CRC, izracunana nad `vhod`. Niz dveh znakov.
    """
    m = int(np.log2(n))
    k = n-m -1 ## -1 ker pri npr L(7, 4) je spremenljivka n ubistvu 8 
    # print(k)
    # print(n)
    # print(m)

    Ht = make_Ht(n, m)
    nicle = np.zeros(m)
    # print(Ht)
    # print()
    # print(Ht.T)

    # decode
    izhod = []
    y_list = []
    chunks = [vhod[i:i+n] for i in range(0, len(vhod), n)]
    for y_list in chunks:
        
        y = np.array(y_list, dtype=np.uint8)
        parity = np.remainder(np.sum(y), 2)
        sindrom = getSindrom(y, Ht, n, m)

        if(parity == 0):
            if np.array_equal(sindrom, nicle):
                izhod.extend(y_list[:k])
            else:
                izhod.extend([-1] * k)

        else:
            if np.array_equal(sindrom, nicle):
                izhod.extend(y_list[:k])
            else:
                e_idx = findErrRow(Ht, sindrom)
                if(e_idx >= k):
                    izhod.extend(y_list[:k])
                else:
                    y_list[e_idx] = y_list[e_idx] ^1
                    izhod.extend(y_list[:k])


        # na koncu bo v zadnji iteraciji vse appendan, 
        # je pa treba se enkrat dekodirat besedo

    # end for
    # end decode
###############################################################################

    crc = ''
    return (izhod, crc)

# if __name__ == "__main__":
#     main()

