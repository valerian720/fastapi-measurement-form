FROM tiangolo/uvicorn-gunicorn-fastapi:latest

# set the working directory
RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
RUN export PYTHONPATH=$PWD

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY . /app

# start the server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]