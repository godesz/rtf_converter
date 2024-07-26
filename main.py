import uvicorn

# pip install fastapi uvicorn python-multipart spire.doc  
# uvicorn main:app --reload

if __name__ == "__main__":
 uvicorn.run("app:app", host="0.0.0.0", port=8000)