# Development environment for Mac ( multipass )

## Required apps (必要アプリ)
- shellcheck
- pyenv
- ansible-lint
- multipass

## Purpose (目的)

> Migration Vagrat to multipass
> Install tools for Development

> Vagrant から multipass へ移行
> その他開発ツールをインストール

## Usage

### Edit env
```ini
PYTHON_VERSION=3.9.8
RSA_FILE_NAME=~/.ssh/id_rsa # your secret_key
RSA_PUB_FILE_NAME=~/.ssh/id_rsa.pub # your public_key 
ANSIBLE_RSA_PUB_FILE_NAME=~/.ssh/ansible_rsa.pub # optional as you like
CPU=4
MEMORY=4G
DISK_SIZE=60GB
VM_NAME=develop
VM_VERSION=20.04
CLOUD_INIT=./cloud-config.yaml
MOUNT_WORKSPACE_HOST=/CloudStation/workspace # Mount dir host
MOUNT_WORKSPACE_VM=/home/ubuntu/workspace  # Mount dir vm
DEVELOP_INIT=fale  # Ansible roles/develop_init true: exec   false: skip
```

### What Roles/develop_init?
 
>Roles for installation of personal installations (git pull, file copy...)
 
> 個人的な設置のインストール用ロール (git pull, file copy...)

### Create VM
```bash
# permission
chmod 775 ./create_vm.sh
```
```bash
# exec
./create_vm.sh
```

--- 

## Memo
### Exec Ansible

#### Exec all

```bash
ansible-playbook -i hosts/multipass site.yml -l multipass
```

#### Tags (specification Tag)

```bash
ansible-playbook -i hosts/multipass site.yml -l multipass -t tag
```

#### Skip-tags (Exclusion Tag)

```bash
ansible-playbook -i hosts/multipass site.yml -l multipass --skip-tags tag
```

#### Example

```bash
ansible-playbook -i hosts/multipass site.yml -l multipass -t ansible
````

#### Roles

```txt
# tree -L 1
.
├── act
├── ansible
├── ansible_lint
├── awscli
├── bash_it
├── ccze
├── circleci
├── common
├── ctags
├── develop_init
├── direnv
├── docker
├── docker_compose
├── example
├── git
├── glances
├── gnupg2
├── goenv
├── gtags
├── hostname
├── jq
├── lazydocker
├── luaenv
├── mycli
├── neofetch
├── nmap
├── nodenv
├── nvim
├── oh_my_zsh
├── openstack
├── pass
├── phpenv
├── pwgen
├── pyenv
├── rbenv
├── ssh_config
├── sshpass
├── testinfra
├── tests
├── tfenv
├── tmux
├── tmuxinator
├── tmuxp
├── tree
├── vim8
├── yarn
├── zip
└── zsh
```
### Multipass

#### Install multipass

```bash
brew install --cask multipass
```

#### create VM

```bash
multipass launch -c 2 -m 2 -d 20GB  -n <VM_NAME>  20.04 --cloud-init ./cloud-config.yaml
```

### cloud-init yaml

#### Example

```yaml
---
locale: en_US.UTF8
timezone: Asia/Tokyo
package_upgrade: true
users:
  - name: ubuntu
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh-authorized-keys:
      - xxxxxxxxxx

packages:
  - docker
  - avahi-daemon
  - apt-transport-https
  - ca-certificates
  - curl
  - gnupg
  - lsb-release

runcmd:
  - sudo curl -fsSL https://get.docker.com | sudo bash
  - sudo systemctl enable docker
  - sudo systemctl enable -s HUP ssh
  - sudo groupadd docker
  - sudo usermod -aG docker ubuntu
```

#### VM list

```bash
multipass ls
```

#### VM  commands

```bash
multipass start 
multipass stop
multipass delete
multipass purge
```

#### Mount Dir

```bash
multipass mount "${HOME}"/xxx <VM_NAME>:"${HOME}"/xxx
```

#### Shell login

```bash
multipass shell <VM_NAME>
```

#### Kill

```bash
ps -ef | grep -i multipass | awk '{print "sudo kill -9 "$2}' | sh

```

## License

MIT

