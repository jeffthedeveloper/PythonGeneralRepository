import random

# Create a list of possible street names
possible_street_names = ["Main Street", "Broadway", "Park Avenue", "Wall Street", "Oak Street"]

# Create a list of possible city names
possible_city_names = ["New York", "Los Angeles", "Chicago", "Houston", "Philadelphia"]

# Create a list of possible state names
possible_state_names = ["New York", "California", "Illinois", "Texas", "Pennsylvania"]

# Create a list of possible zip codes
possible_zip_codes = ["10001", "90001", "60601", "77001", "19101"]

# Create a function to generate a random address
def generate_random_address():
    return f"{random.choice(possible_street_names)}, {random.choice(possible_city_names)}, {random.choice(possible_state_names)} {random.choice(possible_zip_codes)}"

# Generate a random address
random_address = generate_random_address()

# Print the random address
print(random_address)
