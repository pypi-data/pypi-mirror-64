import datetime
import GcMessageProtocol
from GcMessageProtocol.errors import (
    UnknownProtocolException,
    UnknownProtocolFieldException,
    MissingProtocolFieldsException
)

class Protocol():
    split = "%|!%" # Used to separate fields
    __field_types = {
        "type":( (eval,), (lambda x: '.'.join([x.__module__, x.__name__]),) ),
        "message":( (int,), (str,) ),
        "bot":( (int,), (str,) ),
        "timestamp":(
            (eval, datetime.datetime.fromtimestamp), (lambda x: x.timestamp(), str)
            )
        } # Base needed fields

    __protocols = dict() # A list of protocols registered

    def __init__(self, info:str=None, **infoObject):
        if not info:
            info = infoObject
            itype = infoObject.get('type')
            if not itype or itype != self.__class__.__name__:
                info['type'] = self.__class__
        
        self.__name = None
        self.information = info
        self.checkMissingFields()
        if self.__class__ != Protocol:
            Protocol.register(self.__class__)


    # Check protocol missing fields and raise MissingProtocolFieldsException if anyone is missing
    def checkMissingFields(self):
        if self.__class__.obrigatory_fields:
            field_list = self.fields.list
            missing_fields = list(filter(
                lambda field: field not in field_list,
                self.__class__.obrigatory_fields
            ))
            if missing_fields:
                raise MissingProtocolFieldsException(missing_fields)

    # Stringify the protocol message to send on discord 
    def toMessage(self):
        return str(self.fields)

    # Get protocol name
    @property
    def name(self):
        return self.__name if self.__name else self.__class__.__name__

    # Set protocol name
    @name.setter
    def name(self, value):
        self.__name = value if value != self.__class__.__name__ else None
    
    # Get Fields object of current protocol
    @property
    def fields(self):
        return Fields(self.information)

    # -- Static -- #

    # Get a given registered protocol by name
    @staticmethod
    def getProtocol(name):
        protocol = Protocol.__protocols.get(name, None)
        if not protocol:
            raise UnknownProtocolException(name)

        return protocol

    # Function used to identify and return a protocol by a message.content
    @staticmethod
    def identifyProtocol(message:str):
        fields = Fields(message)
        return fields.type(**fields.fields)

    # Register a field and its converters to Protocol.__field_types
    @staticmethod
    def registerField(field_name, convert: tuple, revert: tuple):
        Protocol.__field_types[field_name] = (convert, revert)

    # Register a Protocol to Protocol.__protocols
    @staticmethod
    def register(protocol):
        if Protocol != protocol.__base__:
            raise TypeError(f"This is not an protocol: {protocol.__name__}")
        
        name = protocol.name if protocol.name else protocol.__name__
        Protocol.__protocols[name] = protocol
        return protocol

# A class used to make field conversionss #
class Fields(object):

    # Convert a str to a field dict
    @staticmethod
    def from_str(info):
        info = info.split(Protocol.split)
        fields = {}
        for field in info:
            k, v = field.split(':')
            convertOperations = Protocol._Protocol__field_types.get(k)
            if not convertOperations:
                raise UnknownProtocolFieldException(k)
            for convert in convertOperations[0]:
                v = convert(v)
            fields[k] = v
        return fields

    def __init__(self, info):
        if not isinstance(info, (str, dict)):
            raise TypeError("Info must be a str or dict, not " + type(info).__name__)
        if type(info) == str:
            info = Fields.from_str(info)
        super().__setattr__('_Fields__fields', info)

    # Return all fields as a dict #
    @property
    def fields(self):
        return super().__getattribute__('_Fields__fields')

    # Return a list of all field names
    @property
    def list(self):
        return list(self.fields)

    def __getattribute__(self, name):
        obj = super().__getattribute__('_Fields__fields').get(name)
        return obj if obj else super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in self.fields:
            fields = self.fields
            fields[name] = value
            name = '_Fields__fields'
            value = fields
        return super().__setattr__(name, value)

    # Convert fields to a messageable string
    def __str__(self):
        field_str = []
        for k, v in self.fields.items():
            convertOperations = Protocol._Protocol__field_types.get(k)
            if not convertOperations:
                raise UnknownProtocolFieldException(k)
            for convert in convertOperations[1]:
                v = convert(v)
            field_str.append(':'.join([k,v]))
        return Protocol.split.join(field_str)