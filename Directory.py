import os
import shutil
from termcolor import colored

def directory_name_changer(directory_name):
    new_name = input("Enter new name for the directory: ")
    try:
        os.rename(directory_name, new_name)
        
        print(colored("<Directory's name has been updated successfully!>", color = "green", attrs=["bold", "underline"]))

    except Exception as e:
        print(colored(f"An error has occurred: {e}", "red"))

def directory_checker(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(colored("<<Directory created successfully!>>", color = "green", attrs=["bold", "underline"]))
    else:
        print(colored("Directory is already existing.", "yellow"))
        name_changer = input("Do you want to change its name with the current one? Type Yes or press Enter: ")
        if name_changer == "yes":
            directory_name_changer(directory_name)

def directory_deleter(directory_name):
    if not os.path.exists(directory_name):
        print(colored(f"Directory '{directory_name}' does not exist.", color="yellow", attrs=["bold", "underline"]))
        return
    wish = input(f'Do you want to delete {directory_name} folder? Type "Yes" to agree: ')
    try:
        if wish == "yes":
            shutil.rmtree(directory_name)
            print(colored("<Directory Deleted successfully!>", color="cyan", attrs=["bold", "underline"]))
    except Exception as e:
        print(colored(f"Can't delete this directory! Reason: {e}", "red"))

def directory_manager():
    wants = input('Type "create" to create or "delete" to delete a directory: ')
    try:
        if wants == "create":
            directory_name = input("Enter name for directory: ")
            directory_checker(directory_name)
        elif wants == "delete":
            directory_name = input("Enter name of the directory: ")
            directory_deleter(directory_name)
        else:
            print(colored("Invalid option. Please type 'create' or 'delete'.", color = "red", attrs=["bold", "underline"]))
    except Exception as e:
        print(colored(f"An error occurred: {e}", color = "red", attrs=["bold", "underline"]))

while True:
    if __name__ == "__main__":
        directory_manager()