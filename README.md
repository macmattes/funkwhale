Funkwhale ansible role
======================

An ansible role to install and update [Funkwhale](https://funkwhale.audio).

Summary
-------

Using this role, you can install and upgrade a Funkwhale pod, closely matching our [standard installation guide](https://docs.funkwhale.audio/installation/debian.html). The role will take care of:

- Installing and configure dependencies and packages
- Install and configure PostgreSQL, Redis and Nginx (optional)
- Install and configure Funkwhale and it's dependencies
- Install and configure a SSL certificate with Let's Encrypt (optional)

Installation and usage
----------------------

Install ansible:

```
pip install --user ansible
```

Create a directory for ansible files:

    mkdir ~/ansible-funkwhale
    cd ansible-funkwhale

Create a playbook requirements and inventory file:

    touch requirements.yml
    touch playbook.yml
    touch inventory.ini

Add the following to `requirements.yml`:

```
- src: git+https://dev.funkwhale.audio/funkwhale/ansible
  name: funkwhale
  version: master
```

Install the role:

```
ansible-galaxy install -r requirements.yml
```

Add the following to `playbook.yml`:

```yaml
- hosts: funkwhale-servers
  roles:
    - role: funkwhale
      funkwhale_hostname: yourdomain.funkwhale
      funkwhale_version: 0.18.3
      funkwhale_letsencrypt_email: contact@youremail.com
```

See below for a full documentation on available variables.

Add your server to `inventory.ini`:

```ini
[funkwhale-servers]
your-server-ip-or-domain
```

Launch the installation (in check mode, so nothing is applied):

```
ansible-playbook --ask-become-pass -i inventory.ini playbook.yml --check --diff
```
*On some hosts, you may need to install the `python-apt` package for check mode to work*.

This command will show you the changes that would be applied to your system. If you are confortable with them,
rerun the same command without the `--check` flag.


Role Variables
--------------

**Required variables**

| name                          | Example                       | Description                                   |
| ----------------------------- | ----------------------------- | --------------------------------------------- |
| `funkwhale_hostname`          | `yourdomain.funkwhale`        | The domain name of your Funkwhale pod         |
| `funkwhale_version`           | `0.18.3`                      | The version to install/upgrade to. You can also use `develop` to run the development branch         |
| `funkwhale_letsencrypt_email` | `contact@youremail.com`       | The email to associate with your Let's Encrypt certificate (not needed if you set `funkwhale_letsencrypt_enabled: false`, see below) |

**Optional variables**


| name                                    | Default                       | Description                                   |
| --------------------------------------- | ----------------------------- | --------------------------------------------- |
| `funkwhale_api_ip`                      | `127.0.0.1`                   | IP adress to bind the Funkwhale server to |
| `funkwhale_api_port`                    | `5000`                        | Port to bind the Funkwhale server to |
| `funkwhale_config_path`                 | `/srv/funkwhale/config`       | Path to Funkwhale's configuration directory |
| `funkwhale_database_managed`            | `true`                        | If `true`, the role will manage the database server and Funkwhale's database  |
| `funkwhale_database_name`               | `funkwhale`                   | Name of the Funkwhale database to use |
| `funkwhale_database_user`               | `funkwhale`                   | Postgresql username to login as |
| `funkwhale_env_vars`                    | `[]`                          | List of environment variables to append to the generated `.env` file. Example: `["AWS_ACCESS_KEY_ID=myawsid", "AWS_SECRET_ACCESS_KEY=myawskey"]` |
| `funkwhale_external_storage_enabled`    | `false`                       | If `true`, set up the proper configuration to use an extenal storage for media files |
| `funkwhale_install_path`                | `/srv/funkwhale`              | Path were frontend, api and virtualenv files should be stored (**no trailing slash**) |
| `funkwhale_letsencrypt_certbot_flags`   | `null`                        | Additional flags to pass to `certbot` |
| `funkwhale_letsencrypt_enabled`         | `true`                        | If `true`, will configure SSL with certbot and Let's Encrypt |
| `funkwhale_media_path`                  | `/srv/funkwhale/data/media`   | Path were audio and uploaded files should be stored (**no trailing slash**)  |
| `funkwhale_music_path`                  | `/srv/funkwhale/data/music`   | Path to your existing music library, to use with [CLI import](https://docs.funkwhale.audio/admin/importing-music.html) (**no trailing slash**) |
| `funkwhale_nginx_managed`               | `true`                        | If `true`, will install and configure nginx |
| `funkwhale_nginx_max_body_size`         | `100M`                        | Value of nginx's `max_body_size` parameter to use |
| `funkwhale_protocol`                    | `https`                       | If set to `https`, will configure Funkwhale and Nginx to work behind HTTPS. Use `http` to completely disable SSL. |
| `funkwhale_redis_managed`               | `true`                        | If `true`, will install and configure redis |
| `funkwhale_ssl_cert_path`               | ``                            | Path to an existing SSL certificate to use (use in combination with `funkwhale_letsencrypt_enabled: false`) |
| `funkwhale_ssl_key_path`                | ``                            | Path to an existing SSL key to use (use in combination with `funkwhale_letsencrypt_enabled: false`) |
| `funkwhale_static_path`                 | `/srv/funkwhale/data/static`  | Path were Funkwhale static files should be stored |
| `funkwhale_systemd_after`               | `redis.service postgresql.service` | Configuration used for Systemd `After=` directive. Modify it if you have a database or redis server on a separate host   |
| `funkwhale_systemd_service_name`        | `funkwhale`                   | Name of the generated Systemd service, e.g when calling `systemctl start <xxx>` |
| `funkwhale_username`                    | `funkwhale`                   | Username of the system user and owner of Funkwhale data, files and configuration |

Supported platforms
-------------------

- Debian 9
- More to come

Dependencies
------------

This roles has no other dependencies.

License
-------

AGPL3

Author Information
------------------

Contact us at https://funkwhale.audio/community/
