#!/usr/bin/python
# coding=utf-8

#
# Import
#
import logging
import optparse
import vk

#
# function main()
#
def main():
    #
    # Default logger
        #
    logger = logging.getLogger('file-description.py logger')
    logger.setLevel(logging.INFO)

    #
    # Get attrs
    #
    script_args = parse_args()

    #
    # Config logger if need
    #
    if script_args.dst_log_file is not None:
        # Declare format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Set handler 
        log_file_handler = logging.FileHandler(script_args.dst_log_file, mode="a")
        # Set format to handler
        log_file_handler.setFormatter(formatter)
        # Set handler to logger
        logger.addHandler(log_file_handler)
        # Set level
        logger.setLevel(logging.DEBUG)

    #
    # Main part
    #    
    logger.debug('Script start')
    
    logger.debug('Check VK id: %s', script_args.vk_id)
    
    logger.debug('VK App id: %s', script_args.app_id)
    logger.debug('VK user login: %s', script_args.user_name)
    logger.debug('VK user password: %s', script_args.user_pass)
    
    if script_args.app_id and script_args.user_name == None and script_args.user_pass == None:
        vksession = vk.Session()
    else:
        try:
            vksession = vk.AuthSession(app_id=script_args.app_id, user_login=script_args.user_name, user_password=script_args.user_pass)
        except vk.exceptions.VkAuthError:
            logger.debug('Cant auth in VK.')
            logger.debug('Script finish')
            exit(1)
    
    vkapi = vk.API(vksession)
        
    vk_user_all_data = vkapi.users.get(user_id=script_args.vk_id, fields='online')
    
    logger.debug('User online status: %s', vk_user_all_data[0]['online'])
    print(vk_user_all_data[0]['online'])
    
    logger.debug('Script finish')
    
#
# function parse_args()
#
def parse_args():
    usage = "Usage: %prog [options]"
    
    parser = optparse.OptionParser(usage)
    
    parser.add_option("-i", "--id", action="store", type="string", dest="vk_id", metavar="VK_ID", help="Required argument! Set user id.")
    parser.add_option("-a", "--app", action="store", type="string", dest="app_id", metavar="APP_ID", help="VK App id.")
    parser.add_option("-u", "--user", action="store", type="string", dest="user_name", metavar="USER_NAME", help="Set user name for auth.")
    parser.add_option("-p", "--pass", action="store", type="string", dest="user_pass", metavar="USER_PASS", help="Set user password for auth.")
    parser.add_option("-l", "--log", action="store", type="string", dest="dst_log_file", metavar="DST_LOG_FILE", help="If set - script try to write log to this file.")
    
    (options, args) = parser.parse_args()
    
    if options.vk_id == None:
        parser.error("Required arguments not set. For more info use key --help .")
    
    return (options)
    


if __name__ == '__main__':
    main()