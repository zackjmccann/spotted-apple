FROM python:3.9-slim

RUN groupadd --gid 1000 spotted-apple && \
    useradd --uid 1000 --gid 1000 -ms /bin/bash spotted-app-dev
    
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    make \
    musl-dev \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*
    
ADD --chmod=755 https://astral.sh/uv/install.sh /tmp/install.sh
RUN /tmp/install.sh && rm /tmp/install.sh

ENV HOME=/home/spotted-apple-dev
ENV VIRTUAL_ENV=prod-venv
ENV STREAMLIT_PORT=8501

COPY src ${HOME}/src
COPY run.sh ${HOME}/run.sh
COPY requirements.txt ${HOME}/requirements.txt
# RUN chmod +x ${HOME}/run.sh

RUN python -m venv ${VIRTUAL_ENV}
RUN . ${VIRTUAL_ENV}/bin/activate
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
RUN /root/.cargo/bin/uv pip install --system --no-cache -r ${HOME}/requirements.txt

USER spotted-app-dev
WORKDIR ${HOME}

EXPOSE ${STREAMLIT_PORT}

ENTRYPOINT ["./run.sh"]
