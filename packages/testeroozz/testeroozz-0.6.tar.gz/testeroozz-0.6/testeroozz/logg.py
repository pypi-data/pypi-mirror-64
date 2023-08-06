import logging

# # note that this funciton only works once
# test_Var = "it works!!!!"
#
# logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w", format=f"%(name)s - %(levelname)s - %(message)s, {test_Var}")
#
# logging.debug('this is a debug message')
# logging.info('this is an info message')
# logging.warning('this is a warning')
# logging.error('now shit gets real')
# logging.critical('this is a super critical message!')
#
# a = 5
# b = 0
#
# try:
#     a/b
# except Exception as e:
#     logging.error('exception has occured', exc_info=True)
#     logging.exception('this is a second exception log')
#
#
# logging.critical('-------------------------------------------------------------')
# logging.critical('lets try building our own version of a logger')
# logging.critical('-------------------------------------------------------------')
#
# #logger = class whose objects will be used to call functions
# #logrecord = objects of this class have all the info of the event being logged, eg the name of the logger
# #handler = set logrecord to required output. base for subclassess like StreamHandler
# #formatter = used to specify format of string

logger = logging.getLogger('lelogger') #create a custom logger object

#create handlers
c_handler = logging.StreamHandler() #this outputs to console
f_handler = logging.FileHandler("app.log") #this outputs to file
c_handler.setLevel(logging.WARNING) #only warning+ will be logged to console
f_handler.setLevel(logging.ERROR) #only error+ will be logged to file

#create formatters
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#add them to handlers
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

#add handlers to the logger - ok this is where we connect the two
logger.addHandler(c_handler)
logger.addHandler(f_handler)

#testing!
logger.info('this is an info message - SHOULD NOT BE LOGGED') #logged to none
logger.warning('this is a warning message!! - should be logged') #logged to both console and file
logger.error('this is an error message') #logged to file only

#when this is called, a logrecord object is created, which stores all the info about the event
#it then passes that info to c_handler and f_handler
