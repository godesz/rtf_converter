import re
import html
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from spire.doc import Document, FileFormat
import tempfile
import os
from pydantic import BaseModel

app = FastAPI()

# You can add additional URLs to this list, for example, the frontend's production domain, or other frontends.
allowed_origins = [
    "http://localhost:3000", "http://localhost:3001", "https://localhost:3000", "https://localhost:3001"
]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Requested-With", "Content-Type"],
)


# pip install fastapi uvicorn python-multipart spire.doc  
# uvicorn main:app --reload


def embed_css(html_content, css_file_path):
    with open(css_file_path, 'r') as css_file:
        css_content = css_file.read()
    
    # Embed CSS in the HTML
    html_with_css = html_content.replace('</head>', f'<style>{css_content}</style></head>')
    return html_with_css

def remove_spire_warning(html_content):
    # Remove the Spire.Doc evaluation warning
    pattern = r'Evaluation Warning: The document was created with Spire.Doc for Python.'
    html_content = re.sub(pattern, ' ', html_content, flags=re.DOTALL)
    return html_content
	
def clean_html(html_content):

    # Replace the content type
    html_content = html_content.replace(
        'content="application/xhtml+xml; charset=utf-8"',
        'content="text/html; charset=utf-8"'
    )
    # Unescape HTML entities
    html_content = html.unescape(html_content)
    
    # Remove extra backslashes before quotes
    html_content = html_content.replace('\\"', '"')
    html_content = html_content.replace('<br>\n', '<br>')
        
    # Remove newlines between tags
    html_content = re.sub(r'>\s*\n\s*<', '><', html_content)
    
    return html_content
    
# Create a Pydantic model for the request body
class RTFContent(BaseModel):
    content: str    

def to_raw(string):
    return fr"{string}"    
  

@app.post("/api/convert")
async def convert_rtf_to_html(rtf_content: RTFContent): #(file: UploadFile = File(...)):
    print("Converting...")
    rtf_content.content = rtf_content.content#[1:-1]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, "input.rtf")

        # Write the RTF content to a temporary file
        with open(input_path, "w", encoding='utf8') as buffer:
            buffer.write(rtf_content.content)
            
        output_path = os.path.join(temp_dir, "output.html")
        css_path = os.path.join(temp_dir, "output_styles.css")
        
        print("Spire.start:")
        doc = Document()
        doc.LoadFromFile(input_path, FileFormat.Rtf)
        doc.SaveToFile(output_path, FileFormat.Html)
        doc.Close()
        print("Converted to doc.")
        with open(output_path, 'r', encoding='utf8') as html_file:
            html_content = html_file.read()
        
        html_content = remove_spire_warning(html_content)
        html_content = embed_css(html_content, css_path)
        html_content = clean_html(html_content)
        
        
        
    return {"html_content": html_content }
    
@app.get("/api/test")
async def testing_endpoint():
    return "Health of API is OK"
       