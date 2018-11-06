FROM postgres:9.6.9-alpine

# Copy maintenance scripts to the volume.
# These scripts are for managing the PostgreSQL backups.
COPY ./docker/local/postgresql/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
