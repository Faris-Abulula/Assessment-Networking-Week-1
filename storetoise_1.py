"""The Storetoise CLI."""

from argparse import ArgumentParser, Namespace
import requests

BASE_URL = "http://sigma-storetoise-lb-698404422.eu-west-2.elb.amazonaws.com"


def valid_number(number: str | None) -> int | None:
    """Checks if input number is between 0 and 1000"""
    if number:
        if number.isdigit() and 0 < int(number) <= 1000:
            return int(number)

        print("Number must be an integer between 0 and 1000.")
    return None


def load_storetoise_data(url: str) -> dict:
    """Returns the data from the Storetoise API"""
    response = requests.get(url, timeout=10)

    return response.json()


def list_storage_ids(data: dict, number: int | None = None) -> None:
    """Returns the ids stored in the username"""
    storage_ids = data["ids"]

    if number:
        limit = min(number, len(storage_ids))
        storage_ids = storage_ids[:limit]

    for storage_id in sorted(storage_ids):
        print(storage_id)


def command_line_inputs() -> Namespace:
    """Inputs from the command line"""
    parser = ArgumentParser(description="Storetoise CLI")

    parser.add_argument("--username", "-u", required=True,
                        help="Username for Storetoise")

    parser.add_argument("--number", "-n",
                        type=valid_number,
                        help="Limit the number of results")

    return parser.parse_args()


if __name__ == "__main__":
    args = command_line_inputs()

    user_url = f"{BASE_URL}/storage/{args.username}"
    ids_data = load_storetoise_data(user_url)

    list_storage_ids(ids_data, args.number)
