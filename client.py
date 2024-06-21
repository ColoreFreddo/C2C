import os
import ed25519

def generate_keys():

    folder_path = "./Keys"

    os.makedirs(folder_path, exist_ok=True)

    seed = os.urandom(32)

    private_key = ed25519.PrivateKey(seed)
    public_key = private_key.public_key

    private_key_path = os.path.join(folder_path, "private.pem")

    public_key_path = os.path.join(folder_path, "public.pem")

    with open(private_key_path, "wb") as f:
        f.write(private_key.to_pem())

    with open(public_key_path, "wb") as f:
        f.write(public_key.to_pem())

    print(f"Keys generated and saved to: {folder_path}")
