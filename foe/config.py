
"""
"""

# Native
import os

# 3rd-Party
import anyconfig

# Proprietary


DEFAULT = './config/foe.yml'
# Add the ability to get config from a different file
PATH = os.environ.get('FOE_CONFIG', DEFAULT)
# Load the default config then override, so that we always have the correct structure
config = anyconfig.load([DEFAULT, PATH])
