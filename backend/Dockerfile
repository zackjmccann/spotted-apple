FROM postgres:15.0

ENV HOME=/db
ENV PORT=5432

WORKDIR ${HOME}
    
COPY bin/ /docker-entrypoint-initdb.d/
COPY --chown=999:999 config/ ./config
RUN chmod 0755 config/*

EXPOSE ${PORT}

CMD [ "postgres", "-c", "config_file=/config/postgresql.conf"]
