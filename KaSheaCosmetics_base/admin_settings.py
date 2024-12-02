from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_HEADER": "Ka'Shea Cosmetics",
    "SITE_ICON": {
        "light": lambda request: static("images/logo_black.svg"),  # light mode
        "dark": lambda request: static("images/logo_white.svg"),  # dark mode
    },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    "SITE_LOGO": {
        "light": lambda request: static("images/logo_black.svg"),  # light mode
        "dark": lambda request: static("images/logo_white.svg"),  # dark mode
    },
    
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "25 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "250 245 100",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
}
