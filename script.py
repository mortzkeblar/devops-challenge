#!/usr/bin/env python3

import subprocess
import docker
import argparse
import sys

IMAGE_NAME = "devops-challenge"
IMAGE_TAG = "latest"

client = docker.from_env()


def print_message(message):
    print(f"{'=' * 60}\n{message}\n{'=' * 60}")


def parse_arguments(dock_image):
    parser = argparse.ArgumentParser(description="Script for managing the file upload/download microservice")
    subparsers = parser.add_subparsers()

    parser_build = subparsers.add_parser("build", help="Builds a Docker image from current directory. I can use "
                                                       "--force to force image build without cache save")
    parser_build.add_argument("--force", action="store_true", help="Force build image with --no-cache option")
    parser_build.set_defaults(func=create_image)
    parser_remove = subparsers.add_parser("remove", help="Delete the image if there is an existing image already "
                                                         "constructed")
    parser_remove.set_defaults(func=delete_image)

    if len(sys.argv) <= 1:
        sys.argv.append("--help")

    options = parser.parse_args()

    if hasattr(options, 'force'):
        options.func(dock_image, options.force)
    else:
        options.func(dock_image)


def check_exists_image(dock_image):
    try:
        client.images.get(dock_image)
        return True
    except docker.errors.ImageNotFound:
        return False


def is_containers_active(dock_image):
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
    image_show = client.images.get(dock_image)
    print(f"Image name: {dock_image}")
    print(f"Image ID: {image_show.short_id}")
    print(f"Created: {image_show.attrs['Created']}")
    is_containers_active(dock_image)


def delete_image(dock_image):
    try:
        client.images.remove(dock_image)
        print_message(f"{dock_image} ha sido borrado")
    except docker.errors.ImageNotFound:
        print_message("There is no image to delete")


def create_image(dock_image, force=False):
    if check_exists_image(dock_image):
        if force:
            subprocess.run(f'docker build --no-cache -t {dock_image} .', shell=True)
            print_message(f"The image {dock_image} recreated")
            show_image(dock_image)
            return

        print_message(f"The image {dock_image} already exists")
        show_image(dock_image)
        return

    subprocess.run(f'docker build -t {dock_image} .', shell=True)
    print_message(f"The image {dock_image} created")
    show_image(dock_image)


def main():
    image = f"{IMAGE_NAME}:{IMAGE_TAG}"
    parse_arguments(image)


if __name__ == "__main__":
    main()
