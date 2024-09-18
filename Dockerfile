# Pull official Python 3.9.7 image.
FROM python:3.9.7

# Set project working directory.
WORKDIR /usr/src/project

# Copy project files to working directory.
COPY . .

# Update Python packages.
RUN pip install --upgrade pip

# Install Python dependencies.
RUN pip install -r requirements.txt
