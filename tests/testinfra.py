""" This is a testinfra for ansible program."""
# vars
host_name = "develop.ubuntu"
home_path = "/home/ubuntu/"


def test_passwd_file(host):
    """Check passwd"""
    passwd = host.file("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644


def test_distribution(host):
    assert "ubuntu" == host.system_info.distribution


def test_hostname(host):
    """Check hostname"""
    # host = testinfra.get_host("ansible://multipass")
    # host.ansible.get_variables()

    # host = host.get_host("ansible://multipass")
    #     all_variables = host.ansible.get_variables()
    # print( all_variables )
    # assert host.sysctl("kernel.hostname") == all_variables["hostname"]
    assert host.sysctl("kernel.hostname") == host_name
    # return host.sysctl("kernel.hostname")
    # pprint.pprint(host)
    # return host


def test_enable_services(host):
    enable_services = [
        "ssh",
        "docker",
    ]
    for i in range(len(enable_services)):
        service = host.service(enable_services[i])
        assert service.is_running
        assert service.is_enabled


def test_installed_pkg(host):
    installed_pkg = [
        "git",
        "gnupg2",
        "sshpass",
        "pass",
        "zip",
        "docker-ce",
        # "python",
        "ruby",
        "zsh",
        "glances",
        "neofetch",
        "ccze",
        "neovim",
        "pwgen",
        "nmap",
        "tmux",
        "jq",
    ]
    for i in range(len(installed_pkg)):
        pkg = host.package(installed_pkg[i])
        assert pkg.is_installed


def test_file_exist(host):
    pathes = [
        home_path + ".bash_it",
        home_path + ".oh-my-zsh",
        "/usr/bin/ctags",
        "/usr/local/bin/gtags",
        "/usr/local/bin/circleci",
        "/usr/local/bin/vim",
        home_path + ".local/bin/lazydocker",
    ]
    for path in pathes:
        assert host.file(path).exists


def test_envs(host):
    envs = {
        "python": {
            "path": home_path + ".pyenv/shims/python",
        },
        "ruby": {
            "path": home_path + ".rbenv/shims/ruby",
        },
        "lua": {
            "path": home_path + ".luaenv/shims/lua",
        },
        "go": {
            "path": home_path + ".luaenv/shims/lua",
        },
    }
    for key in envs:
        assert host.file(envs[key]["path"]).exists


def test_apps(host):
    apps = {
        "pass": {"command": "which pass", "result": "/usr/bin/pass"},
        "sshpass": {"command": "which sshpass", "result": "/usr/bin/sshpass"},
        "git": {"command": "which git", "result": "/usr/bin/git"},
        "zip": {"command": "which zip", "result": "/usr/bin/zip"},
        "tmux": {"command": "which tmux", "result": "/usr/bin/tmux"},
        "docker": {"command": "which docker", "result": "/usr/bin/docker"},
        "docker-compose": {
            "command": "which docker-compose",
            "result": "/usr/local/bin/docker-compose",
        },
        "zsh": {"command": "which zsh", "result": "/bin/zsh"},
        "ctags": {"command": "which ctags", "result": "/usr/bin/ctags"},
        "gtags": {"command": "which gtags", "result": "/usr/local/bin/gtags"},
        "circleci": {"command": "which circleci", "result": "/usr/local/bin/circleci"},
        "glances": {"command": "which glances", "result": "/usr/bin/glances"},
        "neofetch": {"command": "which neofetch", "result": "/usr/bin/neofetch"},
        "ccze": {"command": "which ccze", "result": "/usr/bin/ccze"},
        "vim8_pass": {"command": "which vim", "result": "/usr/local/bin/vim"},
        "nvim": {"command": "which nvim", "result": "/usr/bin/nvim"},
        "lazydocker": {
            "command": "which lazydocker",
            "result": home_path + ".local/bin/lazydocker",
        },
        "pwgen": {"command": "which pwgen", "result": "/usr/bin/pwgen"},
        "nmap": {"command": "which nmap", "result": "/usr/bin/nmap"},
        "jq": {"command": "which jq", "result": "/usr/bin/jq"},
        "tmuxp": {"command": "which tmuxp", "result": home_path + ".pyenv/shims/tmuxp"},
        "act": {"command": "which act", "result": "/home/ubuntu/bin/act"},
    }
    for key in apps:
        # result = host.run(apps[key]["command"])
        # assert apps[key]["result"] in result
        # assert apps[key]["result"] == result
        assert host.file(apps[key]["result"]).exists


#
def test_open_port(host):
    """Check ports"""
    ports = [
        "22",
        "2376",
    ]
    localhost = host.addr("localhost")
    for port in ports:
        assert localhost.port(port).is_reachable


def test_multipass_user(host):
    users = [
        "ubuntu",
    ]
    for user in users:
        u = host.user(user)
        assert u.exists
        assert u.name == user
        assert u.home == "/home/" + user
