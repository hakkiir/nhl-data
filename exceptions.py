# exceptions.py
class APIError(Exception):
    """Yleisluokka kaikille API-virheille."""
    pass

class TransformationError(Exception):
    """Yleisluokka kaikille transformaatio-virheille."""
    pass

class SaveToDatabaseError(Exception):
    """Yleisluokka kaikille tallennus-virheille."""
    pass