deactivate
rm -rf .venv
rm -rf bin
mkdir .venv
python3 -m venv .venv
source .venv/bin/activate

pip3 install --no-deps --find-links . -r ../shared/api_requirements.txt
pip3 install --no-deps -e ../../src/vc_api
pip3 check
