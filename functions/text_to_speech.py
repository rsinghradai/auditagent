import requests

from dotenv import dotenv_values
import os 

# Load environment variables from .env file
env_variables = dotenv_values('.env')
# Access environment variables
#Eleven labs api key 
ELEVEN_LABS_API_KEY = env_variables.get("ELEVEN_LABS_API_KEY")

def convert_text_to_speech(message):

    #define data ( body)
    body= {
        "text":message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
        }
    }

#Define Voice
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"

    headers={"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept":"audio/mpeg"}
    endpoint= f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"
    
    #send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return 
    
    #handle response
    if response.status_code==200:
        return response.content
    else:
        return 

