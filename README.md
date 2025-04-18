# SmallProxy

A lightweight proxy server with a web interface for managing filters. Perfect for blocking websites quickly for your clients. Powered by [TinyProxy](https://tinyproxy.github.io/).

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
  - Color-coded log entries for easy identification of different event types

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
- squareup.com
- api.squareup.com
- connect.squareup.com

### Default Whitelist
The following domains are allowed by default in whitelist mode:
- google.com

## Security Note

The web interface is accessible on port 5000. Make sure to restrict access to authorized users only if deploying in a shared environment.

NOTE: This is meant strictly for testing and lab purposes. Run this in production at your own risk.

## Using the Proxy

1. Configure your devices to use the proxy server at the host IP address and port 8888.
2. Use the web interface at `http://hostname:5000` to manage which sites are blocked or allowed.
3. Toggle between whitelist and blacklist modes as needed:
   - **Blacklist Mode**: Only domains on the blacklist are blocked
   - **Whitelist Mode**: Only domains on the whitelist are allowed, all others are blocked

## Acknowledgments

SmallProxy is powered by [TinyProxy](https://tinyproxy.github.io/), a lightweight HTTP/HTTPS proxy daemon for POSIX operating systems.

## Repository Info

This repository includes:
- `.gitignore` - Excludes common system files and development artifacts
- `CHANGELOG.md` - Documents all significant changes to the project
- `Dockerfile` - Container definition for building and running SmallProxy
- `default.json` - Default configuration file with initial whitelist and blacklist settings
