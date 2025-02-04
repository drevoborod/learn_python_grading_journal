# uv export && pip install
# envs for Python (disable buffer output)

FROM python:3.12-slim

RUN apt-get update; apt-get install -y --no-install-recommends make; \
	rm -rf /var/lib/apt/lists/*
RUN pip install uv

WORKDIR /app

COPY pyproject.toml /app/
COPY uv.lock /app/

RUN uv export > deps.txt && pip install -r deps.txt

COPY grading_journal /app/grading_journal
COPY Makefile /app/

ENTRYPOINT []
CMD ["make", "run"]