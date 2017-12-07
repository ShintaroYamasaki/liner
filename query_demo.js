globalapps = [
{
  name: 'gpio int-int',
  note: '',
  module_name: 'gpiodigital',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'pin_num',
      type: 'int'
    }
  ]
},
{
  name: 'socket int-int',
  note: '',
  module_name: 'socket',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'address',
      type: 'str'
    },
    {
      name: 'port',
      type: 'int'
    }
  ]
},
{
  name: 'http get str-str',
  note: '',
  module_name: 'httpget',
  readtype: 'str',
  writetype: 'str',
  required_configs: [
    {
      name: 'read_uri',
      type: 'str'
    },
    {
      name: 'write_uri',
      type: 'str'
    }
  ]
},
{
  name: 'mabeee server int-int',
  note: '',
  module_name: 'mabeeeserver',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'uri',
      type: 'str'
    },
    {
      name: 'deviceid',
      type: 'int'
    }
  ]
},
{
  name: 'phue onoff int-int',
  note: 'Please press hue bridge button before adding this app.',
  module_name: 'phueonoffmanager',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'address',
      type: 'str'
    },
    {
      name: 'light_name',
      type: 'str'
    }
  ]
},
{
  name: 'phue brightness int-int',
  note: 'Please press hue bridge button before adding this app.',
  module_name: 'phuebrightnessmanager',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'address',
      type: 'str'
    },
    {
      name: 'light_name',
      type: 'str'
    }
  ]
},
{
  name: 'ifttt outgoing webhocks',
  note: 'https://ifttt.com/maker_webhooks',
  module_name: 'iftttoutgoingwebhocks',
  readtype: 'str',
  writetype: 'str',
  required_configs: [
    {
      name: 'uri',
      type: 'str'
    }
  ]
},
{
  name: 'ECHONET lite Air Conditioner ON/OFF int-int',
  note: '',
  module_name: 'echonetaircononoff',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'IP_Address',
      type: 'str'
    }
  ]
},
{
  name: 'ECHONET lite Air Conditioner Templeture int-int',
  note: '',
  module_name: 'echonetaircontemp',
  readtype: 'int',
  writetype: 'int',
  required_configs: [
    {
      name: 'IP_Address',
      type: 'str'
    }
  ]
}
]

db.global_apps.drop();
db.createCollection('global_apps');
db.global_apps.insert(globalapps);
result = db.global_apps.find();
shellPrint(result);

gpio_id = db.global_apps.find({name: 'gpio int-int'})[0]._id.valueOf();
socket_id = db.global_apps.find({name: 'socket int-int'})[0]._id.valueOf();
mabeee_id = db.global_apps.find({name: 'mabeee server int-int'})[0]._id.valueOf();
phue_id = db.global_apps.find({name: 'phue onoff int-int'})[0]._id.valueOf();
phueb_id = db.global_apps.find({name: 'phue brightness int-int'})[0]._id.valueOf();


localapps = [
{
  name: 'gpio23',
  module_name: 'gpiodigital',
  global_app_id: gpio_id,
  readtype: 'int',
  writetype: 'int',
  note: '',
  configs: [
    {
      name: 'pin_num',
      type: 'int',
      value: NumberInt(23)
    }
  ]
},
{
  name: 'gpio24',
  module_name: 'gpiodigital',
  global_app_id: gpio_id,
  readtype: 'int',
  writetype: 'int',
  note: '',
  configs: [
    {
      name: 'pin_num',
      type: 'int',
      value: NumberInt(24)
    }
  ]
}
]

db.local_apps.drop();
db.createCollection('local_apps');
db.local_apps.insert(localapps);
result = db.local_apps.find();
shellPrint(result);

gpio23_id = db.local_apps.find({name: 'gpio23'})[0]._id.valueOf();
gpio24_id = db.local_apps.find({name: 'gpio24'})[0]._id.valueOf();

devices = [
  {
    name: 'self',
    note: '',
    apps: [gpio23_id, gpio24_id]
  },
  {
    name: 'grove Pi',
    note: 'ip: 192.168.1.8',
  },
  {
    name: 'macbook',
    note: 'ip: 192.168.1.3',
  },
  {
    name: 'phue',
    note: 'ip: 192.168.1.2',
  }
]

db.devices.drop();
db.createCollection('devices');
db.devices.insert(devices);
result = db.devices.find();
shellPrint(result);



rules = [
{
  name: 'gpio23 on with 24',
  on: false,
  event: {
    nodeid: gpio23_id, 
    operator: '==', 
    value: NumberInt(1),
    type: 'int'
  }, 
  action: {
    nodeid: gpio24_id, 
    value: NumberInt(1),
    type: 'int'
  }
},
{
  name: 'gpio23 off with 24',
  on: false,
  event: {
    nodeid: gpio23_id, 
    operator: '==', 
    value: NumberInt(0),
    type: 'int'
  }, 
  action: {
    nodeid: gpio24_id, 
    value: NumberInt(0),
    type: 'int'
  }
}
]


db.rules.drop();
db.createCollection('rules');
db.rules.insert(rules);