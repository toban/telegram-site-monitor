#!/bin/bash
#docker pull selenium/standalone-chrome
docker run --rm -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome
