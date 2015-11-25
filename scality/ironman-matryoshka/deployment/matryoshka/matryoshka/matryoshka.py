#!/usr/bin/env python2

from docker import Client, tls
import os
import sys
import subprocess
import yaml

import time
# -------------------------------------
#  CONFIGURATION
# -------------------------------------
# circleci
VERSION = '1.20'
DOCKER_HOST_ENV_VAR = 'DOCKER_HOST'
# matryoshka
FUNCTIONAL_TEST_DIR = 'functional'

# yaml configuration file
YAML_CONF_FILE = "master.yml"
# constants to parse the above file
MATRYOSHKA_INDEX = 0
TEST_INDEX = 1
MATRYOSHKA_SECTION = 'matryoshka'
COMPOSE_SECTION = 'docker-compose.yml'
DOLL_IMAGE = 'image'
DOLL_TAG = 'tag'
DOLL_STARTUP = 'startup'
DOLL_CONFIGURE = 'configure'
TEST_ON = True  # do not ask
TEST_EXEC = 'exec'
TEST_CODE = 'okCode'
CURRENT_IMAGE = 'current'
DOCKER_USER_ENV = 'docker_user'
DOCKER_PASSWORD_ENV = 'docker_password'
DOCKER_REPO_ENV = 'docker_server'
# -------------------------------------
#  GLOBALS
# ------------------------------------
# gateway to docker on circleci
base_url = 'unix://var/run/docker.sock'
client = None
# the docker image of the software being built
dockerImage = None  # referenced as current in master.yml
pulledImages = set(['dochub.ironmann.io:5000/ironman-baselatest'])
dockerHasLogin = False
# ------------------------------------

# first argument is the container Id
# second argument is the command to run
# return a tuple composed of the return code of the command (integer)
# and of the output of the command (as a string)
# (the output comprised both the stdin and stderr)


def runInDocker(container, command):
    containerId = container.get('Id')
    containerName = container.get('Name') 
    if containerName.startswith('/'):
       containerName=containerName[1:]
    # circleci does not allow running command inside docker
    # see https://circleci.com/docs/docker#docker-exec
    # we need to run bash before command otherwise the substitution of the IP
    # var might not be ok
    # No need to infer a real IP - just feed the loopback to the test script
    command = "export IP=127.0.0.1 ; " + command
    if os.environ.get('CIRCLECI'):
        command = "cd /mnt  ; " + command
    	fullCmd = "sudo lxc-attach -n " + containerId + \
        	" -- bash -c \' " + command + " \'"
    else:
       command = "cd /test ; " + command 
       fullCmd = "docker exec "+ containerName + \
                " bash -c \' " + command + " \'" 
    print("running "+fullCmd)
    try:
        return (0,
                subprocess.check_output(fullCmd,
                                        stderr=subprocess.STDOUT,
                                        shell=True
                                        )
                )
    except subprocess.CalledProcessError as e:
        # exit code is not zero
        return (e.returncode, e.output)

# needs love
def runBuildCompose(dir,command):
    command='cd '+dir+' ; '+ command
    try: 
         return subprocess.check_output(command,
                                   stderr=subprocess.STDOUT,
                                   shell=True
                                   )
    except subprocess.CalledProcessError as e:
        # exit code is not zero
        return e.output

def populateDocker(dir):
    result = {}
    try:
         dockersId=subprocess.check_output('cd '+dir+' ; docker-compose ps -q',
                                   stderr=subprocess.STDOUT,
                                   shell=True
                                   )
    except subprocess.CalledProcessError as e:
         print('failed to gather list of running containers from compose')
         print(e.output)
         sys.exit(-1)
    for dockerId in dockersId.splitlines():
        docker=client.inspect_container(dockerId)
        name=docker['Name']
        # py-docker quirk ?
        if name.startswith('/'):
              name=name[1:]
        print("populating "+name)
        result[name]=docker
    return result

