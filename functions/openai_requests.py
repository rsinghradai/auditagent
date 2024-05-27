from dotenv import dotenv_values
import os 

from functions.database import get_recent_messages

# Load environment variables from .env file
env_variables = dotenv_values('.env')
# Access environment variables
#openai_organization = env_variables.get("OPEN_AI_ORG")
openai_api_key = env_variables.get("OPENAI_API_KEY")

from openai import OpenAI

client = OpenAI(
    api_key = openai_api_key,
)
def convert_audio_to_text(audio_content):
   
    #audio_file= open("/path/to/file/audio.mp3", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_content
)
    print(transcription.text)
    return transcription.text

def get_chat_response(message_input):
    messages= get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)
    print(messages)

    try:
        response = client.chat.completions.create(
                                 model="gpt-3.5-turbo",
                                 messages= messages
                               )
        message_text= response.choices[0].message
        return message_text
        print(message_text)
    except Exception as e:
        print(e)
        return
