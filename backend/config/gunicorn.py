# -*- coding: utf-8 -*-

import os
import multiprocessing
from distutils.util import strtobool


bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
accesslog = "-"
access_log_format = "%(t)s [%(h)s] | %(r)s (%(s)s) in %(D)sµs"  # noqa: E501

workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2))
threads = int(os.getenv("PYTHON_MAX_THREADS", 1))
reload = bool(strtobool(os.getenv("WEB_RELOAD", "false")))
timeout = int(os.getenv("WEB_TIMEOUT", 120))
