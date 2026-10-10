from os import path, makedirs

filepath = path.join('data', 'data.data')


def create_dir():
    makedirs(path.join('data'), exist_ok=True)


def load_high_score():
    if path.exists(filepath):
        with open(filepath, 'rb') as f:
            data = f.read()
            data = data.decode()
            return int(data)
    else:
        with open(filepath, 'wb') as f:
            f.write('0'.encode())
            return 0


def save_high_score(high_score):
    with open(filepath, 'wb') as f:
        f.write((str(high_score)).encode())
