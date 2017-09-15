import databasehelper
import threading
import time
from apps.node import Node
import configmanager

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_TEMP_DATASTORE = configmanager.get_key('DATABASE', 'DataStoreCollectionTemp')

INTERVAL = float(configmanager.get_key('INTERVALS', 'DatastoreInterval'))

class DataStoreThread(threading.Thread):
  def __init__(self, node: Node, node_id: str) -> None:
    super(DataStoreThread, self).__init__()
    self.interval = INTERVAL
    self.__node = node
    self.__id = node_id

  def __store(self) -> None:
    db = databasehelper.get_database(DB_NAME)
    col = databasehelper.get_collection(db, DB_COLLECTION_TEMP_DATASTORE + str(self.__id))
    while self.__isrunning:
      readVal = self.__node.read()
      #print(readVal)
      doc = {'time': time.time(), 'value': readVal}
      databasehelper.insert(col, doc)
      time.sleep(self.interval)

  def run(self) -> None:
    self.__isrunning = True
    self.__store()

  def kill(self) -> None:
    self.__isrunning = False




data_stores = {}

def run_datastorer(node_id: str, node: Node) -> None:
  datastorethread = DataStoreThread(node, node_id)
  datastorethread.start()
  data_stores[node_id] = datastorethread

def kill_datastorer(node_id: str) -> None:
  data_stores[node_id].kill()
  data_stores[node_id] = None
  del data_stores[node_id]

def killall() -> None:
  for datastore in data_stores.values():
    datastore.kill()