# This function runs a test. The test is an executable command
# run on a specific docker
# - arg 1 : path of the test suite (mandatory)
# - arg 2 : name of the test (mandatory)
# - arg 3 : docker container on which the test should run (mandatory)
# - arg 4 : execTest executable test file (mandatory)
# - arg 5 : okCode exit code to check after executing
#           - if None will be considered as 0
# return True if passed, False otherwise


def runTest(dir, name, container, execTest, okCode):
    if okCode is None:
        okCode = 0
    (code, result) = runInDocker(container, execTest)
    print("Ran " + dir + " " + name)
    print(result)
    if code != okCode:
        print(dir + " " + name + " failed")
        print("exit code is " + str(code))
        return False
    return True


def stopDocker(container):
    client.stop(container=container.get('Id'), timeout=10)


# This function creates a docker container:
# - arg 1 : path of the test suite (mandatory)
# - arg 2 : name of the docker instance (mandatory)
# - arg 3 : docker image to use (mandatory)
# - arg 4 : tag of the docker image (optional)
# - arg 5 : command line startup (optional - can be None)
# - arg 6 : command line configuration (optional - can be None)
# returns the running container


def setupDocker(dir, name, image, tag, startup, configure):
    global dockerHasLogin, pulledImages
    if tag is None:
        tag = 'latest'
    if image == CURRENT_IMAGE:
        image = dockerImage
    else:
        # make sure we have the image locally
        if (image + tag) not in pulledImages:
            if not dockerHasLogin:
                email = os.environ['CIRCLE_USERNAME'] + "@" + \
                    os.environ['CIRCLE_PROJECT_USERNAME'] + '.com'
                client.login(username=os.environ[DOCKER_USER_ENV],
                             password=os.environ[DOCKER_PASSWORD_ENV],
                             registry=os.environ[DOCKER_REPO_ENV],
                             email=email)
                dockerHasLogin = True
            response = client.pull(repository=image, tag=tag)
            print(response)
            pulledImages.add(image + tag)
    config = client.create_host_config(
        network_mode='host', privileged=False, binds=[dir + ':/mnt'])
    container = None
    image = image + ':' + tag
    if startup is None:
        container = client.create_container(
            image=image, volumes=['/mnt'], host_config=config)
    else:
        container = client.create_container(
            image=image, volumes=['/mnt'], host_config=config, command=startup)
    client.start(container=container.get('Id'))
    if configure:
        (code, result) = runInDocker(container, configure)
        print(dir + " " + name + " configure exited" + str(code))
        print(result)
    return container

# this procedure gathers the output of all the docker and sends in
# on stdout
# it takes one argument : a dictionary name ==> docker container


def log(dockers):
    for name, container in dockers.iteritems():
        print(name + " says ----------------------------------")
        output = client.logs(container=container.get(
            'Id'), stdout=True, stderr=True, stream=False, timestamps=True)
        print(output)

# this function takes a yamlfile in argument along
# with the directory where the test suite is located
# it  triggers the processing of the test suite
# returns True if the test passed, False otherwise


