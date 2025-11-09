import speech_recognition as sr
import ollama

recognizer = sr.Recognizer()

mics = sr.Microphone.list_microphone_names()
print("Available microphones:", mics[0:2])

device_index = 1

try:
    with sr.Microphone(device_index) as source:
        print(f"Using microphone: {mics[device_index]}")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Adjusted for background noise.")

        while True:
            print("\nListening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing...")
                text = recognizer.recognize_google(audio)
                print("Recognized:", text)

                response = ollama.chat(
                    model='deepseek-coder',
                    messages=[{'role': 'user', 'content': text}]
                )

                print(response['message']['content'])

            except sr.WaitTimeoutError:
                print("Unable to detect speech. Trying again...")
            except sr.UnknownValueError:
                print("Unable to detect audio. Please try again.")
except IndexError:(
    print("Unable to find microphone index. Check available devices and update 'device_index'."))
except Exception as e:
    print(f"Unexpected error: {e}")