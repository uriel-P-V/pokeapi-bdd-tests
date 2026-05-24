Feature: Pokemon API

  Background:
    Given the Pokemon API is available

  @smoke
  Scenario: Get Pikachu by name
    When I request the pokemon "pikachu"
    Then the response status code should be 200

  @regression
  Scenario: Validate basic fields
    When I request the pokemon "pikachu"
    Then the basic fields should match:
      | field  | value   |
      | id     | 25      |
      | name   | pikachu |
      | height | 4       |
      | weight | 60      |

  @regression
  Scenario: Validate base stats
    When I request the pokemon "pikachu"
    Then the stats should match:
      | stat    | base_stat |
      | hp      | 35        |
      | attack  | 55        |
      | speed   | 90        |

  @regression
  Scenario: Validate pokemon type
    When I request the pokemon "pikachu"
    Then the pokemon type should be "electric"

  @regression
  Scenario: Request invalid pokemon
    When I request the pokemon "invalidpokemon"
    Then the response status code should be 404