from enum import Enum

import requests


class Status(Enum):
    NEW = 1
    BUILT = 2
    PRODUCING = 3
    FINISHED = 4


class ApiClient:

    def __init__(self):
        print("Initializing...")

    def list_build_jobs(self):
        print("Listing build jobs...")
        data = requests.get("http://localhost:3001/api/production_builds")
        for item in data.json():
            print(item)

    def filter_build_jobs_by_date(self, date1, date2, status=None):
        print("Filtering build jobs by date...")
        if status:
            data = requests.get(
                f"http://localhost:3001/api/production_builds?startTime_gte={date1}&startTime_lte={date2}&status={status.name}")
        else:
            data = requests.get(
                f"http://localhost:3001/api/production_builds?startTime_gte={date1}&startTime_lte={date2}")
        for item in data.json():
            print(item)


if __name__ == '__main__':
    client = ApiClient()
    # client.list_build_jobs()
    client.filter_build_jobs_by_date('2025-10-24T09:00:00Z', '2025-10-24T13:30:00Z')
    client.filter_build_jobs_by_date('2025-10-24T09:00:00Z', '2025-10-29T13:30:00Z', Status.PRODUCING)
