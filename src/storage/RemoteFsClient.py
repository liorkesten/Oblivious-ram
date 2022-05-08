from src.storage.IStorageClient import IStorageClient
import os
import requests


class RemoteFsClient(IStorageClient):
    def __init__(self, host: str = "localhost", port: int = "8080"):
        # create dir if not exists
        self.url = f"http://{host}:{port}"
        self.session = requests.Session()

    def read(self, filename: str) -> bytes:
        # read the file and return the context as string
        read_url = f"{self.url}/read"
        response = self.session.get(url=read_url, params={"filename": filename})
        return response.content

    def write(self, filename: str, data: bytes) -> bytes:
        # read the file and return the context as string
        read_url = f"{self.url}/write"
        response = self.session.post(url=read_url, params={"filename": filename}, data=data, headers={"Content-Type": "text/plain"})
        return response.content

    def delete(self, filename: str) -> bool:
        # delete the file and return the context as string
        read_url = f"{self.url}/delete"
        response = self.session.delete(url=read_url, params={"filename": filename})
        return response.status_code == 200
