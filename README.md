# pokeapi-bdd-tests

![CI](https://github.com/uriel-P-V/pokeapi-bdd-tests/actions/workflows/tests.yml/badge.svg)

A BDD-based test suite for the PokéAPI —
demonstrates deep contract validation with Behave and Gherkin,
testing nested JSON structures, typed field comparison,
and mock-based regression testing with a single patch.

---

## Project Structure

```
pokeapi-bdd-tests/
├── .github/
│   └── workflows/
│       └── tests.yml          ← GitHub Actions CI
├── features/
│   ├── steps/
│   │   └── pokemon_steps.py   ← All step definitions
│   ├── environment.py         ← Hooks and mock setup
│   └── pokemon.feature        ← 5 deep BDD scenarios
└── requirements.txt
```

---

## Features

- **Deep contract validation** — validates nested fields, typed values, and lists
- **Stats validation** — verifies specific base stat values from nested list structures
- **Type validation** — verifies pokemon type from nested list
- **Single mock** — one `patch("requests.get")` with URL discrimination
- **Tag-driven execution** — `@smoke` hits real API, `@regression` fully mocked
- **GitHub Actions CI** — smoke runs first, regression only if smoke passes

---

## BDD Scenarios

```gherkin
Feature: Pokemon API

  Background:
    Given the Pokemon API is available

  @smoke
  Scenario: Get Pikachu by name
    When I request the pokemon "pikachu"
    Then the response status code should be 200

  @regression
  Scenario: Validate base stats
    When I request the pokemon "pikachu"
    Then the stats should match:
      | stat    | base_stat |
      | hp      | 35        |
      | attack  | 55        |
      | speed   | 90        |

  @regression
  Scenario: Request invalid pokemon
    When I request the pokemon "invalidpokemon"
    Then the response status code should be 404
```

---

## Mock Strategy

Single `patch("requests.get")` with URL discrimination —
returns Pikachu mock data for valid requests, 404 for anything else.

```python
def mock_pokemon_get(url, **kwargs):
    mock = MagicMock()
    if url == f"{API_BASE_URL}/pokemon/pikachu":
        mock.status_code = 200
        mock.json.return_value = MOCK_PIKACHU_RESPONSE
    else:
        mock.status_code = 404
        mock.text = "Not Found"
    return mock
```

---

## Setup

```bash
git clone https://github.com/uriel-P-V/pokeapi-bdd-tests.git
cd pokeapi-bdd-tests
pip install -r requirements.txt
behave
```

---

## Running Tests

```bash
# All scenarios
behave

# Smoke only — hits real PokéAPI
behave --tags=smoke

# Regression only — fully mocked, no internet required
behave --tags=regression
```

---

## CI/CD Pipeline

Two dependent jobs run on every push and pull request to `main`:

```
push / PR → smoke (1 scenario) → regression (4 scenarios)
```

If `smoke` fails, `regression` is skipped automatically.

---

## Tech Stack

- **Python 3.11+**
- **Behave** — BDD framework with Gherkin support
- **Requests** — HTTP client for API calls
- **unittest.mock** — patch, MagicMock, side_effect
- **GitHub Actions** — CI/CD pipeline

---

## Author

**Uriel Alejandro Pérez Valdovinos**  
[github.com/uriel-P-V](https://github.com/uriel-P-V) · [linkedin.com/in/uriel-pv](https://linkedin.com/in/uriel-pv)