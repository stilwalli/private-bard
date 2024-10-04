## Webapp using FASTAPI#
import subprocess
import os

from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import google
import json

from google.auth import default
from google.cloud import storage


import logging

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static") 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get credentials automatically
credentials, project_id = default()
print ("project_id: ", project_id)

@app.get("/hello")
async def hello_get():
  """
  This is a simple GET request that returns "Hello, world!"
  """
  return {"message": "Hello, world!"}

@app.post("/hello")
async def hello_post(name: str): 
  """
  This is a simple POST request that takes a name as input and 
  returns a greeting.
  """
  return {"message": f"Hello, {name}!"}


@app.post("/hello2")
async def hello_post(request: Request):
    data = await request.json() 
    name = data.get("name") 
    if name:
        return {"message": f"Hello, {name}!"}
    else:
        return {"error": "Name is missing in the request body"}

#curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{"name": "write about India"}' https://private-bard-906035941682.us-central1.run.app/callPrivateGemini 
#curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{"name": "write about India"}' https://private-bard-906035941682.us-central1.run.app/callPrivateGemini 
#curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" d '{"user_prompt": "write about India"}' "https://private-bard-906035941682.us-central1.run.app/callPrivateGemini"


@app.post("/callPrivateGemini")
async def callPrivateGemini(request: Request):
    """Lists all file names in the specified GCP bucket and returns them as JSON."""
    try:
        MODEL_ID = "gemini-1.5-flash-002"  # @param {type:"string"}
        model = GenerativeModel(MODEL_ID)
        # Load a example model with system instructions
        example_model = GenerativeModel(
            MODEL_ID,
            system_instruction=[
                "Your mission is to help users with their questions.",
            ],
        )
        data = await request.json() 
        user_prompt = data.get("user_prompt") 

        print ("user_prompt: ", user_prompt)
        
        if not user_prompt:
            return {"error": "Missing 'user_prompt' field in request body"}

    # Set model parameters
        generation_config = GenerationConfig(
            temperature=0.9,
            top_p=1.0,
            top_k=32,
            candidate_count=1,
            max_output_tokens=8192,
        )

        # Set safety settings
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }

        #prompt = {user_prompt}

        # Set contents to send to the model
        contents = [user_prompt]
        print ("Content: " , contents)
        # Counts tokens
        #print(example_model.count_tokens(contents))

        # Prompt the model to generate content
        response = example_model.generate_content(
            contents,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        # Print the model response
        print(f"\n{response.text}")
        return {"translated_text": response.text}
        #print(f'\nUsage metadata:\n{response.to_dict().get("usage_metadata")}')
        #print(f"\nFinish reason:\n{response.candidates[0].finish_reason}")
        #print(f"\nSafety settings:\n{response.candidates[0].safety_ratings}")

    
    except Exception as e:
        return json.dumps({"error": str(e)})  # Return error as JSON



@app.get("/")
async def main(request: Request):
    return JSONResponse(content={"Available APIs": ["/getBuckets", "/getFilesFromBucket/{bucket_name}"]}, status_code=200)




#callPrivateGemini()