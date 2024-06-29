FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    make \
    gcc \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh
COPY requirements.txt /requirements.txt
RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

COPY . .
EXPOSE ${STREAMLIT_PORT}
HEALTHCHECK CMD curl --fail http://${STREAMLIT_HOST}:${STREAMLIT_PORT}/_stcore/health
CMD streamlit run src/app.py --server.port=${STREAMLIT_PORT} --server.address=${STREAMLIT_HOST}
