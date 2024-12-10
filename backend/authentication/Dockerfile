FROM python:3.12.4-bookworm

ARG UID=2000
ARG GID=2000
ENV HOME=/auth_service
ENV PORT=8080

WORKDIR ${HOME}

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" service \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" auth \
  && chown auth:service -R ${HOME}

USER auth

COPY --chown=auth:service /authentication/requirements*.txt ./
COPY --chown=auth:service bin/ ./bin
COPY --chown=auth:service config/ ./config
COPY --chown=auth:service authentication/ .

RUN chmod 0755 bin/* && bin/install

ARG FLASK_APP='app'
ENV FLASK_APP=${FLASK_APP} \
    FLASK_SKIP_DOTENV="true" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH=${HOME}/${FLASK_APP} \
    PATH=/${HOME}/.local/bin:${PATH} \
    USER='auth'

EXPOSE ${PORT}

CMD [ "gunicorn", "-c", "./config/gunicorn.py", "run:app"]
