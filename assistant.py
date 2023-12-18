import os
import time
from openai import OpenAI, NotFoundError, BadRequestError

from dotenv import load_dotenv


load_dotenv(override=True)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
ASSISTANT_ID=os.environ["Assistant_ID"]

class BrochureAssistant:
   def __init__(self):
      pass
   
   def create_new_thread(self):
      thread=client.beta.threads.create()
      return thread
   
   def retrieve_thread(self,thread_id: str):
      try:
         my_thread = client.beta.threads.retrieve(thread_id=thread_id)
         return my_thread
      except NotFoundError:
         return None

   def add_new_message_to_thread(self,query:str,thread_id):
      try:
         message = client.beta.threads.messages.create(
            thread_id= thread_id,
            role="user",
            content= query
         )
         return {
            "error": None,
            "message":message
         }
      except BadRequestError as e:
         print(e)
         return {
            "error": e.message,
            "message":None
         }

   def run_thread(self,thread_id:str):
      run = client.beta.threads.runs.create(
         thread_id=thread_id,
         assistant_id=ASSISTANT_ID
      )
      return run
   
   def check_run_status(self, thread_id:str, run_id:str):
      try:
         run = client.beta.threads.runs.retrieve(
               thread_id=thread_id,
               run_id=run_id
            )
         return run
      except NotFoundError:
         return None
   
   def retreive_assistant_response(self,thread_id):
      try:
         messages = client.beta.threads.messages.list(
               thread_id=thread_id,
               limit=100
            )
         return messages
      except NotFoundError:
         return None
   
   def retreive_assistant_new_response(self,thread_id: str, before: str):
      try:
         messages = client.beta.threads.messages.list(
               thread_id=thread_id,
               limit=100,
               before=before
            )
         return messages
      except NotFoundError:
         return None

# assistant = BrochureAssistant()
# thread = assistant.create_new_thread()
# if thread:
#    thread_id = thread.id
# print(thread_id)
# message = assistant.add_new_message_to_thread(query="hey",thread_id=thread_id)
# print(message)
# run = assistant.run_thread(thread_id=thread_id)
# print(run)
# time.sleep(0.5)
# print(run)
# message = assistant.add_new_message_to_thread(query="Hello",thread_id=thread_id)
# print(message)
# run2 = assistant.run_thread(thread_id=thread_id)
# print(run2)

# while True:
#    query = input("You: ")
#    if thread_id:
#       # Add new message to thread and run it
#       message = assistant.add_new_message_to_thread(query=query,thread_id=thread_id)
#       print(message)
#       run = assistant.run_thread(thread_id=thread_id)
#       while True:
#          status = assistant.check_run_status(thread_id=thread_id,run_id=run.id)
#          print("status: ",status)
#          if status == "completed":
#             print("status: ", status)
#             break
#          elif status == "cancelled" or status == "cancelling" or status == "expired" or status == "failed":
#             print("status: ", status)
#             break
#          time.sleep(2)
#       if status == "completed":
#          response = assistant.retreive_assistant_response(thread_id=thread_id)
#          print(response)
#       print(f"Assistant: {response.data[0].content[0].text.value}")

# response = assistant.retreive_assistant_one_response(thread_id="thread_Hj1354mueGpcppO7eJ6vBifo",before="msg_jg2amXqsgEv5yMex7q7uKxVp")
# response = assistant.retreive_assistant_response(thread_id="thread_Hj1354mueGpcppO7eJ6vBifo")
# print(response)