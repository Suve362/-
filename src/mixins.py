from sqlalchemy import Column, DateTime, event, func


class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False)

    updated_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False)

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = func.now()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)
