# TODO rename me to config :>

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)


PUDDLRC = Path.home() / '.puddlrc'


def django_setup(debug=False, log_level='INFO', log_sql=False, skipconfigured=False,
                 **kwargs):
    """
    :param skipconfigured: explicitly silence Django "already configured" exception
    """
    from django.conf import settings
    from puddl.project.settings import logging_config
    if skipconfigured and settings.configured:
        return
    config = read_rcfile()
    if debug:
        log_level = 'DEBUG'
    # TODO get stuff from ~/.puddlrc
    result = dict(
        DEBUG=debug,
        LOGGING=logging_config(log_level, log_sql),
        # ALLOWED_HOSTS=...,
        SECRET_KEY='^6x*s4#x8!+zcv9j5h69h+=#9l#h)^u&q6dxx@5ir_+fr7p1)j',
        # if you add stuff here, maybe exclude it in puddl.cli.PluginsCommand
        INSTALLED_APPS=[
            'django.contrib.postgres',
            'puddl',
            'puddl.contrib.file',
        ] + config.get('plugins', []),
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'HOST': config['PGHOST'],
                'PORT': config['PGPORT'],
                'NAME': config['PGDATABASE'],
                'USER': config['PGUSER'],
                'PASSWORD': config['PGPASSWORD'],
            }
        },
    )
    result.update(kwargs)
    settings.configure(**result)
    import django
    django.setup()
    if settings.DEBUG:
        log.warning(f'debug mode enabled')
    return settings


def read_rcfile():
    try:
        with PUDDLRC.open() as f:
            return json.load(f)
    except FileNotFoundError:
        with PUDDLRC.open('w') as f:
            json.dump({}, f)
            return {}


def write_rcfile(config):
    with PUDDLRC.open('w') as f:
        json.dump(config, f, indent=2, sort_keys=True)
