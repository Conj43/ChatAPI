# # docker build -t chatbot .
# # docker run -p 5000:5000 chatbot

# FROM continuumio/miniconda3:latest



# WORKDIR /app

# COPY requirements.txt .

# RUN conda init bash && \
#     /bin/bash -c "source ~/.bashrc && conda create -n chatbot_env python=3.9 -y" && \
#     /bin/bash -c "source ~/.bashrc && conda activate chatbot_env && pip install --no-cache-dir -r requirements.txt"

# COPY . .

# EXPOSE 5000

# ENV FLASK_APP=app.py

# CMD ["/bin/bash", "-c", "source ~/.bashrc && conda activate chatbot_env && gunicorn -w 4 -b 0.0.0.0:5000 app:app"]


# Use the official Miniconda3 image as the base
FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Create the Conda environment and install dependencies
RUN conda create -n chatbot_env python=3.9 -y && \
    # Install Python dependencies within the environment
    /opt/conda/envs/chatbot_env/bin/pip install --no-cache-dir -r requirements.txt && \
    # Clean up Conda caches to reduce image size
    conda clean -afy

# Copy the rest of the application code to the container
COPY . .

# Expose port 5000 to allow external access
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
# Prepend the Conda environment's bin directory to the PATH
ENV PATH=/opt/conda/envs/chatbot_env/bin:$PATH

# Optional: Set Gunicorn configuration via environment variables
ENV GUNICORN_CMD_ARGS="--workers 4 --bind 0.0.0.0:5000 --timeout 120"

# Start Gunicorn using the environment's Gunicorn executable
CMD ["gunicorn", "app:app"]

