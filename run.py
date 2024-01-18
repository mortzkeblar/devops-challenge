import subprocess
import docker
import argparse


def print_message(message):
    print(f"{'=' * 40}\n{message}\n{'=' * 40}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Script for managing the file upload/download microservice")
    parser.add_argument("--fi", action="store_true", help="Forzar la construcción de la imagen")
    parser.add_argument("--rmi", action="store_true", help="Mostrar información de la imagen")
    return parser.parse_args()


def check_exists_image(client, dock_image):
    try:
        client.images.get(dock_image)
        return True
    except docker.errors.ImageNotFound:
        return False


def is_containers_active(client, dock_image):
    containers = client.containers.list(all=True)

    if not containers:
        return "Container status: no containers created"

    container_info = []
    for container in containers:
        container_info.append(container.attrs['Config']['Image'])
        if dock_image == container.attrs['Config']['Image']:
            container_info.append(f"Container status: {'running' if container.status == 'running' else 'exited'}")

    return container_info


def show_image(client, dock_image):
    image_show = client.images.get(dock_image)
    print_message(f"Image name: {dock_image}")
    print_message(f"Image ID: {image_show.short_id}")
    print_message(f"Created: {image_show.attrs['Created']}")
    container_info = is_containers_active(client, dock_image)
    if container_info:
        for info in container_info:
            print_message(info)


def delete_image(client, dock_image):
    client.images.remove(dock_image)
    print_message(f"{dock_image} ha sido borrado")


def create_image(client, dock_image, force):
    if check_exists_image(client, dock_image):
        if force:
            subprocess.run(f'docker build --no-cache -t {dock_image} .', shell=True)
            print_message(f"The image {dock_image} recreated")
            show_image(client, dock_image)
            return

        print_message(f"The image {dock_image} already exists")
        show_image(client, dock_image)
        return

    subprocess.run(f'docker build -t {dock_image} .', shell=True)
    print_message(f"The image {dock_image} created")
    show_image(client, dock_image)


if __name__ == "__main__":
    image_name = "devops-challenge"
    image_tag = "latest"
    image = image_name + ":" + image_tag

    cliente = docker.from_env()
    args = parse_arguments()

    create_image(cliente, image, args.fi)
