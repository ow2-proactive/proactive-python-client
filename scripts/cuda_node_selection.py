#%% node_selection (python)
# job/task variables:
# GPU_NODES_ONLY: False (default)
import os

GPU_NODES_ONLY = False
if variables.get("GPU_NODES_ONLY") is not None:
  if str(variables.get("GPU_NODES_ONLY")).lower() == 'true':
    GPU_NODES_ONLY = True

CUDA_ENABLED = False
CUDA_HOME = os.getenv('CUDA_HOME', None)
CUDA_HOME_DEFAULT = '/usr/local/cuda'
if CUDA_HOME is not None:
  if os.path.isdir(CUDA_HOME) == True:
    CUDA_ENABLED = True
else:
  if os.path.isdir(CUDA_HOME_DEFAULT) == True:
    CUDA_ENABLED = True

selected = ((GPU_NODES_ONLY == False) or (GPU_NODES_ONLY == True and CUDA_ENABLED == True))
