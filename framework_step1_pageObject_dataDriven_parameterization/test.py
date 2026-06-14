import json
import pytest

# Your extracted JSON data structure
json_data = {
    'user_credentials': [
        {'userEmail': 'v.d@gmail.com', 'userPassword': 'RahulShetty@2026'},
        {'userEmail': 'anshika@gmail.com', 'userPassword': 'Iamking@000'}
    ]
}

# Argument 1: "data_variable_name" (String matching your test function parameter)
# Argument 2: The actual list of dictionary items
@pytest.mark.parametrize("user_credentials", json_data['user_credentials'])
def test_API_plus_UI_e2e_test_ecommerce(user_credentials, playwright):
    # Now you can easily extract individual data variables per test iteration:
    email = user_credentials['userEmail']
    password = user_credentials['userPassword']

    print(f"Running test iteration for: {email}")