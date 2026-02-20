# config.py
# Configuration and presets for image resizer

# Supported image formats
SUPPORTED_FORMATS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
    '.tiff', '.webp', '.ico'
}

# Output formats
OUTPUT_FORMATS = {
    'JPEG': '.jpg',
    'PNG': '.png',
    'WEBP': '.webp',
    'BMP': '.bmp',
    'GIF': '.gif'
}

# Common resize presets (width, height)
PRESETS = {
    'thumbnail': (150, 150),
    'small': (320, 320),
    'medium': (640, 640),
    'large': (1024, 1024),
    'hd': (1920, 1080),
    'instagram': (1080, 1080),
    'facebook': (1200, 630),
    'twitter': (1200, 675),
    'youtube': (1280, 720),
    'profile': (400, 400),
}

# Quality settings (for JPEG/WEBP)
QUALITY_PRESETS = {
    'low': 60,
    'medium': 80,
    'high': 95,
    'maximum': 100
}

# Aspect ratio modes
ASPECT_MODES = {
    'fit': 'Resize to fit within dimensions (maintain aspect ratio)',
    'fill': 'Resize to fill dimensions (may crop)',
    'stretch': 'Stretch to exact dimensions (may distort)',
    'pad': 'Resize to fit and add padding (maintain aspect ratio)'
}

# Default settings
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_QUALITY = 85
DEFAULT_FORMAT = 'JPEG'
DEFAULT_MODE = 'fit'
DEFAULT_PREFIX = 'resized_'
DEFAULT_SUFFIX = ''
