Convert RTF to HTML.

# Install 
pip install fastapi uvicorn python-multipart spire.doc  

# Run
uvicorn main:app --reload

# Fetch
url: http://localhost:8000/api/convert
body: RTF file as string
