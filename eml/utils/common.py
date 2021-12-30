import os

def file_save(f, save_path):
    save_dirname = os.path.dirname(save_path)
    if not os.path.exists(save_dirname):
        raise FileNotFoundError

    f.save(save_path)
