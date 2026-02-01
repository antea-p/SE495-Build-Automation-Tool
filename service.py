from math import ceil
from uuid import uuid4

import arrow
import numpy as np
import requests.models
import trimesh

import api_client
from custom_types import Status, Box
from layout import bin_packing

client = api_client.ApiClient()


def _is_build_eligible(build_: dict) -> bool:
    if build_.get('status') != Status.NEW.name:
        return False

    if 'slicePath' not in build_:
        return False

    if 'batches' not in build_ or len(build_.get('batches')) == 0:
        return False

    batches = build_.get('batches')
    for batch in batches:
        if batch.get('quantity') == 0:
            return False

    print(f"Found eligible build {build_['id']}")
    return True


def get_build_jobs_between(days_in_past: int, days_in_future: int):
    now = arrow.now()
    n_days_ago = now.shift(days=days_in_past)
    in_n_days = now.shift(days=days_in_future)

    return client.get_build_jobs(n_days_ago.format('YYYY-MM-DD[T]HH:mm:ss[Z]'),
                                 in_n_days.format('YYYY-MM-DD[T]HH:mm:ss[Z]'))


def filter_and_sort_builds(builds: requests.models.Response, sort_key: str):
    filtered_builds = []

    if not builds.json():
        return None

    for build in builds.json():
        if _is_build_eligible(build):
            filtered_builds.append(build)

    filtered_builds.sort(key=lambda x: x.get(sort_key))

    return filtered_builds


def download_part_files(build_id: str):
    batches = client.get_build_details(build_id=build_id).json().get('batches')
    all_parts = []
    for batch in batches:
        download = client.download_part_file(batch.get('partId'), file_name='PRE_SUPPORTED.stl')
        quantity = batch.get('quantity')
        filename = f'{build_id}-{batch.get('partId')}.stl'
        with open(filename, 'wb') as f:
            f.write(download.content)

            mesh = trimesh.load(filename)
            x, y, z = mesh.bounding_box.extents
            for _ in range(quantity):
                all_parts.append(Box(w=ceil(y), l=ceil(x), h=ceil(z), filename=filename))
            print(f"Downloaded {filename} with dimensions (width x length): {y} mm x {x} mm")
    return all_parts


def process_build(build_id: str):
    print(f"Processing {build_id}")
    to_layout = download_part_files(build_id)

    remaining_parts = True
    layouts = []
    result = bin_packing(to_layout)

    while remaining_parts:
        layout_ = result.get('occupied')
        unfit_boxes = result.get('unfit_boxes')
        layouts.append(layout_)
        if not unfit_boxes:
            remaining_parts = False
        else:
            result = bin_packing(unfit_boxes)

    filenames = create_combined_stl_file(build_id, layouts)
    return filenames


def apply_rotation(mesh, degrees):
    angle = np.radians(degrees)
    direction = [0, 0, 1]
    center = mesh.bounds.mean(axis=0)  # center of boundingbox

    return trimesh.transformations.rotation_matrix(angle, direction, center)


def create_combined_stl_file(build_id: str, result: dict):
    # https://github.com/mikedh/trimesh/issues/365
    # https://stackoverflow.com/questions/72561243/rotating-trimesh-mesh-plane-object
    filenames = []
    for (i, print_run) in enumerate(result):
        uuid_ = uuid4()
        meshes = []
        scene = trimesh.Scene()

        for (j, position) in enumerate(print_run):
            mesh = trimesh.load_mesh(position.filename)

            mesh.apply_transform(apply_rotation(mesh, 90))
            bounds = mesh.bounds
            min_x = bounds[0, 0]
            min_y = bounds[0, 1]
            min_z = bounds[0, 2]
            mesh.apply_translation((-min_x, -min_y, -min_z))
            mesh.apply_translation([position.x, position.y, 0])

            meshes.append(mesh)

            scene.add_geometry(mesh)
            bounds = mesh.bounds  # [[minx, miny, minz], [maxx, maxy, maxz]]
            min_corner, max_corner = bounds

            x, y, z = min_corner
            w, h, d = max_corner - min_corner

            print(x, y, z, w, h, d)
            print(scene.geometry_identifiers)

        scene.apply_transform(apply_rotation(scene, 90))
        export_filename = f"printrun-{build_id}-batch-{i}-{arrow.now().int_timestamp}.stl"
        print(f"Exporting {export_filename}")
        filenames.append(export_filename)
        scene.export(export_filename)

    return filenames
