"""
    Container Type

    A container type can either be an array, or an object.
"""


class ContainerType(object):
    def __init__(self):
        super().__init__()

    def load_from_object(self, input_object):
        pass

    def dump_to_object(self):
        pass

    def checksum(self):
        pass
