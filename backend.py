from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import google.generativeai as genai
import os 
from dotenv import load_dotenv
import os
app = FastAPI()

load_dotenv()

# load_dotenv(dotenv_path='./.env')

API_KEY=os.getenv('API_KEY')
# Define your Gemini API key and model

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class Query(BaseModel):
    text: str = Field("", description="The text to summarize or improve grammar")
    topic: str = Field("", description="The topic for information retrieval")
    text_to_be_improved: str = Field("", description="The text to correct grammar")
    recipient: str = Field("", description="Recipient's email address")
    subject: str = Field("", description="Subject of the email")
    body: str = Field("", description="Body of the email")

# Function to generate content out of prompt using Gemini API
def call_gemini_api(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grammar/")
async def improve_grammar(query: Query):
    """
    Improve the grammar of the given text.
    """
    if not query.text_to_be_improved:
        raise HTTPException(status_code=400, detail="No text provided for grammar improvement.")
    
    new_prompt = f"""
    Improve the grammar of the below text:
    ```{query.text_to_be_improved}```
    """
    improved_text = call_gemini_api(new_prompt)
    return {"text_to_be_improved": improved_text}

@app.post("/summarize/")
async def summarize(query: Query):
    """
    Summarize the given text into points not exceeding 70 words.
    """
    if not query.text:
        raise HTTPException(status_code=400, detail="No text provided for summarization.")
    
    new_prompt = f"""
    Summarize the below given text into points not exceeding more than 70 words:
    ```{query.text}```
    """
    summary = call_gemini_api(new_prompt)
    return {"summary": summary}

@app.post("/information/")
async def get_information(query: Query):
    """
    Provide relevant information about the given topic.
    """
    if not query.topic:
        raise HTTPException(status_code=400, detail="No topic provided for information retrieval.")
    
    new_prompt = f"""
    Provide relevant and recent information about the below topic in brief:
    ```{query.topic}```
    """
    information = call_gemini_api(new_prompt)
    return {"information": information}

@app.post("/generate_mail/")
async def generate_mail(query: Query):
    """
    Generate a formatted email from the provided recipient, subject, and body.
    """
    if not (query.recipient and query.subject and query.body):
        raise HTTPException(status_code=400, detail="Recipient, subject, and body must be provided.")
    
    prompt = f"""
    Generate the below mail 
    To: {query.recipient}
    Subject: {query.subject}
    
    {query.body}
    """
   
    mail_content=call_gemini_api(prompt)
    return {"mail_content": mail_content}