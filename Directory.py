import os

def directory_name_changer(directory_name):
   new_name = input("Enter new name for the directory: ")
   try:
      os.rename(directory_name, new_name)
      print("Directory's name has been updated successfully!")
   except:
      print("An error has occured")


def directory_checker(directory_name):
  if not os.path.exists(directory_name):
      os.makedirs(directory_name)
      print("Directory created successfully!")
  else:
      print( "Directory is already existing.")
      name_changer = input("Do you want to change its anme with the currnt one?Type Yes or press Enter: ")
      if name_changer == "Yes":
         directory_name_changer(directory_name)


directory = input("Enter a directory Name: ")
directory_checker(directory)