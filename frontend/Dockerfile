FROM node:22.6.0-slim

ARG UID=1001
ARG GID=1001
ENV HOME=/app
ENV PORT=3000

WORKDIR ${HOME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean \
    && groupadd -g "${GID}" apple \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" spotted \
    && chown spotted:apple -R ${HOME}
    
USER spotted

COPY --chown=spotted:apple bin/ ./bin
COPY --chown=spotted:apple src/package.json ./
COPY --chown=spotted:apple src/package-lock.json ./
COPY --chown=spotted:apple src/. .

RUN chmod 0755 bin/* && bin/install

EXPOSE ${PORT}

CMD ["npm", "run", "dev"]
