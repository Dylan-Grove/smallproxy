import json
import os
import subprocess
import time
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)
FILTER_FILE = '/etc/tinyproxy/filter'
DEFAULT_CONFIG_FILE = 'default.json'
PROXY_CONFIG_FILE = '/etc/tinyproxy/tinyproxy.conf'

def load_default_filters():
    with open(DEFAULT_CONFIG_FILE, 'r') as file:
        return json.load(file)

def get_current_filters():
    if not os.path.exists(FILTER_FILE):
        return []
    
    with open(FILTER_FILE, 'r') as file:
        # Skip comment lines and empty lines
        lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        return lines

def save_filters(filters, is_whitelist=False):
    with open(FILTER_FILE, 'w') as file:
        # First line is a comment indicating filter type
        file.write(f"# {'WHITELIST' if is_whitelist else 'BLACKLIST'} MODE\n")
        for filter_item in filters:
            # Clean the filter (remove any special characters)
            clean_filter = filter_item.strip()
            file.write(f"{clean_filter}\n")
    
    # Update tinyproxy.conf based on whitelist/blacklist mode
    update_proxy_config(is_whitelist)
    
    # Restart tinyproxy to apply changes
    restart_tinyproxy()
    return True

def update_proxy_config(is_whitelist):
    if os.path.exists(PROXY_CONFIG_FILE):
        # Read the current config
        with open(PROXY_CONFIG_FILE, 'r') as file:
            lines = file.readlines()
        
        # Track if we've updated the config
        config_updated = False
        
        # Find FilterDefaultDeny line if it exists
        filter_default_deny_found = False
        filter_path_found = False
        
        for i, line in enumerate(lines):
            # Update FilterDefaultDeny setting
            if line.strip().startswith('FilterDefaultDeny'):
                lines[i] = f"FilterDefaultDeny {'Yes' if is_whitelist else 'No'}\n"
                filter_default_deny_found = True
                config_updated = True
            
            # Make sure Filter path is set
            elif line.strip().startswith('Filter '):
                if not line.strip().endswith(FILTER_FILE):
                    lines[i] = f"Filter \"{FILTER_FILE}\"\n"
                    config_updated = True
                filter_path_found = True
        
        # If FilterDefaultDeny wasn't found, add it
        if not filter_default_deny_found:
            lines.append(f"FilterDefaultDeny {'Yes' if is_whitelist else 'No'}\n")
            config_updated = True
        
        # If Filter path wasn't found, add it
        if not filter_path_found:
            lines.append(f"Filter \"{FILTER_FILE}\"\n")
            config_updated = True
        
        # Write the updated config only if changes were made
        if config_updated:
            with open(PROXY_CONFIG_FILE, 'w') as file:
                file.writelines(lines)

def restart_tinyproxy():
    try:
        subprocess.run(["pkill", "-HUP", "tinyproxy"])
        time.sleep(1)  # Give it time to restart
    except Exception as e:
        app.logger.error(f"Error restarting tinyproxy: {str(e)}")

def start_tinyproxy():
    try:
        subprocess.Popen(["tinyproxy", "-d", "-c", PROXY_CONFIG_FILE])
        time.sleep(1)  # Give it time to start
    except Exception as e:
        app.logger.error(f"Error starting tinyproxy: {str(e)}")

def stop_tinyproxy():
    try:
        subprocess.run(["pkill", "tinyproxy"])
        time.sleep(1)  # Give it time to stop
    except Exception as e:
        app.logger.error(f"Error stopping tinyproxy: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/filters', methods=['GET'])
def get_filters():
    defaults = load_default_filters()
    current = get_current_filters()
    system_state = defaults.get("system", {
        "blocking_enabled": True, 
        "proxy_enabled": True,
        "whitelist_enabled": False
    })
    
    return jsonify({
        "whitelist": defaults.get("whitelist", []),
        "blacklist": defaults.get("blacklist", []),
        "current": current,
        "system": system_state
    })

@app.route('/api/filters', methods=['POST'])
def update_filters():
    data = request.json
    whitelist = data.get('whitelist', [])
    blacklist = data.get('blacklist', [])
    is_whitelist_mode = data.get('is_whitelist_mode', False)
    
    # Save the active filters based on the current mode
    active_filters = whitelist if is_whitelist_mode else blacklist
    
    try:
        success = save_filters(active_filters, is_whitelist_mode)
        
        # Also update the default config
        defaults = load_default_filters()
        defaults["whitelist"] = whitelist
        defaults["blacklist"] = blacklist
        defaults["system"]["whitelist_enabled"] = is_whitelist_mode
        
        with open(DEFAULT_CONFIG_FILE, 'w') as file:
            json.dump(defaults, file, indent=2)
        
        return jsonify({"success": success})
    except Exception as e:
        app.logger.error(f"Error updating filters: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/system', methods=['POST'])
def update_system():
    system_state = request.json.get('system', {})
    defaults = load_default_filters()
    
    try:
        # Update the default config with the new system state
        defaults["system"] = system_state
        with open(DEFAULT_CONFIG_FILE, 'w') as file:
            json.dump(defaults, file, indent=2)
        
        # Handle proxy service
        if system_state.get("proxy_enabled", True):
            # Try to restart if it's running, or start if it's not
            restart_tinyproxy()
        else:
            stop_tinyproxy()
        
        # Handle blocking
        if system_state.get("blocking_enabled", True):
            # Apply filters based on whitelist/blacklist mode
            is_whitelist_mode = system_state.get("whitelist_enabled", False)
            active_filters = defaults.get("whitelist" if is_whitelist_mode else "blacklist", [])
            save_filters(active_filters, is_whitelist_mode)
        else:
            # Clear filters (empty file)
            save_filters([], system_state.get("whitelist_enabled", False))
        
        return jsonify({"success": True})
    except Exception as e:
        app.logger.error(f"Error updating system: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    LOG_FILE = '/var/log/tinyproxy/tinyproxy.log'
    
    try:
        if not os.path.exists(LOG_FILE):
            # Try using process output as fallback
            logs = subprocess.check_output(["ps", "aux"]).decode('utf-8')
            return f"Log file not found. Process status:\n{logs}"
        
        with open(LOG_FILE, 'r') as file:
            logs = file.read()
        return logs
    except Exception as e:
        return f"Error reading logs: {str(e)}"

if __name__ == '__main__':
    # Initialize the proxy on startup
    defaults = load_default_filters()
    system_state = defaults.get("system", {
        "blocking_enabled": True, 
        "proxy_enabled": True,
        "whitelist_enabled": False
    })
    
    # Make sure the Filter option is enabled in tinyproxy.conf
    update_proxy_config(system_state.get("whitelist_enabled", False))
    
    # Apply initial filters if blocking is enabled
    if system_state.get("blocking_enabled", True):
        is_whitelist_mode = system_state.get("whitelist_enabled", False)
        active_filters = defaults.get("whitelist" if is_whitelist_mode else "blacklist", [])
        save_filters(active_filters, is_whitelist_mode)
    else:
        # Clear filters (empty file)
        save_filters([], system_state.get("whitelist_enabled", False))
    
    # Run Flask on all interfaces on port 5000
    app.run(host='0.0.0.0', port=5000) 