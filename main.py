from fastapi import FastAPI, File, UploadFile,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
#from decouple import config
import openai

# Custom import functions
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

app = FastAPI()

#CORS
origins=[
    "https://localhost:5173",
    "http://localhost:5274",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000"
]

#CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

@app.get("/health")
async  def check_health():
    return{"message": "Healthy"}

@app.get("/reset")
async  def reset_conversations():
    reset_messages()
    return{"message": "Conversations reset"}



#Get audio 
@app.get("/post-audio-get/")
async def get_audio():
    #get saved audio
    audio_input= open("Record_hi.mp3","rb")

    #Decode audio
    message_decoded= convert_audio_to_text(audio_input)
    print(message_decoded)
    chat_response= get_chat_response(message_decoded)
    print(chat_response)

    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get a chat response")
    #store messages
    store_messages(message_decoded, chat_response.content)

    # convert chat response to audio
    audio_output= convert_text_to_speech(chat_response.content)

    #Guard: Ensure there is audio from elevenlabs
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven Labs response")
    
    #create a generator that yields chunks of data
    def iterfile():
        yield audio_output 
        
    return StreamingResponse(iterfile(), media_type="audio/mpeg")


# Post bot response
# Note : Not playing in browser when using post request
@app.post("/post-audio/")
async def post_audio( file: UploadFile = File(...)):
    print("hello")