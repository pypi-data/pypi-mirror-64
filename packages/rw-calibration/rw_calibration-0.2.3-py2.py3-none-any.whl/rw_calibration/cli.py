"""Console script for rw_calibration."""
import sys
import click
from rw_calibration.rw_calibration import calibrate, read_data


@click.command()
@click.option("--wfile", "-w", help="Path to World Coordinates File")
@click.option("--rfile", "-r", help="Path to Robot Coordinates File")
def main(wfile, rfile):
    """Console script for rw_calibration."""
    if wfile is None:
        click.echo(
            click.style(
                "Error: please indicate the path to World Coordinates File", fg="red"
            )
        )
        return 1
    elif rfile is None:
        click.echo(
            click.style(
                "Error: please indicate the path to Robot Coordinates File", fg="red"
            )
        )
        return 1
    else:
        wpoints = read_data(wfile, sep="\t")
        rpoints = read_data(rfile, sep=" ")
        results = calibrate(wpoints, rpoints)

        click.echo("\nRototranslator:\n{}".format(results["Rototranslator"]))
        click.echo("\nError:\t\t\tx\ty\tz")
        click.echo("   Mean:\t{}".format(results["Error Mean"]))
        click.echo("   Std Dev:\t{}".format(results["Error Std Dev"]))

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
