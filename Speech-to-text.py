import pyaudio      #To  capture the Audio
import speech_recognition as SR     #Uses API and convert audio to text
from langdetect import detect, detect_langs


def take_voice_note():
  recognizer = SR.Recognizer()

  mic = SR.Microphone()

  print("Speak: ")

  try:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration = 1)  #Adjust ambiance
        audio = recognizer.listen(source)
        
    print("Processing....")
    text = recognizer.recognize_google(audio)
   #  print(f"You are speaking in {detect_langs(text)}")

   #  with open("9Kar.txt", "a") as file:
   #     file.write(text + "\n")
    print(text)
   #  print(detect(text))

  except Exception as e:
     print("Unable to Listen")
  
if __name__ == "__main__":
   while True:
      
      take_voice_note()
      a = input("Do you want to run again? Give Y for yes and N for no:")

      if (a == "Y") or (a == "y"):
         continue
  

      elif (a == "N") or (a == "n"):
         break

      else:
         print("Invalid Input")


