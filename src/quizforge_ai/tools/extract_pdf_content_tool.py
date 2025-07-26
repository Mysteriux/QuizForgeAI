from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import PyPDF2

class ExtractPDFContentToolInput(BaseModel):
    pdf_path: str = Field(description="the path of the pdf file to extract content from", default="")

class ExtractPDFContentTool(BaseTool):
    
    """
    This tool is used to extract content from a PDF file.
    """
    name: str = "Extract PDF Content"
    description: str = "Extract text content from a PDF file."
    args_schema: Type[BaseModel] = ExtractPDFContentToolInput


    def _run(self, pdf_path: str) -> str:
        try:
          with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    # Split the text into words and join with newlines
                    words = page_text.split()
                    text += " ".join(words)
            return text.strip()
        except Exception as e:
            return f"Error extracting PDF content: {str(e)}"
