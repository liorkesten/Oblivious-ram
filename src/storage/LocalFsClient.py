from src.storage.IStorageClient import IStorageClient
import os


class LocalFsClient(IStorageClient):
    def __init__(self, working_dir="/"):
        working_dir = os.path.join(working_dir, "buckets")
        # create dir if not exists
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        self.working_dir = working_dir

    def read(self, filename) -> bytes:
        # read the file and return the context as string
        full_file_path = os.path.join(self.working_dir, filename)
        with open(full_file_path, "rb") as f:
            return f.read()

    def write(self, filename: str, data: bytes) -> bytes:
        # write the data to the file
        full_file_path = os.path.join(self.working_dir, filename)
        # print(f"writing to {full_file_path}. size_of_data: {len(data)}")
        with open(full_file_path, "wb+") as f:
            f.write(data)
            return data

        return None
