import os
import uuid

import requests


def upload_documentation(path, docs_key):
    url = os.environ.get("FOLGE_URL", "https://folge.io")
    token = os.environ.get("FOLGE_TOKEN")

    revision = str(uuid.uuid4())
    headers = {"Authorization": "Bearer %s" % token}
    base_path = "%s/api/documentation/%s/%s" % (url, docs_key, revision)

    response = requests.post("%s/create" % base_path, headers=headers)
    response.raise_for_status()

    for local_path, remote_path in iterate_files(path):
        with open(local_path, "rb") as fh:
            print(local_path, end=" ")
            response = requests.post(
                "%s/upload" % base_path,
                data={"filename": remote_path},
                files={"content": fh},
                headers=headers,
            )
            response.raise_for_status()
            print("Done")

    response = requests.post("%s/complete" % base_path, headers=headers)
    response.raise_for_status()


def iterate_files(path):
    path = os.path.realpath(path)
    for root, dirs, files in os.walk(path):
        common = os.path.commonpath([path, root])
        subpath = root[len(common) + 1 :]

        for name in files:
            yield os.path.join(root, name), os.path.join(subpath, name)
