# day_9x — HF Spaces Docker runtime (HF deprecated native Streamlit SDK for new Spaces).
# Runs the same $0/keyless Streamlit app; no secrets, no API keys (GOVERNANCE: never set
# ANTHROPIC_API_KEY on this public Space).
FROM python:3.12-slim

# HF Spaces runs containers as uid 1000; give it a writable HOME (fastembed model cache)
RUN useradd -m -u 1000 user

WORKDIR /app
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

# HF Spaces creates /app as root; the app writes its synthetic world under /app/data at
# runtime, so uid-1000 needs to own the WORKDIR itself (not just the copied files).
RUN chown -R user:user /app

USER user
ENV HOME=/home/user

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
