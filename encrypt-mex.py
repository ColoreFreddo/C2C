import ed25519

def generate_key_pair():
    # Genera una coppia di chiavi Ed25519
    key = ed25519.SigningKey.generate()
    public_key = key.get_verifying_key()
    private_key = key.to_ascii(encoding="hex")
    return public_key, private_key

def encrypt_message(message, public_key):
    # Cifra il messaggio utilizzando la chiave pubblica fornita
    encrypted_message = public_key.encrypt(message.encode())
    return encrypted_message

def main():
    # Genera una coppia di chiavi Ed25519
    public_key, private_key = generate_key_pair()

    # Messaggio da cifrare
    message = "Questo è un messaggio segreto da cifrare con Ed25519!"

    # Cifra il messaggio utilizzando la chiave pubblica
    encrypted_message = encrypt_message(message, public_key)
    print("Messaggio cifrato:", encrypted_message)

if __name__ == "__main__":
    main()
