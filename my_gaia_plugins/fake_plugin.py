from gaia.inputs import GaiaIO
from gaia.gaia_process import GaiaProcess


class FakeIO(GaiaIO):

    def __init__(self, uri='', **kwargs):
        super(FakeIO, self).__init__(uri=uri, **kwargs)
        print "Created FakeIO"

    def read(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def delete(self):
        pass


class FakeProcess(GaiaProcess):

    def __init__(self, **kwargs):
        super(FakeProcess, self).__init__(**kwargs)
        print "Created FakeProcess"

    def compute(self):
        print ("Compute something with FakeProcess")
