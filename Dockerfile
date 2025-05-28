FROM python:3.11-slim-bookworm

# set environment variables
# prevents python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1
# non-empty value ensures python output (stdout, stderr) is sent to the terminal without buffering
ENV PYTHONUNBUFFERED=1

# set container working directory
WORKDIR /app

# copy requirements file first to working directory (helps cache layer)
COPY requirements.txt ./

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# # copy project files to working directory
COPY . ./

EXPOSE 8000

# collect static files
RUN python manage.py collectstatic --noinput

# create custom non-root user and group
RUN useradd --system --create-home --shell /bin/bash appuser

# change ownership of the app directory to the new user (prevents permission issues)
RUN chown -R appuser:appuser ./

USER appuser

RUN chmod -R +x ./scripts

CMD ["./scripts/run.sh"]
