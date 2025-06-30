#!/usr/bin/env python3
"""
G.E.N.G.A.R - Gage's Enhanced Next-Gen AI Responder
Main Entry Point
Author: Gage Ayala
"""

import sys
import os

# Add the core directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from core.gengar import main

if __name__ == "__main__":
    main() 