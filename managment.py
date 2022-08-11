import click

from src.db.database import get_db
from src.integrations.integrations import IntegrationAPI
from src.integrations.providers import JSONPlaceHolderProvider


@click.command()
@click.option("--confirm", is_flag=True, help="Confirm the operation")
def run_integration(confirm):
    """Simple command line interface to run the JSON Placeholder
    integration to retrieve and insert the data to our DB.
    :return: Dict
    """
    if confirm:
        db = next(get_db())
        provider = JSONPlaceHolderProvider()
        integration = IntegrationAPI(db=db, provider=provider)
        data = integration.sync()
        click.echo(data)
    else:
        click.echo("You must to confirm the operation using --confirm.")


if __name__ == "__main__":
    run_integration()
