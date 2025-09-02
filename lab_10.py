import requests, pyttsx3, pyaudio, vosk, json
from PIL import Image
from io import BytesIO

#голосовой движок
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Английский голос

#распознавание речи
model = vosk.Model(r"C:\Users\Main\Desktop\vosk-model")
recognizer = vosk.KaldiRecognizer(model, 16000)

#аудиопоток
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

#для изображения
current_img = {"url": "", "breed": ""}

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    print("Listening...")
    while True:
        if recognizer.AcceptWaveform(stream.read(4000, exception_on_overflow=False)):
            if command := json.loads(recognizer.Result()).get("text", "").lower():
                print(f"You said: {command}")
                return command

def get_dog():
    try:
        if (resp := requests.get("https://dog.ceo/api/breeds/image/random")).ok:
            current_img.update(url=resp.json()["message"], breed=resp.json()["message"].split("/")[-2])
            return True
    except Exception as e:
        print(f"Error: {e}")
    return False

def process(cmd):
    if "show" in cmd or "next" in cmd or "another" in cmd:
        if get_dog():
            try:
                img = Image.open(BytesIO(requests.get(current_img["url"]).content))
                img.show()
                speak("Here's a dog" + (f", breed: {current_img['breed']}" if "breed" in cmd else ""))
            except Exception as e:
                speak(f"Error: {e}")
    
    elif "save" in cmd and current_img["url"]:
        try:
            with open(f"dog_{current_img['breed']}.jpg", "wb") as f:
                f.write(requests.get(current_img["url"]).content)
            speak("Image saved")
        except Exception as e:
            speak(f"Save error: {e}")
    
    elif "exit" in cmd or "stop" in cmd:
        speak("Goodbye!")
        exit()
    
    else:
        speak("Command not recognized")

if __name__ == "__main__":
    speak("Hello, friend! My commands: show, save, next, breed, exit")
    while True:
        try:
            process(listen())
        except Exception as e:
            print(f"Critical error: {e}")
            break
    stream.close()
    p.terminate()