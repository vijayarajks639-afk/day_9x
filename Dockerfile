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

# HF Spaces creates /app as root. The app writes its synthetic world + model cache at
# runtime, so point everything writable at $HOME (owned by uid-1000, always writable)
# and belt-and-suspenders chown the WORKDIR too.
RUN chown -R user:user /app && mkdir -p /home/user/data && chown -R user:user /home/user

USER user
ENV HOME=/home/user
ENV DAY9X_DATA_DIR=/home/user/data
ENV FASTEMBED_CACHE_PATH=/home/user/.cache/fastembed

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
