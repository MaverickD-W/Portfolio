 # use a Python image to start with
FROM python:3.14-slim

# set the working directory to a folder where we can copy and run things
WORKDIR /app

# getting ffmpeg For Debian/Ubuntu-based images
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# copy over requirements.txt
COPY requirements.txt .

# install all the requirements
RUN pip install -r requirements.txt

# copy over the code and the datasets
# TODO: make sure this doesn't break from having data be in a sub-folder
COPY . .

CMD ["panel", "serve", "dashboard_app.py", "--port=5003", "--address=0.0.0.0"]
#CMD panel serve college_app2.py --port=5009 --address=0.0.0.0