#!/usr/bin/env python3

import subprocess
import docker


def print_message(message):
    print(f"{'=' * 40}\n{message}\n{'=' * 40}")


def check_exists_image(dock_image):
    client = docker.from_env()
    try:
        client.images.get(dock_image)
        return True
    except docker.errors.ImageNotFound:
        return False


def is_containers_active(dock_image):
    client = docker.from_env()
    containers = client.containers.list(all=True)

    if not containers:
        print("Container status: not containers created")
        return

    for container in containers:
        print(container.attrs['Config']['Image'])
        if dock_image == container.attrs['Config']['Image']:
            if container.status == "running":
                print(f"Container status: running")
            else:
                print(f"Container status: exited")


def show_image(dock_image):
    client = docker.from_env()
    image_show = client.images.get(dock_image)
    print(f"Image name: {dock_image}")
    print(f"Image ID: {image_show.short_id}")
    print(f"Created: {image_show.attrs['Created']}")
    is_containers_active(dock_image)


def create_image(dock_image):
    if check_exists_image(dock_image):
        print_message(f"The image {dock_image} already exists")
        show_image(image)
        return

    subprocess.run(f'docker build -t {dock_image} .', shell=True)
    print_message(f"The image {dock_image} created")
    show_image(image)


if __name__ == "__main__":
    image_name = "devops-challenge"
    image_tag = "latest"
    image = image_name + ":" + image_tag

    create_image(image)
    # is_containers_active(image_name)
