class BaseDTO:

    @staticmethod
    def serialize_single(obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()

        return obj

    def serialize(self, objs):
        if type(objs) is list:
            return [self.serialize_single(obj) for obj in objs]

        return self.serialize_single(objs)

    def to_dict(self):
        keys = self.__annotations__
        return {key: self.serialize(getattr(self, key)) for key in keys}