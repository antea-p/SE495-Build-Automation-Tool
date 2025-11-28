import time

import arrow

import api_client
from custom_types import Status

client = api_client.ApiClient()


def get_filtered_builds_3_days_span() -> list[dict]:
    def is_build_eligible(build_) -> bool:
        if build_.get('status') == Status.NEW:
            return False

        if 'batches' not in build_:
            return False

        batch_unit_count = build_.get('batches').get('batchUnitCount', 0)
        if batch_unit_count == 0:
            return False

        if 'slicePath' not in build_:
            return False

        return True

    # https://arrow.readthedocs.io/en/latest/guide.html
    now = arrow.now()
    three_days_ago = now.shift(days=-3)
    in_three_days = now.shift(days=3)

    recent_builds = client.get_build_jobs(three_days_ago.format('YYYY-MM-DD[T]HH:mm:ss[Z]'),
                                          in_three_days.format('YYYY-MM-DD[T]HH:mm:ss[Z]'))

    filtered_builds = []

    for build in recent_builds:
        if is_build_eligible(build):
            filtered_builds.append(build)

    filtered_builds.sort(key=lambda x: x.get('startTime'))

    return filtered_builds


# Close to main so it's colocated to functions that use it
already_seen_build_ids = set()


def main():
    while True:
        eligible_builds = get_filtered_builds_3_days_span()
        eligible_builds = [build for build in eligible_builds if build['id'] not in already_seen_build_ids]
        if not eligible_builds:
            print("No builds in queue, will sleep for 5 minutes. (－ω－) zzZ")
            time.sleep(5 * 60)
            continue
        for build in eligible_builds:
            print(build)
            print("--------------------------------")
        highest_priority_build = eligible_builds[0]  # Because it's already sorted

        try:
            already_seen_build_ids.add(highest_priority_build['id'])
            # TODO
            # process_build(highest_priority_build['id'])
        except Exception as error:
            print(
                f"Build for {highest_priority_build['id']} failed, will skip to next eligible build. Error message: {error}")
            continue


if __name__ == "__main__":
    main()
