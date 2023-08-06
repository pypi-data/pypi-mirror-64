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

    def __init__(self, user: str, host: str, port: int = 22, connect_kwargs: Dict = None):
        
        if not user and host:
            raise ClientError("user and host are required.")
        
        self.user: str = user
        self.port: int = port
        self.cmd: str = ""
            
        super(Connection, self).__init__(user=self.user, host=self.host, port=self.port, connect_kwargs=connect_kwargs)
        

    def detect_os(self) -> str:
        """
        This function will finger print the remote Operating System by checking the lsb-release for ubuntu/deb versions.
        and redhat-release for centos/redhat versions.
        :return: either debian or centos
        """
        # Check OS Version
        relases = [x for x in self.conn.run('ls -1 /etc/').stdout.strip().split('\n')]

        if 'redhat-release' in relases:
            return 'redhat'

        if 'lsb-release' in relases:
            return 'debian'

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
    
    def install(self, packages: List[str], os_name: str = 'ubuntu') -> List[str]:
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
            return self.sudo(self.cmd).stdout.strip().split("\n")
            
        except ClientError as e: 
            raise ClientError(f"Unable to install packages {', '.join(packages)}") from e
            
            
    def install_docker_ce(self) -> List[str]:
        """
        This function will install docker community edition to the remote ubuntu server
        :return: output from installastion
        """

        # Check OS Version
        os_version = self.detect_os()
        if os_version != 'debian':
            raise EnvironmentError("ERROR: Remote Operation System is not Ubuntu")

        commands = ['apt-get install -y apt-transport-https ca-certificates  curl software-properties-common',
                    'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - ',
                    'apt-key fingerprint 0EBFCD88',
                    'add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"',
                    'apt-get install docker-ce -y'
                    ]

        try:
            # run the command in batch
            print("[+] Succefully installing  Docker-CE")
            response: List = []
            for cmd in commands:
                response.extend(self.conn.sudo(cmd).stdout.strip().split('\n'))

            return response

        except ClientError as e:
            raise ClientError("ERROR: Unable to install DOCKER-CE ", "X")

    def deploy_hadoop(self):
        pass

