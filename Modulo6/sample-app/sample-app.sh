#!/bin/bash
# Step 1: Create temporary directories to store the website files
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

# Step 2: Copy the website directories and sample_app.py to the temporary directory
cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

# Step 3: Create a Dockerfile
echo "FROM python" >> tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile

echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  sample_app.py /home/myapp/" >> tempdir/Dockerfile

echo "EXPOSE 8080" >> tempdir/Dockerfile
echo "CMD python /home/myapp/sample_app.py" >> tempdir/Dockerfile

# Step 4: Build the Docker container.
cd tempdir
docker build -t sampleapp .

# Step 5: Start the container and verify it is running.
docker run -t -d -p 8080:8080 --name samplerunning sampleapp

docker ps -a
