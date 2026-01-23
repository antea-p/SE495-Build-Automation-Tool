from math import ceil
from pathlib import Path
from typing import Any

import trimesh

import api_client
import chitubox as cb
import service
from layout import Box, bin_packing

client = api_client.ApiClient()
chitubox = cb.Chitubox()


def get_filtered_builds_3_days_span() -> list[Any] | None:
    # https://arrow.readthedocs.io/en/latest/guide.html
    recent_builds = service.get_build_jobs_between(days_in_past=-3, days_in_future=3)

    return service.filter_and_sort_builds(builds=recent_builds, sort_key='startTime')


def process_build(build_id: str):
    print(f"Processing {build_id}")
    batches = client.get_build_details(build_id=build_id).json().get('batches')
    to_layout = []
    for batch in batches:
        download = client.download_part_file(batch.get('partId'), file_name='PRE_SUPPORTED.stl')
        quantity = batch.get('quantity')
        filename = f'{build_id}-{batch.get('partId')}.stl'
        with open(filename, 'wb') as f:
            f.write(download.content)

            mesh = trimesh.load(filename)
            x, y, z = mesh.bounding_box.extents
            for _ in range(quantity):
                to_layout.append(Box(w=ceil(y), l=ceil(x), h=ceil(z), filename=filename))
            print(f"Downloaded {filename} with dimensions (width x length): {y} mm x {x} mm")

    print(f"Build {build_id} has {len(to_layout)} boxes to layout.")
    # print("To layout: ", to_layout)

    remaining_parts = True
    layouts = []
    result = bin_packing(to_layout)

    while remaining_parts:
        layout_ = result[0]
        unfit_boxes = result[2]
        layouts.append(layout_)
        if not unfit_boxes:
            remaining_parts = False
        else:
            result = bin_packing(unfit_boxes)

    print(f"Build {build_id} will require {len(layouts)} print runs")
    for layout in layouts:
        print(layout, sep='\n')
    print("---------------------------")

    return layouts


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


if __name__ == "__main__":
    main()
