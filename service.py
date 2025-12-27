from uuid import uuid4

import arrow
import numpy as np
import requests.models
import trimesh

import api_client
from custom_types import Status

client = api_client.ApiClient()


def is_build_eligible(build_: dict) -> bool:
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
        if is_build_eligible(build):
            filtered_builds.append(build)

    filtered_builds.sort(key=lambda x: x.get(sort_key))

    return filtered_builds


def apply_rotation(mesh):
    angle = np.radians(-180)
    direction = [0, 0, 1]
    center = mesh.centroid

    return trimesh.transformations.rotation_matrix(angle, direction, center)


def create_combined_stl_file(result):
    # https://github.com/mikedh/trimesh/issues/365
    # https://stackoverflow.com/questions/72561243/rotating-trimesh-mesh-plane-object
    for (i, print_run) in enumerate(result):
        print(print_run)
        uuid_ = uuid4()
        scene = trimesh.Scene()
        meshes = []

        for (j, position) in enumerate(print_run):
            print(f"Positon {j}: {position}")
            mesh = trimesh.load_mesh(position.filename)
            meshes.append(mesh)

            target_position = np.array([0, 0, 0])
            mesh.apply_translation(target_position - mesh.centroid)

            mesh.apply_translation([position.x, -position.y, 0])
            mesh.apply_transform(apply_rotation(mesh))

            scene.add_geometry(mesh)
            # scene.export(f"incomplete-printrun-{uuid_}-{i}_{j}.stl")
            # combined_mesh.export(f"incomplete-printrun-{uuid_}-{j}.stl")

        combined_mesh = trimesh.util.concatenate([meshes])

        print(f"Created combined stl file for print_run {i}")
        scene.export(f"printrun-{uuid_}.stl")
    return combined_mesh
