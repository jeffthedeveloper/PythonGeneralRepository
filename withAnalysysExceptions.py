def withdraw(amount):
  try:
    account_balance = 1000
    if amount > account_balance:
      raise ValueError("Insufficient funds")
    elif not isinstance(amount, int):
      raise TypeError("Amount must be an integer")
    print(str(amount) + " withdrawn!")
  except ValueError as e:
    print(e)
  except TypeError as e:
    print(e)

# Add a finally block to clean up any resources that were opened in the try block
finally:
  # Do something to clean up resources, such as closing a file
  pass

# Get the amount to withdraw from the user
amount = int(input("Enter the amount to withdraw: "))

# Withdraw the amount from the user's account
withdraw(amount)
