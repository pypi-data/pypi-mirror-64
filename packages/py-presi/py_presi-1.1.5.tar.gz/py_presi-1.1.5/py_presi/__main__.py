import click
import py_presi.build


@click.command()
def build():
    click.echo("Building ...")
    py_presi.build.build()


if __name__ == "__main__":
    build()
