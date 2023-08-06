from GcMessageProtocol.protocols.protocol import Protocol, datetime

# Protocol to specify bans #
class BanProtocol(Protocol):
    obrigatory_fields = ['bot', 'user_id', 'target_id', 'reason', 'timestamp']

    def __init__(self, bot:int, user_id:int, target_id:int, 
            reason:str, timestamp:datetime.datetime, **kwargs):
        
        Protocol.registerField('user_id', (int,), (str,))
        Protocol.registerField('target_id', (int,), (str,))
        Protocol.registerField('reason', (), ())
        super().__init__(bot=bot, user_id=user_id, target_id=target_id, reason=reason, timestamp=timestamp)

        fields = self.fields
        self.user_id = fields.user_id
        self.target_id = fields.target_id
        self.reason = fields.reason
        self.date = fields.timestamp

