FROM python:3.9

WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml ./
RUN pip install poetry && poetry install

COPY . .

CMD [ "poetry", "run", "python", "main.py"]