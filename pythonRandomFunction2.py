import random

# Create a list of possible company names
possible_company_names = ["Acme Corporation", "Google", "Microsoft", "Apple", "Amazon"]

# Create a function to generate a random company name
def generate_random_company_name():
    return random.choice(possible_company_names)

# Generate a random company name
random_company_name = generate_random_company_name()

# Print the random company name
print(random_company_name)
