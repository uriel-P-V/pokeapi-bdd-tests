from unittest.mock import patch, MagicMock

API_BASE_URL = "https://pokeapi.co/api/v2"


MOCK_PIKACHU_RESPONSE = {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "stats": [
        {
            "base_stat": 35,
            "stat": {
                "name": "hp"
            }
        },
        {
            "base_stat": 55,
            "stat": {
                "name": "attack"
            }
        },
        {
            "base_stat": 90,
            "stat": {
                "name": "speed"
            }
        }
    ],
    "types": [
        {
            "type": {
                "name": "electric"
            }
        }
    ]
}


def mock_pokemon_get(url, **kwargs):

    mock = MagicMock()

    if url == f"{API_BASE_URL}/pokemon/pikachu":
        mock.status_code = 200
        mock.json.return_value = MOCK_PIKACHU_RESPONSE

    elif "/pokemon/invalidpokemon" in url:
        mock.status_code = 404
        mock.text = ""
        mock.json.return_value = {}

    else:
        mock.status_code = 404
        mock.text = ""
        mock.json.return_value = {}

    return mock


def before_scenario(context, scenario):
    print(f"Starting scenario: {scenario.name}")

    if "regression" in scenario.tags:
        context.mock_get = patch("requests.get", side_effect=mock_pokemon_get)
        context.mock_get.start()


def after_scenario(context, scenario):
    print( f"Finished scenario: " f"{scenario.name} - Status: {scenario.status}")

    if "regression" in scenario.tags:
        context.mock_get.stop()