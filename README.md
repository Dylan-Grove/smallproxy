# Homelab Proxy

A Docker-based proxy server that blocks specific Square domains while allowing all other traffic.

## Blocked Domains
- api.squareup.com
- connect.squareup.com
- squareup.com

## Setup Instructions

1. Build the Docker image:
```bash
docker build -t homelab-proxy .
```

2. Run the container:
```bash
docker run -d --name homelab-proxy -p 3128:3128 homelab-proxy
```

## iPad Configuration

1. Go to Settings > Wi-Fi
2. Tap the (i) icon next to your connected network
3. Scroll down and tap "Configure Proxy"
4. Select "Manual"
5. Enter the following:
   - Server: [Your Docker host IP address]
   - Port: 3128
6. Tap "Save"

## Testing

To verify the proxy is working:
1. Try accessing squareup.com - it should be blocked
2. Try accessing other websites - they should work normally

## Logs

To view the proxy logs:
```bash
docker logs homelab-proxy
``` 
