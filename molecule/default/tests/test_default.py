import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


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


def test_funkwhale_user_creation(host):
    user = host.user("funkwhale")
    assert user.home == "/srv/funkwhale"
    assert user.shell == "/bin/false"


@pytest.mark.parametrize(
    "path",
    [
        "/srv/funkwhale/",
        "/srv/funkwhale/data/media",
        "/srv/funkwhale/data/static",
        "/srv/funkwhale/data/music",
    ],
)
def test_funkwhale_directories_creation(path, host):
    dir = host.file(path)

    assert dir.exists is True
    assert dir.is_directory is True


def test_funkwhale_env_file(host):
    f = host.file("/srv/funkwhale/config/.env")

    assert f.contains("MEDIA_ROOT=/srv/funkwhale/data/media") is True
    assert f.contains("STATIC_ROOT=/srv/funkwhale/data/static") is True
    assert f.contains("MUSIC_DIRECTORY_PATH=/srv/funkwhale/data/music") is True
    assert f.contains("MUSIC_DIRECTORY_SERVE_PATH=/srv/funkwhale/data/music") is True
    assert f.contains("FUNKWHALE_HOSTNAME=yourdomain.funkwhale") is True
    assert f.contains("FUNKWHALE_PROTOCOL=https") is True
    assert f.contains("DJANGO_SECRET_KEY=") is True
    assert f.contains("FUNKWHALE_API_IP=127.0.0.1") is True
    assert f.contains("FUNKWHALE_API_PORT=5000") is True
    assert f.contains("REVERSE_PROXY_TYPE=nginx") is True
    assert f.contains("DATABASE_URL=postgresql://funkwhale@:5432/funkwhale") is True
    assert f.contains("CACHE_URL=redis://127.0.0.1:6379/0") is True
    assert (
        f.contains("EMAIL_CONFIG=smtp+tls://user@:password@youremail.host:587") is True
    )
    assert f.contains("DEFAULT_FROM_EMAIL=noreply@yourdomain") is True
    assert f.contains("FUNKWHALE_FRONTEND_PATH=/srv/funkwhale/frontend/dist") is True
    assert (
        f.contains("FUNKWHALE_SPA_HTML_ROOT=/srv/funkwhale/frontend/dist/index.html")
        is True
    )
    assert f.contains("NGINX_MAX_BODY_SIZE=100M") is True
    assert f.contains("DJANGO_SETTINGS_MODULE=config.settings.production") is True

    # additional vars
    assert f.contains("ADDITIONAL_VAR=1") is True
    assert f.contains("ADDITIONAL_VAR=2") is True
