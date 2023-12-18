from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from schema import ThreadResponse,MessageRequest, MessageResponse, StatusResponse, RetrieveResponse, Message
from assistant import BrochureAssistant
app = FastAPI(
    title="Pdf assistant"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
assistant = BrochureAssistant()
# Create new thread and return thread id
@app.get("/create_thread", response_model=ThreadResponse)
def create_thread():
    try:
        thread = assistant.create_new_thread()
        print(thread)
        return ThreadResponse(thread_id=thread.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Get a query and thread id and return thread id and run id
@app.post("/send_message", response_model=MessageResponse)
def send_message(request: MessageRequest):
    try: 
        thread = assistant.retrieve_thread(thread_id=request.thread_id)
        if not thread:
            HTTPException(status_code=404,detail="Thread with this id not found")

        # Add new message to thread
        message = assistant.add_new_message_to_thread(query=request.query, thread_id=request.thread_id)
        if message["error"]:
            HTTPException(status_code=400,detail=message["error"])
        
        # Run the thread
        run = assistant.run_thread(thread_id=request.thread_id)

        return MessageResponse(thread_id=run.thread_id,run_id=run.id,message_id=message["message"].id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get run id and thread id and return the status with message (if there is any error)
@app.get("/check_status/{thread_id}/{run_id}",response_model=StatusResponse)
def check_status(thread_id: str, run_id: str):
    try:
        run = assistant.check_run_status(thread_id, run_id)
        if not run:
            HTTPException(status_code=404,detail="Thread or run with this id not found")
        if run.status in ["completed" ,"queued" ,"in_progress" ,"cancelling"]:
            return StatusResponse(status= run.status)
        else:
            return StatusResponse(
                status=run.status,
                error_message=run.last_error.message
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get thread id and return the the list of messages
@app.get("/retrieve_responses/{thread_id}",response_model=RetrieveResponse)
def retrieve_responses(thread_id: str):
    try:
        messages = assistant.retreive_assistant_response(thread_id)
        if not messages:
            HTTPException(status_code=404,detail="Thread with this id not found")
        messages = [ Message(role=message.role,content=message.content[0].text.value) for message in messages].reverse()
        return RetrieveResponse(messages=messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/retrieve_message_responses/{thread_id}/{message_id}",response_model=Message)
def retrieve_message_responses(thread_id: str,message_id: str):
    try:
        messages = assistant.retreive_assistant_new_response(thread_id=thread_id,before=message_id)
        if not messages:
            HTTPException(status_code=404,detail="Thread with this id not found")
        print(list(messages.data))
        first_message = messages.data[-1]
        return Message(role=first_message.role,content=first_message.content[0].text.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))