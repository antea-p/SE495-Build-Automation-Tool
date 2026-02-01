from pathlib import Path
from typing import Any

import api_client
import chitubox as cb
import service

client = api_client.ApiClient()
chitubox = cb.Chitubox()


def get_filtered_builds_3_days_span() -> list[Any] | None:
    # https://arrow.readthedocs.io/en/latest/guide.html
    recent_builds = service.get_build_jobs_between(days_in_past=-3, days_in_future=3)

    return service.filter_and_sort_builds(builds=recent_builds, sort_key='startTime')


def main():
    already_seen_build_ids = set()

    filtered_builds = get_filtered_builds_3_days_span()
    if filtered_builds:
        remaining_builds = [build for build in filtered_builds if build['id'] not in already_seen_build_ids]
    else:
        print("No builds in queue, terminating the script...")
        return

    while remaining_builds:
        highest_priority_build = remaining_builds[0]  # Because it's already sorted
        highest_priority_id = highest_priority_build['id']

        try:
            # if highest_priority_id not in already_seen_build_ids:
            already_seen_build_ids.add(highest_priority_id)
            filenames = service.process_build(highest_priority_id)
            for filename in filenames:
                chitubox.perform_automation(Path(filename))
            remaining_builds.remove(highest_priority_build)
        except Exception as error:
            print(
                f"Build for {highest_priority_id} failed, will skip to next eligible build. Error message: {error}")
            continue

    chitubox.show_message("Completed the work. Please verify there were no errors.")


if __name__ == "__main__":
    main()
