# --------- STAGE 1: Install dependencies ---------
    FROM python:latest AS builder
    WORKDIR /usr/src/app
    COPY requirements.txt .
    RUN pip install --upgrade pip \
     && pip install --prefix=/install -r requirements.txt
    # --------- STAGE 2: Final Image ---------
    FROM python:latest
    COPY --from=builder /install /usr/local
    WORKDIR /usr/src/app
    COPY . /usr/src/app
    CMD ["python", "./setup.py"]
    EXPOSE   8080
    