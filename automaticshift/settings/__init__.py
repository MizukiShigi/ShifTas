# settings/__init__.py

from .production import *           # production.py(本番環境用)をimport

try:
    from .development import *      # development.py(開発環境用)をimport
except:
    pass