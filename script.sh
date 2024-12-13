#!/bin/bash

pip3 install --upgrade pip
pip3 install virtualenv
virtualenv venv
source ./venv/bin/activate

npm install
npm install
npm audit fix
pip3 install flask
pip3 install flask_cors
pip3 install pandas
pip3 install numpy
pip3 install fpdf