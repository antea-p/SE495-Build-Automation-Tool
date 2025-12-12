from typing import Any

import api_client
import service

client = api_client.ApiClient()


def get_filtered_builds_3_days_span() -> list[Any] | None:
    # https://arrow.readthedocs.io/en/latest/guide.html
    recent_builds = service.get_build_jobs_between(days_in_past=-3, days_in_future=3)

    return service.filter_and_sort_builds(builds=recent_builds, sort_key='startTime')


def main():
    already_seen_build_ids = set()

    while True:
        filtered_builds = get_filtered_builds_3_days_span()
        if filtered_builds:
            eligible_builds = [build for build in filtered_builds if build['id'] not in already_seen_build_ids]
        else:
            print("No builds in queue, terminating the script...")
            return

        if eligible_builds:
            for build in eligible_builds:
                print(build)
                print("--------------------------------")
            highest_priority_build = eligible_builds[0]  # Because it's already sorted

            try:
                if highest_priority_build['id'] not in already_seen_build_ids:
                    already_seen_build_ids.add(highest_priority_build['id'])
                    # TODO
                    # process_build(highest_priority_build['id'])
                break
            except Exception as error:
                print(
                    f"Build for {highest_priority_build['id']} failed, will skip to next eligible build. Error message: {error}")
                continue


if __name__ == "__main__":
    main()
