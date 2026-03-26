import sys
import click
from api import get_location_by_zipcode, get_current_location, get_weather, get_air_quality


@click.group()
def cli():
    """Weather CLI — get location and current weather conditions."""
    pass


@cli.command("where-is")
@click.option("--zipcode", default=None, help="US zip code to look up.")
def where_is(zipcode):
    """Display the city and state for a given location."""
    try:
        if zipcode:
            loc = get_location_by_zipcode(zipcode)
            click.echo(f"{zipcode} is in {loc['city']}, {loc['state']}.")
        else:
            loc = get_current_location()
            click.echo(f"Your current location is {loc['city']}, {loc['state']}.")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except RuntimeError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


@cli.command("current")
@click.option("--zipcode", default=None, help="US zip code to get weather for.")
def current(zipcode):
    """Display the current temperature and weather conditions."""
    try:
        if zipcode:
            loc = get_location_by_zipcode(zipcode)
        else:
            loc = get_current_location()
        weather = get_weather(loc["lat"], loc["lon"])
        temp = weather["temperature_f"]
        condition = weather["condition"]
        click.echo(
            f"It is currently {temp}ºF, and {condition} in {loc['city']}, {loc['state']}."
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except RuntimeError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


@cli.command("aqi")
@click.option("--zipcode", default=None, help="US zip code to get air quality for.")
def aqi(zipcode):
    """Display the current air quality index (US AQI)."""
    try:
        if zipcode:
            loc = get_location_by_zipcode(zipcode)
        else:
            loc = get_current_location()
        air = get_air_quality(loc["lat"], loc["lon"])
        click.echo(
            f"The air quality in {loc['city']}, {loc['state']} is {air['aqi']} ({air['category']})."
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except RuntimeError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
