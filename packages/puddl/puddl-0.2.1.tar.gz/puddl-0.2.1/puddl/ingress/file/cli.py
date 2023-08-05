import click


@click.command(name='file')
@click.argument('path', type=click.Path(exists=True), nargs=-1, required=True)
def main(path):
    from puddl.models import Device
    from puddl.ingress.file.models import File
    for x in path:  # path could use a better name, but the help text needs to be sane
        File.objects.upsert(
            device=Device.objects.me(),
            path=x
        )
