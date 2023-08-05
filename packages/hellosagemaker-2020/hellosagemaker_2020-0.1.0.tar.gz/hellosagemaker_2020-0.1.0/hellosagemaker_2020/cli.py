"""Console script for hellosagemaker_2020."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for hellosagemaker_2020."""
    click.echo("Replace this message by putting your code into "
               "hellosagemaker_2020.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
