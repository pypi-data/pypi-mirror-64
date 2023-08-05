"""Process"""
import os
import subprocess

def start_mysql_server(mysql_bin_folder,mysql_config_file):
	DETACHED_PROCESS = 0x00000008	
	return subprocess.Popen([os.path.join(mysql_bin_folder,"mysqld.exe"),"--defaults-file="+mysql_config_file,"--standalone"],creationflags=DETACHED_PROCESS).pid
