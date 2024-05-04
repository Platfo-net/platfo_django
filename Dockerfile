FROM python:3.10.14-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Run migrations and collect static files (if necessary)
# Uncomment these lines if you need to run migrations or collect static files during the build process
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# Expose the port where Gunicorn will run
EXPOSE 8000
#
## Command to start the Gunicorn server
CMD ["gunicorn", "--bind", "--reload", "0.0.0.0:8000", "core.wsgi:application"]
