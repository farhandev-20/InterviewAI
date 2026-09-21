import os
import multiprocessing

# Bind dynamically to Railway / Cloud PORT or default to 5000
port = os.getenv("PORT", "5000")
bind = f"0.0.0.0:{port}"

workers = max(multiprocessing.cpu_count(), 2)
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

loglevel = "info"
accesslog = "-"
errorlog = "-"
