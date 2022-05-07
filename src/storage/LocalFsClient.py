from src.storage.IStorageClient import IStorageClient
import os


class LocalFsClient(IStorageClient):
    def __init__(self, working_dir="/"):
        working_dir = os.path.join(working_dir, "buckets")
        # create dir if not exists
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        self.working_dir = working_dir

    def read(self, filename) -> str:
        # read the file and return the context as string
        full_file_path = os.path.join(self.working_dir, filename)
        with open(full_file_path, "r") as f:
            return f.read()

    def write(self, filename, data) -> str:
        # write the data to the file
        full_file_path = os.path.join(self.working_dir, filename)
        with open(full_file_path, "w+") as f:
            f.write(data)
            return "File written successfully"