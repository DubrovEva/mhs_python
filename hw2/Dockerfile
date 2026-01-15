FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        texlive-latex-base \
        texlive-latex-recommended \
        texlive-pictures \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app/hw2

ENV PYTHONPATH=/app

RUN python -m hw2.task2.generate_table \
    && python -m hw2.task2.generate_report

WORKDIR /app/hw2/artifacts
RUN pdflatex -interaction=nonstopmode report.tex
