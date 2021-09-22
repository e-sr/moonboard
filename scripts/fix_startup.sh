#!/bin/bash
sudo systemctl stop moonboard
sudo systemctl stop com.moonboard

# startup in correct order
sudo systemctl restart com.moonboard
sudo systemctl restart moonboard
