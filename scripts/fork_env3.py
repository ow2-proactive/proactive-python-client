DOCKER_ENABLED = True
if variables.get("DOCKER_ENABLED") is not None:
    if str(variables.get("DOCKER_ENABLED")).lower() == 'false':
        DOCKER_ENABLED = False

DOCKER_IMAGE = 'activeeon/dlm3'
if variables.get("DOCKER_IMAGE") is not None:
    DOCKER_IMAGE = variables.get("DOCKER_IMAGE")

print('Fork environment info...')
print('DOCKER_ENABLED:     ' + str(DOCKER_ENABLED))
print('DOCKER_IMAGE:       ' + DOCKER_IMAGE)

if DOCKER_ENABLED:
    #Be aware, that the prefix command is internally split by spaces. So paths with spaces won't work.
    # Prepare Docker parameters
    containerName = DOCKER_IMAGE
    dockerRunCommand =  'docker run '
    dockerParameters = '--rm '
    # Prepare ProActive home volume
    paHomeHost = variables.get("PA_SCHEDULER_HOME")
    paHomeContainer = variables.get("PA_SCHEDULER_HOME")
    proActiveHomeVolume = '-v '+paHomeHost +':'+paHomeContainer+' '
    # Prepare working directory (For Dataspaces and serialized task file)
    workspaceHost = localspace
    workspaceContainer = localspace
    workspaceVolume = '-v '+localspace +':'+localspace+' '
    # Prepare container working directory
    containerWorkingDirectory = '-w '+workspaceContainer+' '
    # Save pre execution command into magic variable 'preJavaHomeCmd', which is picked up by the node
    preJavaHomeCmd = dockerRunCommand + dockerParameters + proActiveHomeVolume + workspaceVolume + containerWorkingDirectory + containerName
    print('DOCKER_FULL_CMD:    ' + preJavaHomeCmd)
else:
    print("Fork environment disabled")
