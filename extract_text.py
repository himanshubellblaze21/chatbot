import boto3
import os
import fitz  # PyMuPDF for PDF extraction
import docx

s3_client = boto3.client("s3")

def extract_text(file_name, file_type, s3_bucket):
    """Download file from S3 and extract text from a PDF or DOCX file."""

    # Ensure a correct temporary directory
    temp_dir = os.path.join(os.getcwd(), "temp_files")
    os.makedirs(temp_dir, exist_ok=True)  # Create temp folder if not exists
    local_path = os.path.join(temp_dir, file_name)

    # Download file from S3
    s3_client.download_file(s3_bucket, file_name, local_path)

    text = ""

    try:
        if file_type == "pdf":
            # Use `with` statement to ensure proper closure of the file
            with fitz.open(local_path) as doc:
                text = "\n".join([page.get_text("text") for page in doc])

        elif file_type == "docx":
            # Read DOCX file properly
            doc = docx.Document(local_path)
            text = "\n".join([para.text for para in doc.paragraphs])

    except Exception as e:
        print(f"❌ Error extracting text: {e}")

    finally:
        # Ensure the file is closed before deleting it
        if os.path.exists(local_path):
            try:
                os.remove(local_path)
            except PermissionError:
                print(f"⚠️ Could not delete {local_path}, it may still be in use.")

    return text