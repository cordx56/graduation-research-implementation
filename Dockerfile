FROM python:3.9

WORKDIR /app

RUN apt update && \
    apt install -y graphviz libgraphviz-dev graphviz-dev pkg-config
RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system

COPY . .

CMD jupyter notebook --ip 0.0.0.0 --allow-root
