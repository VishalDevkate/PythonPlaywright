Feature: create order and verify details
  test scenarios for create order and associated details

  Scenario Outline: verify Thanks you for shopping message on order details page
    Given order created through API with <username> and <password>
    When user is on login page
    And user logs in with <username> and <password>
    And user navigates to orders page
    And user clicks on latest order
    Then Thank you for shopping message is displayed
    Examples:
      | username         | password          |
      | v.d@gmail.com    | RahulShetty@2026  |
      | anshika@gmail.com| Iamking@000       |