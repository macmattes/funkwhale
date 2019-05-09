import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_hosts_file(host):
    f = host.file("/etc/hosts")

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"


@pytest.mark.parametrize(
    "package",
    [
        "python3",
        "python3-dev",
        "python3-pip",
        "python3-venv",
        "libldap2-dev",
        "libsasl2-dev",
        "git",
        "unzip",
        "build-essential",
        "ffmpeg",
        "libjpeg-dev",
        "libmagic-dev",
        "libpq-dev",
        "postgresql-client",
    ],
)
def test_installed_mandatory_packages(host, package):
    package = host.package(package)
    assert package.is_installed


@pytest.mark.parametrize("service", ["redis-server", "postgresql", "nginx"])
def test_installed_services(host, service):
    service = host.service(service)
    assert service.is_running
    assert service.is_enabled


def test_database_created(host):
    cmd = """
        sudo -u postgres psql -A -t -c \
            "SELECT 1 FROM pg_catalog.pg_user u WHERE u.usename =  'funkwhale';"
    """
    result = host.run(cmd)
    assert result.stdout == "1"


def test_database_user_created(host):
    cmd = """
        sudo -u postgres psql -A -t -c "SELECT 1 FROM pg_database WHERE datname = 'funkwhale';"
    """
    result = host.run(cmd)
    assert result.stdout == "1"
