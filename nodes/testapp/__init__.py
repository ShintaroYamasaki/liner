from node import Node
import time
import os

IOFILE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/io'
LOGFILE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/logs'

class NodeMain(Node):
  def __init__(self, config: dict, parent=None):
    super().__init__(config, parent)
    self.__iofile = config['iofile']
    self.__logfile = config['logfile']
    self.__testapp = TestApp(self.__iofile, self.__logfile)

  def read(self):
    super().read()
    _value = self.__testapp.read()
    return int(_value)

  def write(self, value):
    super().write(value)
    self.__testapp.write(value)



class TestApp:

  def __init__(self, iofile, logfile):
    self.iofile = IOFILE_DIR + '/' + iofile
    self.logfile = LOGFILE_DIR + '/' + logfile
    with open(self.iofile, 'w') as f:
      f.write('0')
    
  def read(self) -> int:
    _value = ''
    with open(self.iofile, 'r') as f:
      _value = f.read()
    with open(self.logfile, 'a') as f:
      line = str(time.time()) + ',' + _value + ',' + 'read' + "\n"
      f.write(line)
    return int(_value)

  def write(self, value: int):
    with open(self.logfile, 'a') as f:
      line = str(time.time()) + ',' + str(value) + ',' + 'write' + "\n"
      f.write(line)
    with open(self.iofile, 'w') as f:
      f.write(str(value))

