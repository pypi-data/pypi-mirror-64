import logging

import click

log = logging.getLogger(__name__)
LOG_LEVELS = ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG']


class PluginsCommand(click.Group):
    """
    Hook plugins.

    https://click.palletsprojects.com/en/7.x/commands/#custom-multi-commands
    """

    def list_commands(self, ctx):
        core_commands = set(super().list_commands(ctx))
        from puddl.conf import django_setup
        django_setup(skipconfigured=True)
        from django.apps import apps
        candidates = [app.label for app in apps.get_app_configs()]
        commands = set(x for x in candidates if x not in ['puddl', 'postgres'])
        # the label of an installed app must not overlap with puddl's core commands
        invalid_commands = sorted(core_commands & commands)
        if invalid_commands:
            log.error(f'invalid commands: {invalid_commands}')
            raise SystemExit(1)
        return sorted(core_commands | commands)

    def get_command(self, ctx, name):
        core_commands = super().list_commands(ctx)
        if name in core_commands:
            return globals()[name]
        from puddl.conf import django_setup
        django_setup(skipconfigured=True)
        from django.apps import apps
        x = apps.get_app_config(name)
        import importlib
        mod = importlib.util.resolve_name('.cli', x.module.__package__)
        entrypoint = importlib.import_module(mod).main
        if entrypoint.name != name:
            log.warning(f'plugin {name} should set "name={name}" in cli.main()')
            entrypoint.name = name
        return entrypoint


@click.group(cls=PluginsCommand)
@click.option('-d', '--debug/--no-debug')
@click.option('-l', '--log-level',
              type=click.Choice(LOG_LEVELS, case_sensitive=False),
              default='INFO')
@click.option('--log-sql/--no-log-sql')
@click.version_option()
def root(debug, log_level, log_sql):
    from puddl.conf import django_setup
    django_setup(debug, log_level, log_sql, skipconfigured=True)


@root.group()
def config():
    pass


@config.command()
@click.option('--from-key-value', is_flag=True)
def update(from_key_value):
    from puddl.conf import read_rcfile, write_rcfile
    config = read_rcfile()
    if from_key_value:
        updates = {}
        for line in click.get_text_stream('stdin').read().strip().split('\n'):
            k, v = line.split('=')
            updates[k] = v
        config.update(updates)
    write_rcfile(config)


@root.group()
def app():
    pass


@app.command('add')
@click.argument('package_path')
def add_app(package_path):
    from puddl.conf import read_rcfile, write_rcfile
    config = read_rcfile()
    if 'plugins' not in config:
        config['plugins'] = []
    tmp = config.get('plugins', []) + [package_path]
    config['plugins'] = list(sorted(set(tmp)))
    write_rcfile(config)


@app.command('ls')
def app_ls():
    from django.apps import apps
    xs = [f'{x.label} ({x.name})' for x in apps.get_app_configs()]
    print('\n'.join((sorted(xs))))


@root.group()
def db():
    pass


@db.command()
def health():
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    log.info('database available')


@db.command()
def migrate():
    from django.core import management
    management.call_command('migrate')


@db.command()
def shell():
    from django.core import management
    management.call_command('dbshell')


def main():
    # this function is referenced in `setup.py`
    root(auto_envvar_prefix='PUDDL')


if __name__ == '__main__':
    # https://click.palletsprojects.com/en/7.x/options/#values-from-environment-variables
    main()
