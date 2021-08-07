#!/usr/bin/python3

from itertools import groupby

import docker
import yaml

def update_yaml(file):
    client = docker.from_env()
    with open(file, 'r') as f:
        try:
            docker_compose_file = yaml.safe_load(f)
            image_list = [image for image in client.images.list() if 'repo.spectrum-health.org' in image.attrs['RepoTags'][0]]
            image_list.sort(key=lambda image: image.attrs['RepoTags'][0].split('/')[2].split(':')[0] if len(image.attrs['RepoTags']) > 0 and len(image.attrs['RepoTags'][0].split('/')) > 1 else '')
            image_group_list = [list(i) for j, i in groupby(image_list, lambda image: image.attrs['RepoTags'][0].split('/')[2].split(':')[0] if len(image.attrs['RepoTags']) > 0 and len(image.attrs['RepoTags'][0].split('/')) > 1 else '')]
            for service in docker_compose_file['services']:
                for image in image_group_list:
                    if service in image[0].attrs['RepoTags'][0]:
                        docker_compose_file['services'][service]['image'] = image[0].attrs['RepoTags'][0]
        except yaml.YAMLError as exc:
            print(exc)
            
    with open(file, 'w') as f:
        try:
            yaml.dump(docker_compose_file, f)
        except yaml.YAMLError as exc:
            print(exc)

def main():
    update_yaml('docker-compose.yaml')
    update_yaml('docker-compose-debug.yaml')

if __name__ == "__main__":
    main()
