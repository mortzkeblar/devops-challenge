#!/usr/bin/env python3

import subprocess
import docker
import argparse


def print_message(message):
    print(f"{'=' * 40}\n{message}\n{'=' * 40}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Script for managing the file upload/download microservice")
    parser.add_argument("-fi", "--forceimage", action="store_true", help="Forzar la construcción de la imagen")
    parser.add_argument("-rmi", "--rmimage", action="store_true", help="Mostrar información de la imagen")
    return parser.parse_args()


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


def delete_image(dock_image):
    client = docker.from_env()
    client.images.remove(dock_image)
    print_message(f"{dock_image} ha sido borrado")


def create_image(dock_image, force):
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
    image_name = "devops-challenge"
    image_tag = "latest"
    image = image_name + ":" + image_tag

    args = parse_arguments()
    if args.rmimage:
        delete_image(image)
        return

    create_image(image, args.forceimage)
    # is_containers_active(image_name)


if __name__ == "__main__":
    main()
