FROM alpine:latest

# Install packages
RUN apk add --no-cache tinyproxy python3 py3-pip supervisor

# Set up tinyproxy log directory
RUN mkdir -p /var/log/tinyproxy && \
    chmod 777 /var/log/tinyproxy

# Create filter file and run directory
RUN mkdir -p /etc/tinyproxy && \
    touch /etc/tinyproxy/filter && \
    mkdir -p /var/run/tinyproxy && \
    chmod 777 /var/run/tinyproxy

# Create a minimal tinyproxy configuration with proper logging
RUN echo "Port 8888" > /etc/tinyproxy/tinyproxy.conf && \
    echo "Listen 0.0.0.0" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "Timeout 600" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "Allow 127.0.0.1" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "Allow 192.168.0.0/16" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "Allow 10.0.0.0/8" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "Allow 172.16.0.0/12" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "Filter \"/etc/tinyproxy/filter\"" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "FilterDefaultDeny No" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "LogLevel Info" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "LogFile \"/var/log/tinyproxy/tinyproxy.log\"" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "Syslog Off" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "ConnectPort 443" >> /etc/tinyproxy/tinyproxy.conf && \
    echo "ConnectPort 80" >> /etc/tinyproxy/tinyproxy.conf

# Set up supervisor to manage both processes
RUN mkdir -p /etc/supervisor.d && \
    printf "[supervisord]\n\
nodaemon=true\n\
user=root\n\
\n\
[program:tinyproxy]\n\
command=tinyproxy -d -c /etc/tinyproxy/tinyproxy.conf\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
autorestart=true\n\
\n\
[program:flask]\n\
command=/app/venv/bin/python /app/app.py\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
" > /etc/supervisor.d/supervisord.conf

# Create a startup script to ensure log permissions are correct
RUN printf "#!/bin/sh\n\
# Ensure log directory exists and has correct permissions\n\
mkdir -p /var/log/tinyproxy\n\
chmod 777 /var/log/tinyproxy\n\
touch /var/log/tinyproxy/tinyproxy.log\n\
chmod 666 /var/log/tinyproxy/tinyproxy.log\n\
\n\
# Start supervisord\n\
exec supervisord -c /etc/supervisor.d/supervisord.conf\n\
" > /startup.sh && \
chmod +x /startup.sh

# Set up the application
WORKDIR /app
COPY app.py .
COPY requirements.txt .
COPY default.json .
COPY templates ./templates/

# Create Python virtual environment and install dependencies
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Expose port 8888 for TinyProxy and 5000 for Flask web UI
EXPOSE 8888 5000

# Use startup script to initialize environment before starting services
CMD ["/startup.sh"] 