# SmallProxy

A lightweight proxy server with a web interface for managing filters. Powered by [TinyProxy](https://tinyproxy.github.io/).

## Features

- **Dual Port Architecture**:
  - Port 8888: Proxy service (TinyProxy)
  - Port 5000: Web management interface (Flask)

- **Dual Filtering Modes**:
  - **Blacklist Mode**: Block specific domains while allowing all others
  - **Whitelist Mode**: Allow only specific domains while blocking all others
  - Easy toggle between modes

- **Easy Filter Management**:
  - Separate tabs for whitelist and blacklist management
  - Add new domain filters with a simple interface
  - Remove unwanted filters
  - Live status updates when changes are made
  
- **Real-time Log Monitoring**:
  - Live-updating log viewer that automatically shows new log entries
  - Clear log view functionality for better readability
  - Automatic log rotation handling

- **Modern UI**:
  - Clean, responsive design for desktop and mobile
  - Intuitive controls with visual feedback
  - Status messages for all operations

## Setup

1. Build the Docker image:
```bash
docker build -t smallproxy .
```

2. Run the container:
```bash
docker run -d --name smallproxy -p 8888:8888 -p 5000:5000 smallproxy
```

3. Access the web interface at `http://localhost:5000`

## Port Configuration

- `8888`: TinyProxy port (configure your devices to use this proxy port)
- `5000`: Web interface port (access the management UI here)

## Default Configuration

### Default Blacklist
The following domains are blocked by default in blacklist mode:
- facebook.com
- instagram.com
- tiktok.com
- twitter.com
- reddit.com
- youtube.com
- netflix.com
- hulu.com
- disney.com
- disneyplus.com
- twitch.tv

### Default Whitelist
The following domains are allowed by default in whitelist mode:
- google.com
- github.com
- stackoverflow.com
- docs.microsoft.com
- developer.mozilla.org
- wikipedia.org

## Security Note

The web interface is accessible on port 5000. Make sure to restrict access to authorized users only if deploying in a shared environment.

## Using the Proxy

1. Configure your devices to use the proxy server at the host IP address and port 8888.
2. Use the web interface at `http://hostname:5000` to manage which sites are blocked or allowed.
3. Toggle between whitelist and blacklist modes as needed:
   - **Blacklist Mode**: Only domains on the blacklist are blocked
   - **Whitelist Mode**: Only domains on the whitelist are allowed, all others are blocked

## Acknowledgments

SmallProxy is powered by [TinyProxy](https://tinyproxy.github.io/), a lightweight HTTP/HTTPS proxy daemon for POSIX operating systems.
