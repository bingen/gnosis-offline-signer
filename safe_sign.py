import sys, getopt
import json
from getpass import getpass
from eth_account import Account
from hexbytes import HexBytes

"""
Main logic extracted from:
https://github.com/gnosis/gnosis-py
"""

def signature_to_bytes(v: int, r: int, s: int) -> bytes:
    """
    Convert ecdsa signature to bytes
    :param v:
    :param r:
    :param s:
    :return: signature in form of {bytes32 r}{bytes32 s}{uint8 v}
    """

    byte_order = "big"

    return (
        r.to_bytes(32, byteorder=byte_order)
        + s.to_bytes(32, byteorder=byte_order)
        + v.to_bytes(1, byteorder=byte_order)
    )

def sign(private_key: str, safe_tx_hash: HexBytes) -> bytes:
    """
    {bytes32 r}{bytes32 s}{uint8 v}
    :param private_key:
    :return: Signature
    """
    account = Account.from_key(private_key)
    signature_dict = account.signHash(safe_tx_hash)
    signature = signature_to_bytes(
        signature_dict["v"], signature_dict["r"], signature_dict["s"]
    )

    """
    # Insert signature sorted
    if account.address not in self.signers:
        new_owners = self.signers + [account.address]
        new_owner_pos = sorted(new_owners, key=lambda x: int(x, 16)).index(
            account.address
        )
        self.signatures = (
            self.signatures[: 65 * new_owner_pos]
            + signature
            + self.signatures[65 * new_owner_pos :]
        )
    """
    return signature

def get_private_key(keystore: str) -> str:
    with open(keystore) as f:
        encrypted = f.readlines()

    password = getpass("Enter password:")

    return Account.decrypt(json.loads(encrypted[0]), password)

def trim_tx_hash(safe_tx_hash: str) -> str:
    if safe_tx_hash[0:2] == "0x":
        return safe_tx_hash[2:]
    return safe_tx_hash

def get_args(argv):
    help_string = 'Usage: python3 safe_sign.py -s hash -k keystore'
    if len(argv) < 4:
        print(help_string)
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv,"hs:k:",["hash=,keystore="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt in ("-s", "--hash"):
            safe_tx_hash = arg
        elif opt in ("-k", "--keystore"):
            keystore = arg

    return safe_tx_hash, keystore

if __name__ == "__main__":
    safe_tx_hash, keystore = get_args(sys.argv[1:])
    safe_tx_hash = trim_tx_hash(safe_tx_hash)
    pk = get_private_key(keystore)
    hb = HexBytes(safe_tx_hash)
    signature = sign(pk, hb)

    print(HexBytes(signature).hex())
