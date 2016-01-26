#!/usr/bin/python
# coding=utf-8

#
# Import
#
import logging
import optparse

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
	
	logger.debug('Script arguments set to receive: %s', script_args.get_value_name)
	
	source_data_file = "/proc/sys/fs/file-nr"
	logger.debug('Try to open source file %s', source_data_file)

	try:
		src_file_ptr = open(source_data_file, "r")
	except IOError:
		logger.debug('Cant open source file %s', source_data_file)
		logger.debug('Script abort execution')
		exit(1)
			
	logger.debug('Try to read source file %s', source_data_file)
	file_data_string = src_file_ptr.read().replace('\n', '')
	
	file_data_values = file_data_string.split('\t') 

	#
	# Try to get value from data
	#	
	descriptors_count = 0
		
	if script_args.get_value_name == "allocated":
		try:
			descriptors_count = file_data_values[0]
		except IndexError:
			logger.debug('Cant parse data')
			print(descriptors_count)
			exit(1)
	elif script_args.get_value_name == "maximum":
		try:
			descriptors_count = file_data_values[2]
		except IndexError:
			logger.debug('Cant parse data')
			print(descriptors_count)
			exit(1)
	else:
		descriptors_count = 0
		
	logger.debug('Descriptors count value: %s', descriptors_count)
	print(descriptors_count)
	
	logger.debug('Close source file %s', source_data_file)
	src_file_ptr.close();
	
	logger.debug('Script finish')
	
#
# function parse_args()
#
def parse_args():
	usage = "Usage: %prog [options]"
	
	parser = optparse.OptionParser(usage)
	
	parser.add_option("-g", "--get", action="store", type="choice", dest="get_value_name", choices=["allocated", "maximum"], help="Select one of the values: allocated, maximum")
	parser.add_option("-l", "--log", action="store", type="string", dest="dst_log_file", metavar="DST_LOG_FILE", help="If set - script try to write log to this file.")
	
	(options, args) = parser.parse_args()
	
	if options.get_value_name == None:
	    parser.error("Arguments not set. For more info use key --help .")
	
	return (options)
	


if __name__ == '__main__':
	main()