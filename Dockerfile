FROM python:3.10

RUN mkdir docker-snapchat-filters 
WORKDIR /docker-snapchat-filters

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]