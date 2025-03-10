# outreach-app

A webapp resource for physicsy outreach activity.

---

## Overview

Build docker images using a selection custom webApps.

### Structure

  * dockerFiles: template files to create docker images
  * mainFiles: files for mainPages which contain sidebar title and links
  * _requirements_ and _temp_id_ files required for distributed images
  * content from sub-directories pages - see READMEs in directories

---

## Build and Run Custom Docker Image

1. Duplicate/Edit _dockerFiles/DockerFileComb_

  * add content of interest: copy _userPages_ directories from specific subdirectories

2. Build image

  From top directory:
  > docker build . -f dockerFiles/DockerFileComb -t web-app

3. Run container

  From top directory:
  > docker run -p 8501:8501 web-app

4. Open browser at _"localhost:8501"_

  You should see the _streamlit_ web applcation pages.

5. (Development) Run with mounted volume:

  This allows you to make _hot_ changes to files in the mounted directory - speeds up development muchly. Remember to re-build the image after the changes are settled.

  Mount the volume using _"-v"_ argument with local directory path on LHS of colon and container directory path on RHS, e.g.:

  > docker run -p 8501:8501 -v $(pwd)/pixSimApp/userPages/:/code/userPages/pixSimApp web-app

  **NB**

  a. Spaces in mounted directory paths are tricky (and hidden if you use symlinks or '$' paths). You may see an error:
  > docker: invalid reference format: repository name must be lowercase.

    * In this case use quotations around the mount paths, e.g.:
    > docker run -v "LOCAL_PATH:CONTAINER_PATH" my-image

  b. Windows users may have to use _PWD_ instead _pwd_.

  c. Powershell users should use _curled_ brackets, i.e. _${PWD}_ instead of _$(PWD)_


6. (_optional_) Push to dockerHub with _buildx_

  * An extra step is required to run containers across architectures, e.g. Apple Silicon (arm) and linux (amd).
  * Cross-architecture builds are made using docker's _buildx_ plugin for multi-platform images
  > docker buildx build --platform linux/amd64,linux/arm64 --push -f dockerFiles/DockerfileComb -t someRepo/web-app:multi .

  **NB** 
  
  No local image is made, it is pushed straight to repository. Hence, to run locally you must pull and run:
  > docker run -p 8501:8501 someRepo/web-app:multi

    * docker will select image appropriate to local architecture
  
  
## Troubleshooting

### Docker permission issue

```bash
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.40/containers/json: dial unix /var/run/docker.sock: connect: permission denied
```

In a terminal do ``sudo chmod 666 /var/run/docker.sock`` [source](https://www.digitalocean.com/community/questions/how-to-fix-docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket)