def parse(yamlfile, dir):
    matryoshka = None
    tests = None
    with open(yamlfile, 'r') as stream:
        testConf = list(yaml.load_all(stream))
        if(len(testConf) != TEST_INDEX + 1):
            print(yamlfile + " error it should contain two yaml documents")
            sys.exit(-1)
    matryoshka = testConf[MATRYOSHKA_INDEX]
    tests = testConf[TEST_INDEX]
    compose = None
    if matryoshka == MATRYOSHKA_SECTION:
        matryoshka = matryoshka[MATRYOSHKA_SECTION]
    else:
        compose = list(matryoshka)
        if compose and len(compose) ==1 and compose[0]==COMPOSE_SECTION:
             compose = matryoshka[COMPOSE_SECTION]
	else:
             print(yamlfile + " the first yaml should start by "+MATRYOSHKA_SECTION+"  or by "+COMPOSE_SECTION)
             sys.exit(-1)
    dockers = {}
    # setup the environment
    if compose:
        for cmd in compose:
            print("Executing "+ cmd + " in "+dir)
            output=runBuildCompose(dir,cmd)
            print(output)
            dockers=populateDocker(dir)
    elif matryoshka:
        for doll in matryoshka:
            name = list(doll.keys())[0]
            image = doll[name][DOLL_IMAGE]
            tag = doll[name].get(DOLL_TAG)
            startup = doll[name].get(DOLL_STARTUP)
            configure = doll[name].get(DOLL_CONFIGURE)
            print("Creating docker=" + name + " with " + image +
                  " startup=" + str(startup) + " configure=" + str(configure))
            dockers[name] = setupDocker(
                dir, name, image, tag, startup, configure)
            # output the result of starting the different docker
            # not a very obvious thing - the lxc command are displayed already
            # lxc command maps to exec in the  master.yml (circleci quirk)
            # but not the real docker startup commands
            # NEED LOVE HERE: get streams to work here
            log(dockers)
    # run tests
    passed = True
    for test in tests:
        name = list(test.keys())[0]
        doll = test[name][TEST_ON]
        exectest = test[name][TEST_EXEC]
        okCode = test[name].get(TEST_CODE)
        print("Running test=" + name + " on " + doll +
              " with " + exectest + " okCode=" + str(okCode))
        if doll not in dockers:
            print(dir + " " + name + " :  unable to find " + doll)
            print("is " + doll + " missing in the " + MATRYOSHKA_SECTION +
                  " section of the file " + yamlfile + " ?")
            sys.exit(-1)
        success = runTest(dir, name, dockers[doll], exectest, okCode)
        if not success:
            passed = False
            if 'STOP_ON_ERROR' in os.environ:
                sys.exit(-1)
    # output the result of starting the different docker
    # not a very obvious thing - the lxc command are displayed already
    # lxc command maps to exec in the  master.yml (circleci quirk)
    # but not the real docker startup commands
    # NEED LOVE HERE: get streams to work here
    log(dockers)
    # destroy environments
    for _, container in dockers.iteritems():
        stopDocker(container)
    return passed


def main():
    global base_url, dockerImage, client
    if(len(sys.argv) > 1):
        dockerImage = sys.argv[1]
    # find the docker
    if os.environ.get(DOCKER_HOST_ENV_VAR):
        base_url = os.environ[DOCKER_HOST_ENV_VAR]
    if os.environ.get('DOCKER_CERT_PATH'):
        tls_config = tls.TLSConfig(
            client_cert=('/Users/marcsegura-devillechaise//.docker/machine/machines/default/cert.pem',
                         '/Users/marcsegura-devillechaise//.docker/machine/machines/default/key.pem')
            #                verify='/Users/marcsegura-devillechaise//.docker/machine/machines/default/ca.pem'
        )
        client = Client(base_url='tcp://192.168.99.100:2376',
                        version=VERSION, tls=True)
    else:
        client = Client(base_url=base_url, version=VERSION)
    # where is ./ci/functional ?
    functionalDir = os.path.join(os.path.dirname(
        os.path.abspath(sys.argv[0])), FUNCTIONAL_TEST_DIR)
    if len(sys.argv) > 2:
        sys.argv.pop(0)
        testDirs = sys.argv
    else:
        # which directories does it contain ? sort the result
        testDirs = sorted([os.path.join(functionalDir, o) for o in os.listdir(
            functionalDir) if os.path.isdir(os.path.join(functionalDir, o))])
    # iterate over the test suites (i.e.directories)
    passed = True
    for testDir in testDirs:
        print("Testing in " + testDir)
        yamlfile = os.path.join(testDir, YAML_CONF_FILE)
        if os.path.isfile(yamlfile):
            success = parse(yamlfile, testDir)
            if not success:
                passed = False
        else:
            print("No file " + yamlfile + " found - SKIPPING")
    # ensure circleci returns an error
    if not passed:
        sys.exit(-1)


if __name__ == "__main__":
    main()
