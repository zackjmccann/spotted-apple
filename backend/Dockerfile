FROM python:3.12.4-bookworm

ARG UID=1000
ARG GID=1000
ENV HOME=/server
ENV PORT=8000

WORKDIR ${HOME}

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
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

ARG FLASK_DEBUG="false"
ENV FLASK_DEBUG="${FLASK_DEBUG}" \
    FLASK_APP="src.app" \
    FLASK_SKIP_DOTENV="true" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH=${HOME}:${HOME}/app:/app \
    PATH=/${HOME}/.local/bin:${PATH} \
    USER="spotted"

EXPOSE ${PORT}

CMD [ "gunicorn", "-c", "./config/gunicorn.py", "run:app"]
