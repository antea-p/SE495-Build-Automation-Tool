from typing import Optional

import requests

from custom_types import Status


class ApiClient:

    def __init__(self, base_url: str = "http://localhost:3001"):
        print("Initializing...")
        self.BASE_URL = base_url

    def get_build_jobs(self, date1: Optional[str] = None, date2: Optional[str] = None, status: Optional[Status] = None):
        url = f"{self.BASE_URL}/api/production_builds"
        if date1 and date2:
            url += f"?startTime_gte={date1}&startTime_lte={date2}"
        if status:
            url += f"&status={status.name}"

        data = requests.get(url)
        return data

    def get_build_details(self, build_id: str):
        return requests.get(f"{self.BASE_URL}/api/production_builds/{build_id}")

    def update_status(self, build_id: str, new_status: Status):
        body = {"status": new_status.name}
        return requests.patch(f"{self.BASE_URL}/api/production_builds/{build_id}", json=body)

    def upload_slice_file(self, build_id: str, file_path: str):
        payload = {"file": file_path}

        return requests.post(f"{self.BASE_URL}/api/production_builds/{build_id}/slice", files=payload)

    def download_slice_file(self, file_name: str):
        return requests.get(f"{self.BASE_URL}/files/slices/{file_name}")

    def download_part_file(self, part_id: str, file_name: str):
        return requests.get(f"{self.BASE_URL}/files/parts/{part_id}/{file_name}")
