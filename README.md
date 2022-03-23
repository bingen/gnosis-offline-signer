# Simple offline Gnosis Safe signer

## Install

```
git clone https://gitlab.com/bingen/gnosis-offline-signer.git
cd gnosis-offline-signer
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Usage:

```
python3 ./safe_sign.py -s <your-safe-tx-hash> -k <your-wallet-keystore-file>
```

Main logic extracted from [gnosis-py](https://github.com/gnosis/gnosis-py).
