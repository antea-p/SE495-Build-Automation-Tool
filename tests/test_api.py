import pytest
import requests
import responses


class TestApi:

    @responses.activate
    def test_get_build_jobs(self):



    @responses.activate
    def test_get_build_jobs_returns_empty_list_if_no_build_jobs_exist(self):
        pass


    @responses.activate
    def test_get_build_details(self):
        pass


    @responses.activate
    def test_get_build_details_invalid_build_job(self):
        pass


    @responses.activate
    def test_update_status_with_valid_status(self):
        pass


    @responses.activate
    def test_update_status_with_invalid_status(self):
        pass


    @responses.activate
    def test_upload_slice_file(self):
        pass


    @responses.activate
    def test_upload_slice_file_invalid_build_id(self):
        pass


    @responses.activate
    def test_upload_slice_file_invalid_path(self):
        pass


    @responses.activate
    def test_download_slice_file(self):
        pass


    @responses.activate
    def test_download_slice_file_invalid_filename(self):
        pass


    @responses.activate
    def test_download_part_file(self):
        pass


    @responses.activate
    def test_download_part_file_invalid_part_id(self):
        pass


    @responses.activate
    def test_download_part_file_invalid_filename(self):
        pass
