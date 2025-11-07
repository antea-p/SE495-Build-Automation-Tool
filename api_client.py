import requests


class ApiClient:

    def __init__(self):
        print("Initializing...")

    def list_build_jobs(self):
        print("Listing build jobs...")
        data = requests.get("http://localhost:3001/api/production_builds")
        for item in data.json():
            print(item)


if __name__ == '__main__':
    client = ApiClient()
    client.list_build_jobs()
