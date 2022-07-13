#!/usr/bin/env bash

set -eu
echo -e -n "\n"
echo "###################################"
echo "####        shellcheck        #####"
echo "###################################"
shellcheck create_vm.sh

echo -e -n "\n"
echo "###################################"
echo "####       Read .env          #####"
echo "###################################"
source ./.env

pv=$(python --version | awk -F " " '{ print $2 }')
echo "####   Check python version    #####"
echo "python version: $pv"
echo -e -n "\n"

if [ "$pv" != "$PYTHON_VERSION" ]; then
  if [ ! -e ~/.pyenv/versions/"$PYTHON_VERSION" ]; then
    echo -e -n "\n"
    echo "###################################"
    echo "pyenv install $PYTHON_VERSION"
    echo "###################################"
    pyenv install "$PYTHON_VERSION"
  fi
  echo "###################################"
  echo "pyenv install local $PYTHON_VERSION"
  echo "###################################"
  pyenv local "$PYTHON_VERSION"
fi

echo -e -n "\n"
echo "###################################"
echo "### pip install requirement.txt ###"
echo "###################################"
pip install --upgrade pip
pip install -r requirements.txt

echo -e -n "\n"
echo "###################################"
echo "###           Block             ###"
echo "###################################"
black tests/

echo -e -n "\n"
echo "###################################"
echo "###           flake8             ###"
echo "###################################"
flake8 tests/

echo -e -n "\n"
echo "###################################"
echo "###       ansible-lint          ###"
echo "###################################"
ansible-lint

echo -e -n "\n"
echo "###################################"
echo "###       cloud-config          ###"
echo "###################################"
AUTHORIZED_KEYS_ID_RSA=$(cat "$RSA_PUB_FILE_NAME")
AUTHORIZED_KEYS_ANSIBLE_RSA=$(cat "$ANSIBLE_RSA_PUB_FILE_NAME")
cat >./cloud-config.yaml <<_EOF_
---
locale: en_US.UTF8
timezone: Asia/Tokyo
users:
  - name: ubuntu
    ssh-authorized-keys:
      - ${AUTHORIZED_KEYS_ID_RSA}
      - ${AUTHORIZED_KEYS_ANSIBLE_RSA}
_EOF_

echo -e -n "\n"
echo "###################################"
echo "###         Create VM           ###"
echo "###################################"
multipass launch -c "${CPU}" -m "${MEMORY}" -d "${DISK_SIZE}" -n "${VM_NAME}" "${VM_VERSION}" --cloud-init "${CLOUD_INIT}"
sleep 30

echo -e -n "\n"
echo "###################################"
echo "###        Mount Dir            ###"
echo "###################################"
multipass mount "${MOUNT_WORKSPACE_HOST}" "${VM_NAME}":"${MOUNT_WORKSPACE_VM}"
echo "mount ${MOUNT_WORKSPACE_HOST} ${VM_NAME}:${MOUNT_WORKSPACE_VM}"

echo -e -n "\n"
echo "###################################"
echo "###      VM IP address          ###"
echo "###################################"
vm_ip=$(multipass info develop | grep IPv4 | awk '{ print $2 }')
echo "ipv4 : ${vm_ip}"

echo -e -n "\n"
echo "###################################"
echo "###  Create ansible inventory   ###"
echo "###################################"
cat >./hosts/multipass <<_EOF_
[multipass]
multipass ansible_host=$vm_ip ansible_user=ubuntu ansible_ssh_private_key_file=$RSA_FILE_NAME ansible_ssh_common_args='-o StrictHostKeyChecking=no'

[ubuntu20]
multipass
_EOF_

cat ./hosts/multipass

echo -e -n "\n"
echo "###################################"
echo "###   Exec ansible playbook     ###"
echo "###################################"

echo "$DEVELOP_INIT"
if [ "$DEVELOP_INIT" == 'true' ]; then
	ansible-playbook -i hosts/multipass site.yml -l multipass
#	ansible-playbook -i hosts/multipass site.yml -l multipass -t tests
else
	ansible-playbook -i hosts/multipass site.yml -l multipass --skip-tags develop_init
fi
