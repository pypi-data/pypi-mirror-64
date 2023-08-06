#!/bin/sh

set -x

ssh_cmd="ssh -F /srv/magnum/.ssh/config root@localhost"

# docker is already enabled and possibly running on centos atomic host
# so we need to stop it first and delete the docker0 bridge (which will
# be re-created using the flannel-provided subnet).
echo "stopping docker"
$ssh_cmd systemctl stop docker

# make sure we pick up any modified unit files
$ssh_cmd systemctl daemon-reload

for action in enable restart; do
    for service in docker kubelet kube-proxy; do
        echo "$action service $service"
        $ssh_cmd systemctl $action $service
    done
done
