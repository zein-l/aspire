#!/usr/bin/env python3
import os

from app import create_app

# Determine configuration: defaults to "development" if FLASK_CONFIG not set
config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Allow binding to PORT env (useful for containerized deploys)
    port = int(os.getenv('PORT', 5000))
    # Debug mode picked up from config.DEBUG
    debug = app.config.get('DEBUG', False)
    app.run(host='0.0.0.0', port=port, debug=debug)
