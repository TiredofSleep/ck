FROM python:3.13-slim

WORKDIR /ck

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy CK
COPY targets/ck_desktop/ ./targets/ck_desktop/
COPY ck_sim/ ./ck_sim/
COPY requirements.txt LICENSE ./

WORKDIR /ck/targets/ck_desktop

EXPOSE 7777

# CK boot API (headless, no Kivy GUI)
CMD ["python", "ck_boot_api.py"]
