#%% fork environment (python)
import os

DOCKER_ENABLED = True
if variables.get("DOCKER_ENABLED") is not None:
    if str(variables.get("DOCKER_ENABLED")).lower() == 'false':
        DOCKER_ENABLED = False

DOCKER_IMAGE = 'activeeon/dlm3'
if variables.get("DOCKER_IMAGE") is not None:
    DOCKER_IMAGE = variables.get("DOCKER_IMAGE")

DOCKER_GPU_ENABLED = False
if variables.get("DOCKER_GPU_ENABLED") is not None:
    if str(variables.get("DOCKER_GPU_ENABLED")).lower() == 'true':
        DOCKER_GPU_ENABLED = True

CUDA_ENABLED = False
CUDA_HOME = os.getenv('CUDA_HOME', None)
CUDA_HOME_DEFAULT = '/usr/local/cuda'
if CUDA_HOME is not None:
    if os.path.isdir(CUDA_HOME) == True:
        CUDA_ENABLED = True
else:
    if os.path.isdir(CUDA_HOME_DEFAULT) == True:
        CUDA_ENABLED = True

DOCKER_RUN_CMD = 'docker run '
if DOCKER_GPU_ENABLED and CUDA_ENABLED:
    DOCKER_RUN_CMD += '--runtime=nvidia '

print('Fork environment info...')
print('DOCKER_ENABLED:     ' + str(DOCKER_ENABLED))
print('DOCKER_IMAGE:       ' + DOCKER_IMAGE)
print('DOCKER_GPU_ENABLED: ' + str(DOCKER_GPU_ENABLED))
print('DOCKER_RUN_CMD:     ' + DOCKER_RUN_CMD)

if DOCKER_ENABLED == True:
    # Prepare Docker parameters
    containerName = DOCKER_IMAGE
    dockerRunCommand =  DOCKER_RUN_CMD
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
