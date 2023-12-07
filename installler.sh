#!/bin/bash

install_python_pip(){
    
    pip install --upgrade pip
    pip install -r assets/requirements.txt
    pip install

}

create_services(){

    sudo mkdir -p /etc/Camera
    sudo cp -r ./Camera/* /Camera/
    sudo cp Camera/assets/camera.service /etc/systemd/system/camera.service
    sudo systemctl daemon-reload
    sudo systemctl enable camera.service
    sudo systemctl start camera.service

    sudo mkdir -p /etc/VisitantSearcher
    sudo cp -r ./VisitantSearcher/* /etc/VisitantSearcher/
    sudo cp VisitantSearcher/assets/visitantsearcher.service /etc/systemd/system/visitantsearcher.service
    sudo systemctl daemon-reload
    sudo systemctl enable visitantsearcher.service
    sudo systemctl start visitantsearcher.service

    sudo mkdir -p /etc/StreamerServer
    sudo cp -r ./StreamerServer/* /etc/StreamerServer/
    sudo cp StreamerServer/assets/streamerserver.service /etc/systemd/streamerserver.service
    sudo systemctl daemon-reload
    sudo systemctl enable streamerserver.service
    sudo systemctl start streamerserver.service

}

create_virtual_env(){
    
}