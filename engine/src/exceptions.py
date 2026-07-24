"""
Custom exceptions.
"""
class IPTVEngineError(Exception):
    """Base exception for IPTV Engine."""
    pass

class ParsingError(IPTVEngineError):
    """Error parsing M3U."""
    pass

class FetchError(IPTVEngineError):
    """Error fetching data."""
    pass
