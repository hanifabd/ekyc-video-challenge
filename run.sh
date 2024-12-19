# #!/bin/bash

# # Build the Docker image
# IMAGE_NAME=llm-core
# docker build -t $IMAGE_NAME .

# # Run the Docker container
# HOST_PORT=8081
# CONTAINER_PORT=8081
# CONTAINER_NAME=llm-core
# echo -e "-----------------------------------------------"
# echo -e "Build Docker Image\nName: $IMAGE_NAME"
# echo -e "Container: $CONTAINER_NAME"
# echo -e "Port:\n    Host: $HOST_PORT\n    Container: $CONTAINER_PORT"
# echo -e "-----------------------------------------------"
# docker run --gpus all --name $CONTAINER_NAME -p $HOST_PORT:$CONTAINER_PORT -e CUDA_LAUNCH_BLOCKING=1 $IMAGE_NAME