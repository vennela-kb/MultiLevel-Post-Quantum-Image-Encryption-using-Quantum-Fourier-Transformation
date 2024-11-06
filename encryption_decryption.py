

import base64
import hashlib
import numpy as np
import psutil
import time
!pip install qiskit pillow pycryptodome
from Crypto import Random
from Crypto.Cipher import AES
from PIL import Image
from google.colab import files
from io import BytesIO
!pip install qiskit-aer # Added qiskit-aer to the installation command.
from qiskit import QuantumCircuit, transpile, assemble # Removed Aer from this line
from qiskit.circuit.library import QFT
from qiskit_aer import Aer # Added this line to import Aer from the correct module.

from google.colab import files
from io import BytesIO
from PIL import Image
from google.colab import drive
drive.mount('/content/drive')
uploaded = files.upload()

# Get the actual key from the uploaded dictionary
key = list(uploaded.keys())[0]

# Open the image using the correct key
im = Image.open(BytesIO(uploaded[key])).convert("L")

import matplotlib.pyplot as plt
plt.imshow(im)
plt.show()

im

#Define the AES Cipher Class
class AESCipher(object):
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        t = (self.bs - len(s) % self.bs)
        return s + t * chr(t).encode('utf-8')

    @staticmethod
    def _unpad(s):
        return s[:-s[-1]]

"""# **Perform QFT on the Image**"""

def encode_image(image, n):
    im = Image.open(image).convert("L")
    pixel_values = np.array(im.getdata())
    normalized_array = pixel_values / np.linalg.norm(pixel_values)

    qc = QuantumCircuit(n)
    qc.initialize(normalized_array.data, qc.qubits)
    return qc

def apply_qft(qc, n):
    qc.append(QFT(n), qc.qubits)
    return qc

# Calculate the size of the image needed for a power of 2 number of pixels
target_size = 2**int(np.ceil(np.log2(im.size[0] * im.size[1])))

def encode_image(image, n):
    if isinstance(image, str): # Check if 'image' is a file path
        im = Image.open(image).convert("L")
    elif isinstance(image, BytesIO): # Check if 'image' is a BytesIO object
        im = Image.open(image).convert("L")
    else:
        raise ValueError("Invalid input: image must be a file path or a BytesIO object") # Raise an error if neither

    # Resize the image within the function
    im = im.resize((int(np.sqrt(target_size)), int(np.sqrt(target_size))))

    pixel_values = np.array(im.getdata())
    normalized_array = pixel_values / np.linalg.norm(pixel_values)

    qc = QuantumCircuit(n)
    # Ensure the statevector is the correct length
    if len(normalized_array) != 2**n:
        raise ValueError("Statevector length is not a power of 2")
    qc.initialize(normalized_array.data, qc.qubits)
    return qc

n = int(np.log2(target_size))  # Define the number of qubits based on image size
qc = encode_image(BytesIO(uploaded[key]), n) # Pass the BytesIO object directly
qc = apply_qft(qc, n)

"""# **Measure and Retrieve the Transformed Image**"""

def measure_image_state(qc, n):
    qc.measure_all() # Add measurements to the circuit
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 4096
    t_qc = transpile(qc, aer_sim)
    result = aer_sim.run(t_qc, shots=shots).result()
    counts = result.get_counts(qc)
    return counts

counts = measure_image_state(qc, n)

"""# **Encrypt Part of the QFT Result**"""

def encrypt_transformation(transformation, key):
    aes = AESCipher(key)
    return aes.encrypt(transformation)

# Example encryption on the LL (Low-Low) frequency component
transformation = "Your selected transformation data here"
key = "your_secret_key"
cipher = encrypt_transformation(transformation.encode('utf-8'), key)

with open("cipher.txt", "wb") as f:
    f.write(cipher)

"""# **Decrypt the Encrypted Data**"""

def decrypt_transformation(cipher_text, key):
    aes = AESCipher(key)
    return aes.decrypt(cipher_text)

with open("cipher.txt", "rb") as f:
    cipher_text = f.read()

decrypted_data = decrypt_transformation(cipher_text, key)

"""# **Apply Inverse QFT and Reconstruct the Image**"""

def inverse_qft(qc, n):
    # Apply the inverse QFT
    qc.append(QFT(n).inverse(), qc.qubits)
    return qc

def reconstruct_image_from_counts(counts, n):
    # Convert the counts to a numpy array
    # You may need to adjust the way you interpret counts based on your specific requirements
    pixel_values = np.zeros((2**n,), dtype=np.float64)
    total_counts = sum(counts.values())

    for outcome, count in counts.items():
        # Remove spaces from the outcome string before conversion
        outcome = outcome.replace(" ", "")
        index = int(outcome, 2)
        pixel_values[index] = count / total_counts  # Normalize the counts

    # Reshape to the original image dimensions
    side_length = int(np.sqrt(target_size))
    pixel_values = (pixel_values * 255).astype(np.uint8)  # Scale to 0-255
    return Image.fromarray(pixel_values.reshape((side_length, side_length)))

qc = inverse_qft(qc, n)
counts = measure_image_state(qc, n)

# Convert the counts to a format suitable for image reconstruction
# This assumes you want to reconstruct the image based on the measured counts
def reconstruct_image_from_counts(counts, n):
    # Convert the counts to a numpy array
    # You may need to adjust the way you interpret counts based on your specific requirements
    pixel_values = np.zeros((2**n,), dtype=np.float64)
    total_counts = sum(counts.values())

    for outcome, count in counts.items():
        # Remove spaces from the outcome string before conversion
        outcome = outcome.replace(" ", "")
        index = int(outcome, 2)
        pixel_values[index] = count / total_counts  # Normalize the counts

    # Reshape to the original image dimensions
    side_length = int(np.sqrt(target_size))
    pixel_values = (pixel_values * 255).astype(np.uint8)  # Scale to 0-255
    return Image.fromarray(pixel_values.reshape((side_length, side_length)))

def reconstruct_image_from_counts(counts, n):
    # Convert the counts to a numpy array
    pixel_values = np.zeros((2**n,), dtype=np.float64)
    total_counts = sum(counts.values())

    for outcome, count in counts.items():
        outcome = outcome.replace(" ", "")
        # Ensure outcome is within the valid range
        index = int(outcome, 2) % (2**n)
        pixel_values[index] = count

    # Reshape to the original image dimensions
    side_length = int(np.sqrt(target_size))
    pixel_values = (pixel_values * 255 * total_counts / np.max(pixel_values)).astype(np.uint8)
    return Image.fromarray(pixel_values.reshape((side_length, side_length)))

# Reconstruct the image
reconstructed_image = reconstruct_image_from_counts(counts, n)

# Save or display the final image after applying inverse QFT
reconstructed_image.save("reconstructed_image.png")
plt.imshow(reconstructed_image, cmap='gray')
plt.show()
