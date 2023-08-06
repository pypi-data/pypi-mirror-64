#!/usr/bin/env python 
"""
Name: Rio Atmadja 
Date: 02 April 2020 
Description: This class extends the functionality in fabric class
"""
from fabric import Connection
from botocore.exceptions import ClientError 
from typing import Dict, List

class ServerManager(Connection):

    def __init__(self, user:str, host: str, port: int = 22, passwd: str = None, connect_kwargs: Dict = None ):
        
        if not user and host:
            raise ClientError("user and host are required.")
        
        self.user : str = user 
        self.port : int = port 
        self.password: str = passwd
        self.cmd: str = ""     
            
        super(Connection, self).__init__(user=self.user, host=self.host, port=self.port ,connect_kwargs=connect_kwargs)
        

    def execute_cmd(self, cmd: str) -> List[str]:
        """
        This function will execute arbitrary commands 
        :param cmd: given the command to be executed 
        :return : List of outputs from the server.
        """
        try: 
            return self.sudo(cmd).stdout.strip().split("\n") 
        
        except ClientError as e:
            raise ClientError(f"Unable to connect to the servers") 
    
    def install(self, os_name: str = 'ubuntu' , packages: List[str]) -> List[str]:
        """
        This function will install, the given packages based on Operating System.
        The default Operating System is Ubuntu 
        :param os_name: given the linux operating system name, default is Ubuntu
        :param packages: given a list of packages to be installed in the remote servers 
        :return : List of outputs from the server.
        """
        if os_name: 
             self.cmd = f"apt-get update && apt-get install -y {' '.join(packages)}"
                
        else: 
            if not self.execute_cmd("ls -1 /etc | grep redhat"): 
                raise ClientError(f"Unable to determine the host server.") 
                
            self.cmd = f"yum update -y && yum install -y {' '.join(packages)}"
                
        try:
            return self.sudo(cmd).stdout.strip().split("\n") 
            
        except ClientError as e: 
            raise ClientError(f"Unable to install packages {}") from e 
            
            
            
            
            
            
            
            
            
