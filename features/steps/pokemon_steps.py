from behave import given, when, then
import requests

API_BASE_URL = "https://pokeapi.co/api/v2"

@given("the Pokemon API is available")
def step_given_api_available(context):
    response=requests.get(f"{API_BASE_URL}/pokemon/pikachu")
    assert response.status_code == 200


@when('I request the pokemon "{name}"')
def step_when_request_pokemon(context, name):
    context.response=requests.get(f"{API_BASE_URL}/pokemon/{name}")


@then("the response status code should be {expected_status:d}")
def step_then_status_code(context, expected_status):
    assert context.response.status_code == expected_status


@then("the basic fields should match:")
def step_then_basic_fields(context):
    data = context.response.json()
    for row in context.table:
        field = row["field"]
        expected_value = row["value"]
        actual_value = data[field]
        if field in ["id", "height", "weight"]:
            expected_value = int(expected_value)
        assert (  actual_value == expected_value ), f"Expected {field} to be {expected_value}, but got {actual_value}"


@then("the stats should match:")
def step_then_stats_match(context):

    data = context.response.json()
    stats_data = {}
    for stat in data["stats"]:
        stat_name = stat["stat"]["name"]
        base_stat = stat["base_stat"]
        stats_data[stat_name] = base_stat
    for row in context.table:
        expected_stat = row["stat"]
        expected_value = int(row["base_stat"])
        assert (stats_data[expected_stat] == expected_value), (
            f"Expected {expected_stat} "
            f"to be {expected_value}, "
            f"but got {stats_data[expected_stat]}"
        )


@then('the pokemon type should be "{expected_type}"')
def step_then_pokemon_type(context, expected_type):
    data = context.response.json()
    pokemon_types = []

    for pokemon_type in data["types"]:
        pokemon_types.append(pokemon_type["type"]["name"]  )

    assert ( expected_type in pokemon_types), (
        f"{expected_type} not found in "
        f"{pokemon_types}"
    )
