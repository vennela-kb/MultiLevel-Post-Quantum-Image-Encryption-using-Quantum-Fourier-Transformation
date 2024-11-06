"""
**LWE**
Our public key is A & B -> (A, B) -> Z^n_q:
    A is a collection of random numbers Z^n_q 
    B = A.s + e (mod q) -> Z^n_q , where:
        s -> secret value (Private key)
        e -> error

When trying to encrypt:
    Encrypted message = (u, v) where, 
        u = ∑(samples from A) (mod q)
        v = ∑(samples from B) - (q.M)/2 (mod q), where 
            M is a single bit message

To decrypt: 
    Decrypted message = v - s.u (mod q)
        if (Decrypted message < q/2) Message is zero(0)
        else if (Decrypted message > q/2) Message is one(1)
"""

import random
import base64
import time
import psutil


# Measure CPU and memory before running the code
cpu_before = psutil.cpu_percent(interval=None)
mem_before = psutil.virtual_memory().used

start_time = time.time()

# s = random.randint(2, 10)
s = 5
q = 97
n = 20

# max_e = 4
# e = [random.randint(1, max_e) for _ in range(n)]
e = [3, 3, 4, 1, 3, 3, 4, 4, 1, 4, 3, 3, 2, 2, 3, 2, 4, 4, 1, 3]

# A = [random.randint(1, q) for _ in range(n)]
print("Public keys A & B:")
A = [80, 86, 19, 62, 2, 83, 25, 47, 20, 58, 45, 15, 30, 68, 4, 13, 8, 6, 42, 92]
print("A = ", A)


# B_i = (A_i.s) + e (mod q)
def compute_B():
    B = []
    for i in range(n):
        B.append((A[i] * s + e[i]) % q)
    return B


B = compute_B()
print("B = ", B)

# B =  [15, 45, 2, 20, 13, 30, 32, 45, 4, 3, 34, 78, 55, 51, 23, 67, 44, 34, 17, 75]


def encrypt_bit(M):
    numberOfSamplesToBeTaken = 4

    sample_indexes = set()
    while len(sample_indexes) < numberOfSamplesToBeTaken:
        sample_indexes.add(random.randint(0, n - 1))

    # Converting the set to list because set's are not indexable but they do help avoid duplicates
    sample_indexes_list = list(sample_indexes)

    samples = []
    for i in range(numberOfSamplesToBeTaken):
        samples.append((A[sample_indexes_list[i]], B[sample_indexes_list[i]]))

    u = 0
    v = 0
    for x in range(numberOfSamplesToBeTaken):
        u = u + samples[x][0]
        v = v + samples[x][1]

    v = v + ((q // 2) * M)
    u = u % q
    v = v % q

    return (u, v)


def decrypt_bit(u, v):
    dec = (v - (s * u)) % q
    if dec > q / 2:
        return 1
    else:
        return 0


def cipher_to_bits(file_path):
    with open(file_path, "r") as file:
        base64_text = file.read().strip().encode("utf-8")

    binary_data = base64.b64decode(base64_text)
    bit_string = "".join(format(byte, "08b") for byte in binary_data)

    return bit_string


def bits_to_cipher(bit_string):
    byte_array = bytearray()
    for i in range(0, len(bit_string), 8):
        # Convert the list of bits to a string
        byte_str = ''.join(str(bit) for bit in bit_string[i : i + 8])
        byte_array.append(int(byte_str, 2))

    base64_string = base64.b64encode(bytes(byte_array)).decode("utf-8")
    return base64_string

file_path = "../Image-Encryption-using-AES/cipher.txt"
bit_string_message = cipher_to_bits(file_path)

encrypted_message = [encrypt_bit(int(bit)) for bit in bit_string_message]
file_message_str = "".join(str(encrypted_message))

with open("./encrypted_message.txt", "w") as file:
    file.write(file_message_str)

decrypted_bits = [decrypt_bit(u, v) for (u, v) in encrypted_message]
decrypted_message = bits_to_cipher(decrypted_bits)
with open("./LWEcipher.txt", "w") as file:
    file.write(decrypted_message)

# Your code here
end_time = time.time()

# Measure CPU and memory after running the code
cpu_after = psutil.cpu_percent(interval=None)
mem_after = psutil.virtual_memory().used

elapsed_time = end_time - start_time
cpu_usage = cpu_after - cpu_before
memory_usage = (mem_after - mem_before) / (1024 * 1024)  # Convert to MB

print(f"Elapsed time: {elapsed_time} seconds")
print(f"CPU usage: {cpu_usage} %")
print(f"Memory usage: {memory_usage} MB")
