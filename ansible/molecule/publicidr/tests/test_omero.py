import os
import testinfra.utils.ansible_runner
import pytest

# TODO: This should be 'omero-hosts' if we get it deployed in docker
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('omeroreadwrite-hosts')


@pytest.mark.parametrize("name", ["omero-server", "omero-web", "nginx"])
def test_services_running_and_enabled(host, name):
    service = host.service(name)
    assert service.is_running
    assert service.is_enabled


def test_nginx_port_listening(host):
    out = host.check_output('ss --numeric --listening --tcp')
    print(out)
    assert (host.socket(f"tcp://0.0.0.0:80").is_listening or
            host.socket(f"tcp://:::80").is_listening)


@pytest.mark.parametrize("port", [4063, 4064])
def test_omero_port_listening(host, port):
    out = host.check_output('ss --numeric --listening --tcp')
    print(out)
    assert (host.socket(f"tcp://0.0.0.0:{port}").is_listening or
            host.socket(f"tcp://:::{port}").is_listening)


def test_registry_port_listening(host):
    assert (host.socket(f"tcp://0.0.0.0:4061").is_listening or
            host.socket(f"tcp://:::4061").is_listening)
