Feature: Product catalog
  Manage products through the product API.

  Background:
    Given the following products
      | name        | category | price | availability |
      | Coffee Maker| Kitchen  | 49.99 | true         |
      | Yoga Mat    | Fitness  | 24.5  | true         |
      | Desk Lamp   | Home     | 18.0  | false        |

  Scenario: Reading a Product
    When I click the "Read" button
    Then the text "Coffee Maker" should be present
    And I should see message "Product retrieved successfully"

  Scenario: Updating a Product
    When I update the product name to "Coffee Brewer"
    Then the text "Coffee Brewer" should be present
    And I should see message "Product updated successfully"

  Scenario: Deleting a Product
    When I click the "Delete" button
    Then the text "Coffee Maker" should not be present
    And I should see message "Product deleted successfully"

  Scenario: Listing all products
    When I click the "List All" button
    Then the text "Coffee Maker" should be present
    And I should see message "Products retrieved successfully"

  Scenario: Searching products by category
    Given I filter by category "Kitchen"
    When I click the "Search" button
    Then the text "Coffee Maker" should be present
    And the text "Yoga Mat" should not be present

  Scenario: Searching products by availability
    Given I filter by availability "false"
    When I click the "Search" button
    Then the text "Desk Lamp" should be present
    And the text "Coffee Maker" should not be present

  Scenario: Searching products by name
    Given I filter by name "Yoga"
    When I click the "Search" button
    Then the text "Yoga Mat" should be present
    And the text "Coffee Maker" should not be present
