import configparser


config = configparser.ConfigParser()
config.read('config.ini')
router_ip = config['ROUTER']['ip']
router_username = config['ROUTER']['username']
router_password = config['ROUTER']['password']

