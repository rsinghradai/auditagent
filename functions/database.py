import json
import random

def get_recent_messages():
    file_name= "stored_data.json"
    learn_instruction= {
        "role": "system",
        "content":" You are interviewing a user for credit card payment security audit. Ask short questions that are relevant for PCI DSS compliance in the topic of Network Security and then build on the conversation. Your name is Ajay. The user is called Sukant. Keep your answers to under 30 words"
    }

    messages= []

    #Add a random element
    x= random.uniform(0,1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some dry humour."

    messages.append(learn_instruction)

    #get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)
            # Append last 5 items of the data
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)

    except Exception as e:
        print(e)

    return messages

#store messages
def store_messages(request_message, response_message):

    file_name="stored_data.json"

    messages= get_recent_messages()[1:]

    user_message= {"role":"user", "content": request_message}
    assistant_message= {"role":"assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)
    print(messages)

    #save message in json
    with open(file_name, "w") as f:
        json.dump(messages, f)

def reset_messages():
    #overwrite current file with nothing
    open("stored_data.json","w")