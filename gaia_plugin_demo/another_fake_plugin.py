from gaia.inputs import GaiaIO
from gaia.gaia_process import GaiaProcess


class AnotherFakeIO(GaiaIO):

    def __init__(self, uri='', **kwargs):
        print "Created AnotherFakeIO"

    def read(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def delete(self):
        pass


class AnotherFakeProcess(GaiaProcess):

    def __init__(self, **kwargs):
        super(AnotherFakeProcess, self).__init__(**kwargs)
        print "Created AnotherFakeProcess"

    def compute(self):
        print ("Compute something with AnotherFakeProcess")
