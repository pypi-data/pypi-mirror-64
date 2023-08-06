class UnknownProtocolException(Exception):
    def __init__(self, protocolName):
        super().__init__(f"This protocol doesn't exists: {protocolName}")

class UnknownProtocolFieldException(Exception):
    def __init__(self, field):
        super().__init__(f"This field doesn't exists: {field}")

class MissingProtocolFieldsException(Exception):
    def __init__(self, fields):
        super().__init__(f"Some fields are missing: {', '.join(fields)}")