# This is the RESTful api for the chatbot.
from fastapi import FastAPI, Path, Body, HTTPException
from rag import RAG_chat
app = FastAPI()

chatbot = RAG_chat()

@app.post("/ingest/pdf")
async def ingest_pdf(file_path: str = Body(...)):
    try:
        chatbot.ingest_pdf(file_path)
        return {"message": "PDF ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to ingest PDF: {str(e)}")

@app.post("/ingest/web")
async def ingest_web(urls: list[str] = Body(...)):
    try:
        chatbot.ingest_web(urls)
        return {"message": "Web pages ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to ingest web pages: {str(e)}")

@app.post("/ask")
async def ask(question: str = Body(...)):
    if not chatbot.chain:
        raise HTTPException(status_code=400, detail="No document ingested yet.")

    try:
        answer = chatbot.ask(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {str(e)}")

@app.get("/clear")
async def clear():
    chatbot.clear()
    return {"message": "Cleared chatbot state."}