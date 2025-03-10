# Use a slim Python image to reduce size
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy application files
COPY ./ /app

# Copy the requirements file separately to leverage Docker caching
COPY ./docker/requirements.txt requirements.txt

# Install required system dependencies for Microsoft ODBC and MySQL client
RUN apt-get update && \
    apt-get install --no-install-recommends --yes\
    unixodbc \
    unixodbc-dev \
    curl \
    libodbc1 \
    odbcinst \
    default-mysql-client \ 
    apt-utils \
    gnupg2 &&\
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

# Download and install msodbcsql18 .deb package 
RUN apt-get update
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list 
    
RUN exit
RUN apt-get update
RUN env ACCEPT_EULA=Y apt-get install -y msodbcsql18 

COPY ./docker/odbc.ini / 
RUN odbcinst -i -s -f /odbc.ini -l
RUN cat /etc/odbc.ini

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the Python path
ENV PYTHONPATH=/app

# Command to run migration script (if needed)
# CMD ["python", "app/main.py"]

