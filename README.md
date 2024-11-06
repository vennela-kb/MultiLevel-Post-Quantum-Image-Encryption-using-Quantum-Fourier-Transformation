LWE and AES Image Encryption with Quantum Fourier Transform: Enhanced Post-Quantum Security
**Objectives:**

1. Study the Learning with Errors (LWE) post-quantum encryption algorithm and Quantum Fourier Transform (QFT) for image encryption.
2. Encrypt and decrypt an image using a combined LWE and AES encryption scheme.
3. Observe and analyze the encryption and decryption process.
4. Implement double encryption using AES and LWE, applying QFT for enhanced security against quantum attacks.

**Setup and Requirements:**

1. Python IDE: PyCharm, Jupyter Notebook, or Google Colab.
2. Python Version: Ensure Python 3.6 or above.
3. Libraries: Install pycryptodome (for AES encryption), numpy, pywavelets, pickle, and opencv-python.

**Description of lwe.py**: 
The lwe.py script provides a basic implementation of the Learning with Errors (LWE) algorithm, handling key generation, message encryption, and decryption. It has been adapted to integrate with a quantum-secure image encryption workflow by incorporating QFT, following these key steps:

**Key Generation**: Defines a secret value s and prime q to generate a unique, secure public key using vectors A, B, and error vector e.
**Message Handling**: Reads messages from cipher.txt. If non-integer content is found, the script hashes it to an integer for compatibility.
**Sampling and Encryption**: Encrypts the message by selecting indices from generated vectors to compute values u and v as the encrypted output.
**Decryption**: Decrypts by computing the message bit from u, v, and s.

**Quantum Fourier Transform and AES Encryption Process**: To enhance security, the Quantum Fourier Transform (QFT) is first applied to the image, decomposing it into frequency components. This allows encryption of the low-frequency (LL) coefficient with AES, while the AES key is secured using LWE. The result is a multi-level encryption approach that integrates classical and post-quantum cryptographic techniques for increased security.

1. **QFT Transformation**: Transforms the image, extracting the LL coefficient.
2. **AES Encryption**: Encrypts the LL coefficient with a symmetric AES key, leveraging QFT’s capabilities to retain more information than classical Fourier.
3. **Double Encryption with LWE**: Encrypts the AES key using LWE, adding a robust layer against quantum computing attacks.

**Advantages of the Approach:**

1. **Post-Quantum Security**: LWE and QFT offer resilience against quantum attacks, ensuring long-term data security.
2. **Enhanced Image Security**: Combined AES and LWE encryption prevents unauthorized access, even from quantum adversaries.
3. **High Efficiency**: Despite the complexity, AES and LWE encryption are optimized to minimize computational load.

**Steps to Run the Code**

1. **Set Up QFT** : Use QFT on the image to separate the frequency components, focusing on the LL coefficient.
2. **AES Encryption** : Encrypt the LL coefficient, which contains primary image details, using AES.
3. **LWE Key Encryption**: Encrypt the AES key with LWE to safeguard it against quantum decryption attacks.
4. **Decryption Process**: Sequentially decrypt the AES key using LWE, followed by AES decryption of the LL coefficient.
5. **Validation**: Compare decrypted images with the original, using metrics such as PSNR, SSIM, entropy, and correlation coefficients.

**Benefits of the Combined Approach:**

1. **Robust against Classical and Quantum Attacks**: With QFT, AES, and LWE integration, the framework offers a future-proof encryption method.
2. **Secure Image Transmission**: Suitable for fields like medicine, defense, and finance where sensitive images require high security.
3. **Resilient Data Integrity**: Quantitative metrics confirm that the encryption maintains image quality while enhancing security.
This layered QFT-AES-LWE encryption framework provides a cutting-edge solution for image encryption in the post-quantum era, ensuring security while balancing computational efficiency and image quality preservation.






