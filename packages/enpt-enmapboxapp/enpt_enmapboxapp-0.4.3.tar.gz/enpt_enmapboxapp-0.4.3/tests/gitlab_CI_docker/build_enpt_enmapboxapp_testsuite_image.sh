#!/usr/bin/env bash

context_dir="./context"
dockerfile="enpt_enmapboxapp_ci.docker"
tag="enpt_enmapboxapp_ci:0.4.0"
gitlab_runner="enpt_enmapboxapp_gitlab_CI_runner"

# get enmapbox project
rm -rf context/enmapbox
git clone https://bitbucket.org/hu-geomatics/enmap-box.git ./context/enmapbox
# git clone https://bitbucket.org/hu-geomatics/enmap-box.git --branch develop --single-branch ./context/enmapbox

# get EnPT project
rm -rf context/enpt
git clone git@gitext.gfz-potsdam.de:EnMAP/GFZ_Tools_EnMAP_BOX/EnPT.git ./context/enpt

# get SICOR project
rm -rf context/sicor
git clone git@gitext.gfz-potsdam.de:EnMAP/sicor.git ./context/sicor

echo "#### Build runner docker image"
sudo docker rmi ${tag}
sudo docker build -f ${context_dir}/${dockerfile} -m 20G -t ${tag} ${context_dir}
# sudo docker build -f ./context/enpt_enmapboxapp_ci.docker -m 20G -t enpt_enmapboxapp_ci:0.7.0 ./context --no-cache

echo "#### Create gitlab-runner (daemon) container with tag; ${tag}"
sudo docker stop ${gitlab_runner}
sudo docker rm ${gitlab_runner}
sudo docker run -d --name ${gitlab_runner} --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=$DISPLAY \
  gitlab/gitlab-runner:latest

echo "#### Register container at gitlab, get token here https://gitext.gfz-potsdam.de/EnMAP/GFZ_Tools_EnMAP_BOX/enpt_enmapboxapp/settings/ci_cd"
read -p "Please enter gitlab token: " token
echo ""
read -p "Please enter gitlab runner name: " runner_name
echo "New gitlab runner image will named  ${gitlab_runner}"
sudo docker exec -it ${gitlab_runner} /bin/bash -c "\
  export RUNNER_EXECUTOR=docker && gitlab-ci-multi-runner register -n \
  --url 'https://gitext.gfz-potsdam.de/ci' \
  --registration-token '${token}' \
  --run-untagged=true \
  --locked=true \
  --tag-list  enpt_enmapboxapp_client \
  --description '${runner_name}' \
  --docker-image '${tag}' "
