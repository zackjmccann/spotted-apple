FROM python:3.12.4-bookworm

ARG UID=1000
ARG GID=2000
ENV HOME=/ops_service
ENV PORT=8000

WORKDIR ${HOME}

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" service \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" ops \
  && chown ops:service -R ${HOME}

USER ops

COPY --chown=ops:service /operations/requirements*.txt ./
COPY --chown=ops:service bin/ ./bin
COPY --chown=ops:service config/ ./config
COPY --chown=ops:service /operations .

RUN chmod 0755 bin/* && bin/install

ARG FLASK_APP='app'
ENV FLASK_APP=${FLASK_APP} \
    FLASK_SKIP_DOTENV="true" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH=${HOME}/${FLASK_APP} \
    PATH=/${HOME}/.local/bin:${PATH} \
    USER="ops"

EXPOSE ${PORT}

CMD [ "gunicorn", "-c", "./config/gunicorn.py", "run:app"]
