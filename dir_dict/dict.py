import collections
import os
import shutil


class DirDict(collections.MutableMapping):
    def __init__(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if not os.path.isdir(folder_path):
            raise ValueError("Not a directory.")
        self._path = folder_path
        super().__init__()

    def __getitem__(self, key):
        all_path = os.path.join(self._path, key)
        if os.path.isdir(all_path):
            return DirDict(all_path)
        elif os.path.isfile(all_path):
            with open(all_path, "r") as f:
                data = f.read()
            return data
        else:
            raise KeyError("No such directory or file")

    def __setitem__(self, key, value):
        all_path = os.path.join(self._path, key)

        if os.path.isdir(all_path):
            shutil.rmtree(all_path)
        elif os.path.isfile(all_path):
            os.remove(all_path)

        if isinstance(value, type(self)):
            shutil.copytree(value._path, all_path)
        else:
            with open(all_path, "w") as f:
                f.write(value)

    def __delitem__(self, key):
        all_path = os.path.join(self._path, key)
        if os.path.isdir(all_path):
            shutil.rmtree(all_path)
        elif os.path.isfile(all_path):
            os.remove(all_path)
        else:
            raise KeyError("No such directory or file")

    def __iter__(self):
        return iter(os.listdir(self._path))

    def __len__(self):
        return len(os.listdir(self._path))