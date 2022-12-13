#!/bin/bash
set -e
echo "BASH >> Ensure the python virtual environment is installed"
python3.8 -m venv ~/ntc
echo "BASH >> Activate the virtual environment"
source ~/ntc/bin/activate
echo "BASH >> Install application requirements within the virtual environment"
pip install -r ./requirements.txt
echo "BASH >> Install the ansbile collections for the environment"
ansible-galaxy install -r ./collections/requirements.yml
echo "BASH >> Execute the progrm"
ansible-playbook ./pb_configure_network.yml -i ./hosts
echo "BASH >> FINISHED"