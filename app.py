import click, pwinput, string
from firebase_auth import *

# Helper functions

def validate_password():

    while True:
        password = pwinput.pwinput("Enter your password: ")
        if len(password) < 8:
            print(f"\nPassword too short must be atleast 8 characters long.\n")
            continue
        
        lower, upper, punc, num = 0, 0, 0, 0

        for c in password:
            if c.isupper():
                upper += 1
            elif c.islower():
                lower += 1
            elif c in string.punctuation:
                punc += 1
            elif c.isdigit():
                num += 1
        
        if lower == 0 or upper == 0 or punc == 0 or num == 0:
            print("\nPassword must have atleast one lowercase letter.\nPassword must have atleast one uppercase letter.\nPassword must have atleast one punctuation.\nPassword must have atleast one number.\n")
            continue
        
        break
    
    return password

def validate_email():
    while True:
        email = input("Enter your email: ")

        if '@' not in email or '.' not in email:
            print("Please enter a valid email address.")
            continue

        break
    return email
@click.command()
def register():
    data = {
        "name": input("Enter your full name: "),
        "email": validate_email(),
        "password": validate_password(),
        "role": input("Enter your role(mentor/student): "),
        "expertise": input("Enter your expertise: ")
    }

    if signup(data):
        print("You have been successfully registered.")

@click.command()
def login():

    data = {
        "email": validate_email(),
        "password": validate_password()
    }

    if signin(data):
        print("You have successfully logged in.")

@click.group()
def cli():
    print("Works")

cli.add_command(register)
cli.add_command(login)

if __name__ == "__main__":
    cli()
