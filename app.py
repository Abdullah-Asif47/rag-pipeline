import chainlit as cl
import requests

N8N_INGEST_URL = "http://localhost:5678/webhook/ingest-doc"
N8N_QUERY_URL = "http://localhost:5678/webhook/rag-query"

@cl.on_chat_start
async def start():
    await cl.Message(content="Agent initialized. Upload a PDF to ingest data, or ask a question to query the database.").send()

@cl.on_message
async def main(message: cl.Message):
    # 1. Handle PDF Uploads
    if message.elements:
        for element in message.elements:
            if element.mime == "application/pdf":
                processing_msg = cl.Message(content=f"⚙️ Ingesting and vectorizing {element.name}...")
                await processing_msg.send()
                
                # Send the file to n8n
                with open(element.path, "rb") as f:
                    files = {"file": (element.name, f, "application/pdf")}
                    response = requests.post(N8N_INGEST_URL, files=files)
                    
                if response.status_code == 200:
                    processing_msg.content = f"✅ Successfully ingested {element.name} into the vector database!"
                else:
                    processing_msg.content = f"❌ Failed to ingest {element.name}. Check n8n logs."
                await processing_msg.update()
        return  # Stop execution after handling the file

    # 2. Handle Text Queries (RAG)
    payload = {"question": message.content}
    response = requests.post(N8N_QUERY_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", "Error: n8n did not return an 'answer' key.")
        await cl.Message(content=answer).send()
    else:
        await cl.Message(content=f"Error connecting to the AI engine: {response.status_code}").send()