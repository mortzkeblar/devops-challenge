#!/usr/bin/env python3

import subprocess

image = 'devops-challenge:latest'
db_dir = '/tmp/db'


def create_image():
    subprocess.run(f'docker build -t {image} .', shell=True)
    print(subprocess.run(f"docker images {image}", shell=True, stdout=subprocess.PIPE, text=True).stdout)


def run_container():
    if no_clone():
        subprocess.run(f'docker run -d -v {db_dir}:/src/instance {image}', shell=True)


# {db_dir}/db.sqlite3/:/src/instance/db.sqlite3

def no_clone():
    listas = subprocess.run("docker ps -a | awk '{print $2}' | tail -n +2 ", shell=True, stdout=subprocess.PIPE,
                            text=True).stdout.split("\n")
    for lista in listas:
        if lista == image:
            print("Ya existe una un contenedor en ejecución")
            return False


create_image()
#run_container()

#no_clone()
