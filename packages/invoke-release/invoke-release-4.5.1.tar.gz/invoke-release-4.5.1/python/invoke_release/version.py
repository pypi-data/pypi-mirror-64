from __future__ import unicode_literals


__version_info__ = (4, 5, 1)
__version__ = '-'.join(filter(None, ['.'.join(map(str, __version_info__[:3])), (__version_info__[3:] or [None])[0]]))
