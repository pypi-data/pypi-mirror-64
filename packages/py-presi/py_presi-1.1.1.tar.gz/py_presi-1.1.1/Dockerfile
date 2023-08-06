FROM python:3.7.6-slim

RUN apt-get update && apt-get install -y \
    --no-install-recommends curl
# cleanup
RUN rm -rf /var/lib/apt/lists/*
 
# Copy the application to container
COPY . /app
WORKDIR /app

# -e is develop install aka symlink not copy to site-packages
RUN pip install --no-cache-dir -e .
# build the html file
RUN pp-build

CMD ["python", "-m", "http.server", "--bind", "0.0.0.0", "8080"]
HEALTHCHECK --interval=5s --timeout=3s \
    CMD curl -f http://0.0.0.0:8080/ || exit 1
