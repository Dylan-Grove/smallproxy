FROM ubuntu:22.04

# Install Squid and other necessary packages
RUN apt-get update && \
    apt-get install -y squid && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy our custom Squid configuration
COPY squid.conf /etc/squid/squid.conf

# Create cache directories
RUN mkdir -p /var/cache/squid && \
    chown -R proxy:proxy /var/cache/squid && \
    squid -z

# Expose Squid port
EXPOSE 3128

# Start Squid
CMD ["squid", "-N"] 