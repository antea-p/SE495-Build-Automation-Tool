import json
from unittest.mock import patch, PropertyMock

import numpy as np
import pytest
import responses
from trimesh.base import Trimesh

import service

BASE_URL = "http://localhost:3001"


# https://stackoverflow.com/a/39401087
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
        "status": "NEW",
        "slicePath": "/files/slices/bld_001.pwmb",
        "batches": [
            {
                "quantity": 3,
                "partId": "5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b",
                "itemId": "2025122101-0001",
                "fileTypes": [
                    "ORIGINAL",
                    "PRE_SUPPORTED"
                ]
            }
        ]
    }


class TestService:

    def test_build_job_is_eligible(self, bld_001):
        assert service._is_build_eligible(bld_001) == True

    def test_build_job_is_not_eligible_if_status_is_not_new(self, bld_001):
        bld_001['status'] = 'BUILT'
        assert service._is_build_eligible(bld_001) == False

    def test_build_job_is_not_eligible_if_batches_dont_exist(self, bld_001):
        bld_001['batches'] = []
        assert service._is_build_eligible(bld_001) == False

        del bld_001['batches']
        assert service._is_build_eligible(bld_001) == False

    def test_build_job_is_not_eligible_if_batches_count_is_zero(self, bld_001):
        bld_001['batches'][0]['quantity'] = 0
        assert service._is_build_eligible(bld_001) == False

    def test_get_build_jobs_returns_nonempty_result_within_date_range(self, mocker, bld_001, build_jobs_list):
        # one result
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = bld_001
        mocker.patch("requests.get", return_value=mock_response)

        actual1 = service.get_build_jobs_between(-3, 1)
        assert actual1.json() == bld_001

        # multiple results
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = build_jobs_list[2:6]
        mocker.patch("requests.get", return_value=mock_response)

        actual2 = service.get_build_jobs_between(-2, 5)
        assert actual2.json() == build_jobs_list[2:6]

    @responses.activate
    def test_get_build_jobs_returns_empty_json_if_no_matches_exist_within_date_range(self, mocker):
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = []
        mocker.patch("requests.get", return_value=mock_response)

        actual = service.get_build_jobs_between(-5, 5)
        assert actual.json() == []

    def test_get_build_jobs_when_days_equal_zero(self, mocker, build_jobs_list):
        # days_in_future equals 0
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = build_jobs_list[0:5]
        mocker.patch("requests.get", return_value=mock_response)
        actual1 = service.get_build_jobs_between(-2, 0)
        assert actual1.json() == build_jobs_list[0:5]

        # both days_in_past and days_in_future equal 0
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = build_jobs_list[3:5]
        mocker.patch("requests.get", return_value=mock_response)
        actual2 = service.get_build_jobs_between(0, 0)
        assert actual2.json() == build_jobs_list[3:5]

        # days_in_past equals 0
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = build_jobs_list[3:]
        mocker.patch("requests.get", return_value=mock_response)
        actual3 = service.get_build_jobs_between(0, 5)
        assert actual3.json() == build_jobs_list[3:]

    def test_get_build_jobs_when_days_in_past_greater_than_days_in_future(self, bld_001):
        with pytest.raises(ValueError) as e_info:
            service.get_build_jobs_between(5, 1)

    def test_get_build_jobs_when_days_in_future_negative(self, bld_001):
        with pytest.raises(ValueError) as e_info:
            service.get_build_jobs_between(5, -5)

    def test_filter_and_sort_builds_returns_nonempty_sorted_list(self, mocker, build_jobs_list):
        # creating a sublist of build jobs that have pre-supported files
        build_jobs = build_jobs_list[1:5]

        # setting their attributes
        build_jobs[0]["startTime"] = "2026-06-01T11:00:00Z"
        build_jobs[0]["endTime"] = "2026-06-01T12:00:00Z"
        build_jobs[0]["status"] = "NEW"

        build_jobs[1]["startTime"] = "2026-02-01T13:00:00Z"
        build_jobs[1]["endTime"] = "2026-02-01T13:45:00Z"
        build_jobs[1]["status"] = "NEW"

        build_jobs[2]["startTime"] = "2026-04-01T14:00:00Z"
        build_jobs[2]["endTime"] = "2026-04-01T16:30:00Z"
        build_jobs[2]["status"] = "NEW"

        build_jobs[3]["startTime"] = "2026-02-01T13:00:00Z"
        build_jobs[3]["endTime"] = "2026-02-01T13:45:00Z"
        build_jobs[3]["status"] = "NEW"

        # mocking
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = build_jobs

        # invocations and assertions
        expected = sorted(build_jobs, key=lambda build_job: build_job["startTime"])

        actual = service.filter_and_sort_builds(mock_response, sort_key="startTime")
        assert actual == expected

    def test_filter_and_sort_builds_returns_empty_list_if_no_matches_exist(self, mocker, bld_001):
        bld_001["status"] = "FINISHED"

        mock_response = mocker.MagicMock()
        mock_response.json.return_value = [bld_001]  # not bld_001, because json returns list of dicts
        actual = service.filter_and_sort_builds(mock_response, sort_key="startTime")
        assert actual == []

    def test_filter_and_sort_builds_sorts_throws_exception_if_sort_key_invalid(self, mocker, build_jobs_list):
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = build_jobs_list

        with pytest.raises(ValueError) as e_info:
            service.filter_and_sort_builds(mock_response, sort_key="aaaaaa")

    def test_download_part_files_from_build_job_with_single_batch(self, mocker, bld_001):
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = bld_001
        mocker.patch("service.client.get_build_details", return_value=mock_response)

        mock_response_2 = mocker.MagicMock()
        mock_response_2.body.return_value = "# OBJ placeholder"
        mock_response_2.content.return_value = "# OBJ placeholder"
        mocker.patch("service.client.download_part_file", return_value=mock_response_2)

        mock_file = mocker.mock_open()
        mocker.patch("builtins.open", mock_file)

        with patch.object(Trimesh, "extents", new_callable=PropertyMock) as extents_mock:
            mock_mesh = mocker.MagicMock()
            p = PropertyMock(return_value=np.array([5, 2.5, 3]))
            type(mock_mesh).extents = p

            mocker.patch("trimesh.load", return_value=mock_mesh)
            mocker.patch("numpy.ptp", return_value=np.array([5, 2.5, 3]))

            # extents_mock.return_value = np.array([5, 2.5, 3])

            actual = service.download_part_files("bld_001")
            mock_file.assert_called_once_with("bld_001-5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b.stl", "wb")

            assert len(actual) == 3
            assert actual[0].filename == "bld_001-5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b.stl"
            assert actual[0].w == 3
            assert actual[0].l == 5
            assert all(box == actual[0] for box in actual)

    def test_download_part_files_from_build_job_with_multiple_batches(self, mocker, bld_001):
        bld_001["batches"].append({
            "quantity": 1,
            "partId": "testPartId",
            "itemId": "testItemId",
            "fileTypes": [
                "ORIGINAL",
                "PRE_SUPPORTED"
            ]
        })

        mock_response = mocker.MagicMock()
        mock_response.json.return_value = bld_001
        mocker.patch("service.client.get_build_details", return_value=mock_response)

        mock_response_2 = mocker.MagicMock()
        mock_response_2.body.return_value = "# OBJ placeholder"
        mock_response_2.content.return_value = "# OBJ placeholder"
        mocker.patch("service.client.download_part_file", return_value=mock_response_2)

        mock_file = mocker.mock_open()
        mocker.patch("builtins.open", mock_file)

        with patch.object(Trimesh, "extents", new_callable=PropertyMock) as extents_mock:
            mock_mesh = mocker.MagicMock()
            p = PropertyMock(return_value=np.array([5, 2.5, 3]))
            type(mock_mesh).extents = p

            mocker.patch("trimesh.load", return_value=mock_mesh)
            mocker.patch("numpy.ptp", return_value=np.array([5, 2.5, 3]))

            # extents_mock.return_value = np.array([5, 2.5, 3])

            actual = service.download_part_files("bld_001")
            assert len(actual) == 4
            assert actual[0].filename == "bld_001-5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b.stl"
            assert actual[3].filename == "bld_001-testPartId.stl"
