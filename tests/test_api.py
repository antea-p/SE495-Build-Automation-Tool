import json

import pytest
import responses

from api_client import ApiClient
from custom_types import Status

BASE_URL = "http://localhost:3001"


# https://stackoverflow.com/a/39401087
@pytest.fixture(scope="class")
def api_client():
    yield ApiClient(BASE_URL)


@pytest.fixture()
def build_jobs_list():
    with open('build_jobs.json', 'r') as file:
        example_build_jobs = json.load(file)
    yield example_build_jobs


@pytest.fixture()
def bld_001(build_jobs_list):
    yield {
        "id": "bld_001",
        "startTime": "2025-10-24T09:00:00Z",
        "endTime": "2025-10-24T12:00:00Z",
        "status": "BUILT",
        "slicePath": "/files/slices/bld_001.pwmb",
        "batches": []
    }


@pytest.fixture()
def bld_001_slice():
    return {
        "id": "bld_001",
        "slicePath": "/files/slices/bld_001.pwmb",
        "status": "BUILT"
    }


class TestApi:
    @responses.activate
    def test_get_build_jobs(self, api_client, build_jobs_list):
        """Verify that expected JSON response is returned if at least one build job exists"""
        with responses.RequestsMock() as response_mocks:
            response_mocks.add(responses.GET, f'{BASE_URL}/api/production_builds', json=build_jobs_list, status=200)

            resp = api_client.get_build_jobs()

            assert resp.json() == build_jobs_list

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/api/production_builds'
            assert response_mocks.calls[0].request.method == 'GET'

    @responses.activate
    def test_get_build_jobs_returns_empty_list_if_no_build_jobs_exist(self, api_client):
        """Verify that empty response is returned if at there are no build jobs"""
        with responses.RequestsMock() as response_mocks:
            response_mocks.add(responses.GET, f'{BASE_URL}/api/production_builds', json=[], status=200)

            resp = api_client.get_build_jobs()

            assert resp.json() == []

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/api/production_builds'
            assert response_mocks.calls[0].request.method == 'GET'

    @responses.activate
    def test_get_build_details(self, api_client, bld_001):
        """Verify that expected JSON response is returned if build job exists"""
        with responses.RequestsMock() as response_mocks:
            response_mocks.add(responses.GET, f'{BASE_URL}/api/production_builds/bld_001', json=bld_001,
                               status=200)

            resp = api_client.get_build_details('bld_001')

            assert resp.json() == bld_001

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/api/production_builds/bld_001'
            assert response_mocks.calls[0].request.method == 'GET'

    @responses.activate
    def test_get_build_details_invalid_build_job(self, api_client):
        """Verify that empty 404 response is returned if build job is invalid or doesn't exist"""
        with responses.RequestsMock() as response_mocks:
            response_mocks.add(responses.GET, f'{BASE_URL}/api/production_builds/INVALID_BUILD_JOB', json=[],
                               status=404)

            resp = api_client.get_build_details('INVALID_BUILD_JOB')

            assert resp.json() == []

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/api/production_builds/INVALID_BUILD_JOB'
            assert response_mocks.calls[0].request.method == 'GET'

    @responses.activate
    def test_update_status_with_valid_status(self, api_client, bld_001):
        """Verify that existing build job's status is updated successfully"""
        with responses.RequestsMock() as response_mocks:
            bld_001['status'] = "NEW"  # updates existing bld_001 status from "BUILT" to "NEW"
            response_mocks.add(responses.PATCH, f'{BASE_URL}/api/production_builds/bld_001', json=bld_001,
                               status=200)

            resp = api_client.update_status('bld_001', Status.NEW)

            assert resp.json() == bld_001

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/api/production_builds/bld_001'
            assert response_mocks.calls[0].request.method == 'PATCH'

    @responses.activate
    def test_upload_slice_file(self, api_client, bld_001_slice):
        with responses.RequestsMock() as response_mocks:
            response_mocks.add(responses.POST, f'{BASE_URL}/api/production_builds/bld_001/slice', json=bld_001_slice,
                               status=200)

            resp = api_client.upload_slice_file('bld_001', "slice_bld_001.pwmb")

            assert resp.json() == bld_001_slice

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/api/production_builds/bld_001/slice'
            assert response_mocks.calls[0].request.method == 'POST'

    @responses.activate
    def test_upload_slice_file_invalid_build_id(self, api_client):
        with responses.RequestsMock() as response_mocks:
            response_json = {
                "error": "Build not found"
            }
            response_mocks.add(responses.POST, f'{BASE_URL}/api/production_builds/nonexistent_build_id/slice',
                               json=response_json,
                               status=404)

            resp = api_client.upload_slice_file('nonexistent_build_id', "slice_bld_001.pwmb")

            assert resp.json() == response_json

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/api/production_builds/nonexistent_build_id/slice'
            assert response_mocks.calls[0].request.method == 'POST'

    @responses.activate
    def test_download_slice_file(self, api_client):
        with responses.RequestsMock() as response_mocks:
            return_body = "PWMB test"
            response_mocks.add(responses.GET, f'{BASE_URL}/files/slices/bld_001.pwmb', body=return_body,
                               status=200)

            resp = api_client.download_slice_file('bld_001.pwmb')

            assert resp.text == return_body

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/files/slices/bld_001.pwmb'
            assert response_mocks.calls[0].request.method == 'GET'

    @responses.activate
    def test_download_slice_file_invalid_filename(self, api_client):
        with responses.RequestsMock() as response_mocks:
            return_body = "Cannot GET /files/slices/INVALID_FILENAME.pwmb"
            response_mocks.add(responses.GET, f'{BASE_URL}/files/slices/INVALID_FILENAME.pwmb', body=return_body,
                               status=404)

            resp = api_client.download_slice_file('INVALID_FILENAME.pwmb')

            assert resp.text == return_body

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/files/slices/INVALID_FILENAME.pwmb'
            assert response_mocks.calls[0].request.method == 'GET'

    @responses.activate
    def test_download_part_file(self, api_client):
        with responses.RequestsMock() as response_mocks:
            return_body = "# OBJ placeholder"
            response_mocks.add(responses.GET, f'{BASE_URL}/files/parts/1234/FIXED.obj',
                               body=return_body,
                               status=200)

            resp = api_client.download_part_file('1234', 'FIXED.obj')

            assert resp.text == return_body

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/files/parts/1234/FIXED.obj'
            assert response_mocks.calls[0].request.method == 'GET'

    @responses.activate
    def test_download_part_file_invalid_part_id(self, api_client):
        with responses.RequestsMock() as response_mocks:
            return_body = "Cannot GET /files/parts/INVALID_PART/FIXED.obj"
            response_mocks.add(responses.GET, f'{BASE_URL}/files/parts/INVALID_PART/FIXED.obj', body=return_body,
                               status=404)

            resp = api_client.download_part_file('INVALID_PART', 'FIXED.obj')

            assert resp.text == return_body
            assert resp.status_code == 404

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/files/parts/INVALID_PART/FIXED.obj'
            assert response_mocks.calls[0].request.method == 'GET'

    @responses.activate
    def test_download_part_file_invalid_filename(self, api_client):
        with responses.RequestsMock() as response_mocks:
            return_body = "Cannot GET /files/parts/1234/INVALID_FILENAME.obj"
            response_mocks.add(responses.GET, f'{BASE_URL}/files/parts/1234/INVALID_FILENAME.obj', body=return_body,
                               status=404)

            resp = api_client.download_part_file('1234', 'INVALID_FILENAME.obj')

            assert resp.text == return_body
            assert resp.status_code == 404

            assert len(response_mocks.calls) == 1
            assert response_mocks.calls[0].request.url == f'{BASE_URL}/files/parts/1234/INVALID_FILENAME.obj'
            assert response_mocks.calls[0].request.method == 'GET'
