import os
import ed25519

def generate_keys():

    folder_name = "Keys"

    current_dir = os.getcwd()

    folder_path = os.path.join(current_dir, folder_name)

    try:
        os.makedirs(folder_path)
    except OSError as e:
        if not os.path.isdir(folder_path):
            raise  # Re-raise if it's not a directory permission issue
        else:
            print(f"Folder '{folder_name}' already exists. Keys will be saved there.")

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