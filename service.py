from datetime import datetime
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


def center_of_bounding_box(mesh):
    return mesh.bounds.mean(axis=0)


def apply_rotation(obj, degrees):
    angle = np.radians(degrees)
    direction = [0, 0, 1]
    center = center_of_bounding_box(obj)

    return trimesh.transformations.rotation_matrix(angle, direction, center)


def create_combined_stl_file(result):
    # https://github.com/mikedh/trimesh/issues/365
    # https://stackoverflow.com/questions/72561243/rotating-trimesh-mesh-plane-object
    for (i, print_run) in enumerate(result):
        uuid_ = uuid4()
        meshes = []
        scene = trimesh.Scene()
        origin = np.array([0, 0, 0])

        for (j, position) in enumerate(print_run):
            mesh = trimesh.load_mesh(position.filename)

            mesh.apply_transform(apply_rotation(mesh, 90))
            mesh.apply_translation(origin - center_of_bounding_box(mesh))
            mesh.apply_translation([position.x, -position.y, 0])

            meshes.append(mesh)

            scene.add_geometry(mesh)
            print(scene.geometry_identifiers)
            print("Meshes so far: ", len(meshes))

            now = datetime.now()
            formatted = now.strftime('%Y-%m-%d-%H_%M_%S')
            scene.export(f"incomplete-printrun-{uuid_}-{formatted}.stl")

        scene.apply_transform(apply_rotation(scene, 90))
        # scene.apply_translation(origin - scene.centroid)
        print(f"Exporting printrun-{uuid_}...")
        scene.export(f"printrun-{uuid_}.stl")
