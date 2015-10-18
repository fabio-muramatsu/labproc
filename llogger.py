import logging
import os.path
import sys
import time

LOG_FILENAME = "log/operative_log.log"

UNKNOWN_USER = "(null)"

TYPE_ACCESS_ERROR = "user.access.error"
TYPE_ADMIN_ACCESS = "admin.access"
TYPE_ADMIN_OPERATION = "admin.operation"
TYPE_USER_ACCESS = "user.access"
TYPE_USER_PANIC = "user.panic"

class LLogger:

	def __init__(self):
		if not os.path.isfile(LOG_FILENAME):
			tfile = open(LOG_FILENAME,"w")

		logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)-15s: %(name)-12s %(levelname)-10s  %(type)-20s %(user)-15s %(message)s',
                    datefmt='%Y/%m/%d %I:%M:%S %p',
                    filename=LOG_FILENAME)
		
		self.log = logging.getLogger('sys.user')
		self.adm = logging.getLogger('sys.admin')

	# -------------------------------------------------------
	# ADMIN PROCEDURES --------------------------------------

	def admin(self, admin):
		meta = {'user':admin, 'type':TYPE_ADMIN_ACCESS}
		self.adm.info("", extra = meta)

	def invalid_op(self, admin):
		meta = {'user':admin, 'type':TYPE_ADMIN_OPERATION}
		self.adm.warning("invalid operation selection", extra = meta)

	def user_ins(self, admin, user):
		meta = {'user':admin, 'type':TYPE_ADMIN_OPERATION}
		self.adm.info("user insertion: ID %s", user, extra = meta)

	def user_ins_error(self, admin, user, msg):
		meta = {'user':admin, 'type':TYPE_ADMIN_OPERATION}
		self.adm.error("invalid user insertion: ID %s - %s", user, msg, extra = meta)

	def user_del(self, admin, user):
		meta = {'user':admin, 'type':TYPE_ADMIN_OPERATION}
		self.adm.info("user removal: ID %s", user, extra = meta)

	def user_del_error(self, admin, user, msg):
		meta = {'user':admin, 'type':TYPE_ADMIN_OPERATION}
		self.adm.error("invalid user removal: ID %s - %s", user, msg, extra = meta)

	# -------------------------------------------------------
	# USER PROCEDURES ---------------------------------------

	def access(self, user):
		meta = {'user':user, 'type':TYPE_USER_ACCESS}
		self.log.info("", extra = meta)

	def psw_error(self, user):
		meta = {'user':user, 'type':TYPE_ACCESS_ERROR}
		self.log.error("incorrect password", extra = meta)

	def panic(self, user):
		meta = {'user':user, 'type':TYPE_USER_PANIC}
		self.log.warning("user panic notification sent", extra = meta)

	# -------------------------------------------------------
	# ERROR PROCEDURES --------------------------------------

	def unknown_id(self, id):
		meta = {'user':UNKNOWN_USER, 'type':TYPE_ACCESS_ERROR}
		self.log.warning("unknown tag id: %s", id, extra = meta)
