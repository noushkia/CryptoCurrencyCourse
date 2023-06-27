# my public Address: mvw1uJQNoPAwwcEDZmdfax3F1GveG28Ewo

from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x

from mechanisms.conf import *
from utils import *

my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

prime_1 = 13
prime_2 = 11
prime_sum = prime_1 + prime_2
prime_sub = abs(prime_1 - prime_2)


def prime_scriptPubKey():
    # OP_2DUP (copy the 2 primes for the 2 ops)
    # OP_ADD
    # OP_SWAP (swap add result with 1st prime)
    # OP_ROT (send 2nd prime to the top)
    # OP_SUB
    # OP_ABS
    # OP_EQUALVERIFY (Compare subs)
    # OP_EQUAL       (Compares adds)
    return [OP_2DUP, OP_ADD,
            OP_SWAP, OP_ROT,
            OP_SUB, OP_ABS,
            prime_sub, OP_EQUALVERIFY,
            prime_sum, OP_EQUAL]


def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key]


def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)

    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptSig = P2PKH_scriptSig(txin, [txout], txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.00001
    txid_to_spend = 'c33c66e953577643db913ab1e6831c2059c8bbf1c00f45ea40a333df52790e52'  # TxHash of UTXO
    utxo_index = 0  # UTXO index among transaction outputs
    ######################################################################

    print('Base58 address: ', my_address)  # Prints your address in base58
    print('Public key: ', my_public_key.hex())  # Print your public key in hex
    print('Private key: ', my_private_key.hex())  # Print your private key in hex

    txout_scriptPubKey = prime_scriptPubKey()

    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)  # Report the hash of transaction which is printed in this section result

    """
    {
      "tx": {
        "block_height": -1,
        "block_index": -1,
        "hash": "74b76b48dfc9f4aac53fc1300881bcd6da17b9b6c0b065b234e04b27431dc769",
        "addresses": [
          "mjifgpTzeHEF3ieEQ7zBvPVsyMVnS2v7Kq"
        ],
        "total": 1000,
        "fees": 11050,
        "size": 209,
        "vsize": 209,
        "preference": "low",
        "relayed_by": "2.176.203.191",
        "received": "2023-05-26T16:11:18.242733591Z",
        "ver": 1,
        "double_spend": false,
        "vin_sz": 1,
        "vout_sz": 1,
        "confirmations": 0,
        "inputs": [
          {
            "prev_hash": "c33c66e953577643db913ab1e6831c2059c8bbf1c00f45ea40a333df52790e52",
            "output_index": 0,
            "script": "47304402205a4b739c0c2e228e1072d6a426c6bffb9149262b7dea0f962f050f6d52642f7402207a078f46695969bce8b7daf8842512940394c341eb036fcedbd02f1d38bc8e2f014104b744ba84a3feb2643322be6862ba5998fd96641fb6080111139c39433a4b598333168486ac7278553a220312a7d2df2e1832e218a2143454246bb0082cb6558e",
            "output_value": 12050,
            "sequence": 4294967295,
            "addresses": [
              "mjifgpTzeHEF3ieEQ7zBvPVsyMVnS2v7Kq"
            ],
            "script_type": "pay-to-pubkey-hash",
            "age": 2435571
          }
        ],
        "outputs": [
          {
            "value": 1000,
            "script": "6e937c7b94905288011887",
            "addresses": null,
            "script_type": "unknown"
          }
        ]
      }
    }
    """
