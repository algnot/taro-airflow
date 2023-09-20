FROM python:3.9

WORKDIR /src

COPY . .

RUN pip install --no-cache-dir -r requirement.txt

CMD [ "python", "index.py" ]