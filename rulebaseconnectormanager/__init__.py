import databasehelper as dbhelper
import configmanager
import appmanager
import threading
import time
import logging
import pymongo

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_RULES = configmanager.get_key('DATABASE', 'RulesCollection')
DB_COLLECTION_TEMP_DATASTORE = configmanager.get_key('DATABASE', 'DataStoreCollectionTemp')
INTERVAL = float(configmanager.get_key('INTERVALS', 'RulebaseInterval'))
 
class RuleBaseConnectorThread(threading.Thread):
  __instance = None

  def __new__(cls, *args, **keys):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

  def __init__(self, interval):
    super(RuleBaseConnectorThread, self).__init__()
    logging.basicConfig(level=logging.DEBUG)
    self.interval = interval

  def setNodesDict(self, nodes: dict):
    self.nodes = nodes

  def __connectnodes(self):
    db = dbhelper.get_database(DB_NAME)
    while self.__isrunning:
      connectionscol = dbhelper.get_collection(db, DB_COLLECTION_RULES)
      connections = list(dbhelper.find(connectionscol, {}))

      for connection in connections:
        event = connection['event']
        eventnodecol = dbhelper.get_collection(db, DB_COLLECTION_TEMP_DATASTORE + str(event['nodeid']))
        eventnodevalues = dbhelper.find_with_params(eventnodecol, {}, dict(sort=[('time', pymongo.DESCENDING)], limit=2))
        # Sort with time by desc
        desceventnodevalues = eventnodevalues

        firstvalue = str(desceventnodevalues[0]['value'])
        secondvalue = str(desceventnodevalues[1]['value'])
        eventoperator = str(event['operator'])
        eventvalue = str(event['value'])

        firstrule = firstvalue + eventoperator + eventvalue
        secondrule = secondvalue + eventoperator + eventvalue

        # Rule check
        if eval(firstrule) and not eval(secondrule):
          logging.info('ignite: ' + str(connection))
          actions = connection['actions']
          for action in actions:
            app_id = action['nodeid']
            appmanager.write_app_value(app_id, action['value'])

      time.sleep(self.interval)

  def run(self):
    self.__isrunning = True
    self.__connectnodes()

  def kill(self):
    self.__isrunning = False





__nodeconnectorthread = RuleBaseConnectorThread(INTERVAL)

def run():
  __nodeconnectorthread.start()

def kill():
  __nodeconnectorthread.kill()

def find_rule(connector_id: int):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  rule = dbhelper.find(col, {'_id': connector_id})
  return rule[0]

def list_rules():
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  listrules = list(dbhelper.find(col, {}))
  return listrules

def add(configs: dict):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  dbhelper.insert(col, configs)

def update(connector_id, configs: dict):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  dbhelper.update(col, {'_id': connector_id}, configs)

def delete(connector_id):
  db = dbhelper.get_database(DB_NAME)
  col = dbhelper.get_collection(db, DB_COLLECTION_RULES)
  dbhelper.delete(col, {'_id': connector_id})
