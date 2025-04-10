FROM mongo:6.0

# Copy the database initialization script into the container
COPY init-mongo.js /docker-entrypoint-initdb.d/

# Expose the default MongoDB port
EXPOSE 27017