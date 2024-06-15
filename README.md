# wen_patch
Repo name is old. Discord bot testing for fun!

* requirements.txt defines the python dependencies needed
* Dockerfile will build a container with the dependencies. Github actions uploads it to Github repo.
* Place config.cfg into some location and add the token
* Start container with `podman run -v <config_location>:/etc wen_patch:0.0.1`
