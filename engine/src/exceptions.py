class EngineError(Exception):
    pass

class ParserError(EngineError):
    pass

class VerificationError(EngineError):
    pass

class ConfigurationError(EngineError):
    pass
