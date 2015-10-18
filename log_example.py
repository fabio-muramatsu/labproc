from llogger import LLogger

log = LLogger()

log.access("pippo")
log.unknown_id("123.234.345.456")
log.psw_error("pippo")
log.panic("pippo")

log.admin("admin_name")
log.user_del("admin_name", "pippo")
log.user_del_error("admin_name", "pippo", "user not found");
log.invalid_op("admin_name");
log.user_ins("admin_name", "pippo")
log.user_ins_error("admin_name", "pippo", "user already exists");

#FORMAT = '%(asctime)-15s \t %(clientip)s \t %(user)-8s \t %(message)s'
#logging.basicConfig(filename='example.log',format=FORMAT)
#d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
#logger = logging.getLogger('tcpserver')
#logger.warning('Protocol problem: %s', 'connection reset', extra=d)