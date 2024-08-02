FROM python:3.9-slim

ARG UID=1000
ARG GID=1000
ENV HOME=/app
ENV PORT=8501

WORKDIR ${HOME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl libpq-dev software-properties-common \
    gcc make musl-dev \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean \
    && groupadd -g "${GID}" apple \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" spotted \
    && chown spotted:apple -R ${HOME}
    
USER spotted

COPY --chown=spotted:apple requirements*.txt ./
COPY --chown=spotted:apple bin/ ./bin
COPY --chown=spotted:apple . .

RUN chmod 0755 bin/* && bin/install

ENV PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH=${HOME}/.local/bin:${PATH} \
    USER="spotted"

EXPOSE ${PORT}

CMD [ "streamlit", "run", "src/app.py" ]
