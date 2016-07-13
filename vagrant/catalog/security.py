"""
    Security.py

    * programmed by Guillaume Simler
    * this program contains the main security features

"""

"""
    I. Import modules
"""

import bleach


"""
    II. Program
"""

def escape(value):
    """
        extends the classic escaping also to the apostrophe

        @Reviewer: Do you please have a better way?
    """
    value = bleach.clean(value)

    value = value.replace("'", "&#39;")

    return value
