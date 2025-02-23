from litellm import completion
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def get_completion():
    response = completion(
      model="openai/gpt-4o-mini-2024-07-18",
      messages=[{ "content": "Hello, how are you?","role": "user"}]
    )
    return response.choices[0].message.content

def get_json(schema, prompt, user_input):
    response = completion(
      model="gpt-4o",
      messages=[{"content" : prompt, "role": "system"}, { "content": user_input ,"role": "user"}],
      response_format=schema
    )
    return response.choices[0].message.content