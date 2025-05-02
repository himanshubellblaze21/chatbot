# Use an official lightweight Python image
FROM python:3.12-slim
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the application files into the container
COPY . /app
 
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Expose the port Streamlit or Flask will run on (default 8501 for Streamlit)
EXPOSE 8501
 
# Command to run the application (modify if using Flask/FastAPI)
CMD ["streamlit", "run", "app.py", "--server.maxUploadSize=5", "--server.port=8501", "--server.address=0.0.0.0"]
