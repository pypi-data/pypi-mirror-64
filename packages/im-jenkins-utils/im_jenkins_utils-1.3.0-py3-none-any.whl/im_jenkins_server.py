#!/usr/bin/env python

"""A Python 3 module to aid the automation of the configuration and backup of
a Jenkins server. It has limited capabilities that currently include the
setting and getting of Job configurations and the setting of secrets in the
form of text, user names & passwords and files.

If SSL certificates are not properly installed you may need to defeat the
built-in Python SSL validation that takes place. You can do this with the
following environment variable: -

    export PYTHONHTTPSVERIFY=0
"""

import configparser
import logging
import glob
import json
import os
import subprocess

import jenkins


# pylint: disable=too-few-public-methods
# pylint: disable=no-member
class ImJenkinsServer(object):
    """Class providing Jenkins configuration services.
    """

    CREDENTIALS_API = 'credentials/store/system/domain/_/createCredentials'

    def __init__(self, url, config_file=None):
        """Initialise the Jenkins server for the given url. The url is
         typically of the form https://<user>:token>@<url>. If a configuratio
         file is supplied this will be loaded and used.

        :param url: The server URL
        :type url: ``String``
        :param config_file: Path to a configuration file (or None)
        :type v: ``String``
        """
        # Our logger...
        self.logger = logging.getLogger(self.__class__.__name__)

        # Connect (and then try and get the server version)...
        self.logger.debug('Connecting to Jenkins...')
        self.url = url
        self.server = None
        self.server_version = None
        try:
            self.server = jenkins.Jenkins(url)
        except BaseException as error:
            self.logger.error('Failed to connect')
            self.logger.info(error)

        if self.server:
            try:
                self.server_version = self.server.get_version()
            except BaseException as error:
                self.logger.error('Failed to get server version')
                self.logger.info(error)
            if self.server_version:
                self.logger.debug('Connected (Jenkins v%s)',
                                  self.server_version)

        # Read config file?
        self.config_file = config_file
        self.config = None
        if self.config_file:
            self.config = configparser.ConfigParser()
            self.config.read(self.config_file)

    def is_connected(self):
        """Returns true if connected to Jenkins.

        :return: True if connected
        :rtype: ``bool``
        """
        return self.server_version is not None

    def get_jobs(self, dst_dir):
        """Gets all the job configurations from the server.
        The jobs are extracted in their raw XML form and written to the
        directory provided using the Job name as the basename of the file.

        :param dst_dir: The directory to store the configurations,
                        which has to exist.
        :type dst_dir: ``String``
        :return: Number of jobs retrieved
        :rtype: ``int``
        """
        # Do nothing if we do not appear to be connected.
        if not self.server_version:
            return 0

        self.logger.debug('Getting job configurations into "%s"...', dst_dir)

        if not os.path.isdir(dst_dir):
            self.logger.error('%s is not a directory', dst_dir)
            return 0

        num_got = 0
        jobs = self.server.get_jobs()
        for job in jobs:
            job_name = job['name']
            self.logger.debug('Getting "%s"...', job_name)
            job_config = self.server.get_job_config(job_name)
            job_config_filename = os.path.join(dst_dir, job_name + '.xml')
            job_file = open(job_config_filename, 'w')
            job_file.write(job_config)
            job_file.close()
            num_got += 1

        self.logger.debug('Got (%s)', num_got)

        return num_got

    def set_jobs(self, src_dir, set_disabled=False, force=False):
        """Writes the jobs in the given directory to the server.

        :param src_dir: The source directory, which must exist
        :type src_dir: ``String``
        :param set_disabled: True to disable the job once it has been
                             created (or reconfigured)
        :type set_disabled: ``Boolean``
        :param force: True to force the action
        :type force: ``Boolean``
        :return: Number of jobs written
        :rtype: ``int`
        """
        # Do nothing if we do not appear to be connected.
        if not self.server_version:
            return 0

        if not os.path.isdir(src_dir):
            self.logger.error('%s is not a directory', src_dir)
            return 0

        self.logger.debug('Setting job configurations from "%s"...', src_dir)

        # Iterate through all the jobs...
        num_set = 0
        job_files = glob.glob('%s/*.xml' % src_dir)
        for job_file in job_files:
            # The name of the job is the basename of the file.
            # and we simply load the file contents (into a string)
            # to create the job (if the job does not exist)
            job_name = os.path.basename(job_file)[:-4]
            job_exists = self.server.job_exists(job_name)
            if job_exists and not force:
                self.logger.warning('Skipping "%s" (Already Present)', job_name)
            else:
                job_definition = open(job_file, 'r').read()
                if job_exists:
                    self.logger.debug('Reconfiguring "%s"...', job_name)
                    self.server.reconfig_job(job_name, job_definition)
                else:
                    self.logger.debug('Creating "%s"...', job_name)
                    self.server.create_job(job_name, job_definition)
                # Optionally disable each job as it's created
                if set_disabled:
                    self.server.disable_job(job_name)
                num_set += 1

        self.logger.debug('Set (%s)', num_set)

        # Success if we get here...
        return num_set

    def get_views(self, dst_dir):
        """Gets all the view configurations from the server (except the 'all' view).
        The views are extracted in their raw XML form and written to the
        directory provided using the view name as the basename of the file.

        :param dst_dir: The directory to store the configurations,
                        which has to exist.
        :type dst_dir: ``String``
        :return: Number of views retrieved
        :rtype: ``int``
        """
        # Do nothing if we do not appear to be connected.
        if not self.server_version:
            return 0

        self.logger.debug('Getting view configurations into "%s"...', dst_dir)

        if not os.path.isdir(dst_dir):
            self.logger.error('%s is not a directory', dst_dir)
            return 0

        num_got = 0
        views = self.server.get_views()
        for view in views:
            view_name = view['name']
            if view_name in ['all']:
                continue
            self.logger.debug('Getting "%s"...', view_name)
            view_config = self.server.get_view_config(view_name)
            view_config_filename = os.path.join(dst_dir, view_name + '.xml')
            view_file = open(view_config_filename, 'w')
            view_file.write(view_config)
            view_file.close()
            num_got += 1

        self.logger.debug('Got (%s)', num_got)

        return num_got

    def set_views(self, src_dir, force=False):
        """Writes the views in the given directory to the server.

        :param src_dir: The source directory, which must exist
        :type src_dir: ``String``
        :param force: True to force the action
        :type force: ``Boolean``
        :return: Number of views written
        :rtype: ``int`
        """
        # Do nothing if we do not appear to be connected.
        if not self.server_version:
            return 0

        if not os.path.isdir(src_dir):
            self.logger.error('%s is not a directory', src_dir)
            return 0

        self.logger.debug('Setting view configurations from "%s"...', src_dir)

        # Iterate through all the views...
        num_set = 0
        view_files = glob.glob('%s/*.xml' % src_dir)
        for view_file in view_files:
            # The name of the view is the basename of the file.
            # and we simply load the file contents (into a string)
            # to create the view (if the job does not exist)
            view_name = os.path.basename(view_file)[:-4]
            view_exists = self.server.view_exists(view_name)
            if view_exists and not force:
                self.logger.warning('Skipping "%s" (Already Present)', view_name)
            else:
                view_definition = open(view_file, 'r').read()
                if view_exists:
                    self.logger.debug('Reconfiguring "%s"...', view_name)
                    self.server.reconfig_view(view_name, view_definition)
                else:
                    self.logger.debug('Creating "%s"...', view_name)
                    self.server.create_view(view_name, view_definition)
                num_set += 1

        self.logger.debug('Set (%s)', num_set)

        # Success if we get here...
        return num_set

    def check_jobs(self, verbose=False):
        """Checks all the jobs on the server. If any have failed or are
        unstable (i.e. where colour begins 'red' or 'yellow') then this call
        returns False, otherwise it returns True. Basically if this call
        returns False then a job on the server has failed or is unstable.

        This method also returns False if the server is not connected.

        :param verbose: True to generate stdout
        :type verbose: ``Boolean``
        :return: False if any job has failed or is unstable.
        """
        # Do nothing if we do not appear to be connected.
        if not self.server_version:
            print('[Failed to connect]')
            return False

        # Are we told to exclude jobs via a config file?
        exclude_jobs = []
        if self.config and self.config.has_option('check', 'exclude-job'):
            # We have some jobs to exclude.
            # Convert all to lower-case - we assume case is not important
            job_names = self.config.get('check', 'exclude-job').split('\n')
            for job_name in job_names:
                exclude_jobs.append(job_name.lower())

        # Check the 'colour' of every job...
        # Unless it's in the excluded list.
        jobs = self.server.get_jobs()
        num_ok = len(jobs)
        num_ignored = 0
        num_red = 0
        num_yellow = 0
        for job in jobs:
            if job['name'].lower() in exclude_jobs:
                num_ignored += 1
                continue
            job_colour = job['color'].lower()
            if job_colour.startswith('red'):
                num_red += 1
                num_ok -= 1
            elif job_colour.startswith('yellow'):
                num_yellow += 1
                num_ok -= 1
            # If not verbose then we can return on the first failure
            if not verbose and (num_yellow or num_red):
                return False

        if verbose:
            if not num_red and not num_yellow:
                print('%d ok, %d ignored' % (num_ok, num_ignored))
            else:
                print('%d ok, %d ignored, %d err, %d fail' % (num_ok,
                                                              num_ignored,
                                                              num_yellow,
                                                              num_red))

        if num_yellow or num_red:
            return False
        return True

    def set_secret_text(self, identity, secret,
                        description='Secret Text'):
        """Uses the jenkins API (and cURL) to set a text-based secret.

        :param identity: The ID to use to refer to the secret
        :param secret: The secret text
        :param description: The secret's description
        """
        # Do nothing if we do not appear to be connected.
        if not self.server_version:
            return 0

        self.logger.debug('+ Setting text "%s"...', identity)
        payload = {
            '': '0',
            'credentials': {
                'scope': 'GLOBAL',
                'id': identity,
                'secret': secret,
                'description': description.replace("'", ""),
                '$class': 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl'
            }
        }
        content = {'url': self.url + '/' + ImJenkinsServer.CREDENTIALS_API,
                   'json': json.dumps(payload)}
        cmd = "curl -X POST '%(url)s'" \
              " --data-urlencode 'json=%(json)s'" % content
        completed_process = subprocess.run(cmd,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
        if completed_process.returncode != 0:
            self.logger.error('POST failed (returncode=%d), stderr follows',
                              completed_process.returncode)
            self.logger.error('%s', completed_process.stderr.decode('utf-8'))
            return False

        return True

    def set_secret_file(self, identity, filename,
                        description='Secret File'):
        """Uses the jenkins API (and cURL) to set a file-based secret.

        :param identity: The ID to use to refer to the secret
        :param filename: The file to load
        :param description: The secret's description
        """
        # Do nothing if we do not appear to be connected.
        if not self.server_version:
            return 0

        self.logger.debug('+ Setting file "%s"...', identity)
        payload = {
            '': '4',
            'credentials': {
                'scope': 'GLOBAL',
                'id': identity,
                'file': 'secret',
                'description': description.replace("'", ""),
                '$class': 'org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl'
            }
        }
        content = {'url': self.url + '/' + ImJenkinsServer.CREDENTIALS_API,
                   'file': filename,
                   'json': json.dumps(payload)}
        cmd = "curl -X POST '%(url)s'" \
              " -F secret=@%(file)s -F 'json=%(json)s'" % content
        completed_process = subprocess.run(cmd,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
        if completed_process.returncode != 0:
            self.logger.error('POST failed (returncode=%d), stderr follows',
                              completed_process.returncode)
            self.logger.error('%s', completed_process.stderr.decode('utf-8'))
            return False

        return True

    def set_secret_user(self, identity, username, password,
                        description='Secret User'):
        """Uses the jenkins API (and cURL) to set a username/password-based secret.

        :param identity: The ID to use to refer to the secret
        :param username: The user's name
        :param password: The user's password
        :param description: The secret's description
        """
        # Do nothing if we do not appear to be connected.
        if not self.server_version:
            return 0

        self.logger.debug('+ Setting username/password "%s"...', id)
        payload = {
            '': '4',
            'credentials': {
                'scope': 'GLOBAL',
                'id': identity,
                'username': username,
                'password': password,
                'description': description.replace("'", ""),
                '$class': 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl'
            }
        }
        content = {'url': self.url + '/' + ImJenkinsServer.CREDENTIALS_API,
                   'json': json.dumps(payload)}
        cmd = "curl -X POST '%(url)s'" \
              " --data-urlencode 'json=%(json)s'" % content
        completed_process = subprocess.run(cmd,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=True)
        if completed_process.returncode != 0:
            self.logger.error('POST failed (returncode=%d), stderr follows',
                              completed_process.returncode)
            self.logger.error('%s', completed_process.stderr.decode('utf-8'))
            return False

        return True
