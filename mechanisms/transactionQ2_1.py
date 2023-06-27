from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x

from mechanisms.conf import *
from utils import *


def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, [txout], txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]


def MultiSig_output_script():
    return [OP_2, first_person_public_key, second_person_public_key, third_person_public_key, OP_3, OP_CHECKMULTISIG]


def send_multisig_P2MS_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)
    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send = 0.00006
    txid_to_spend = '5411056e23291f5d1994c6fd3c4786907845a84210055ceaaa557f914e8b23ce'
    utxo_index = 1

    txout_scriptPubKey = MultiSig_output_script()
    response = send_multisig_P2MS_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)

"""
{
  "tx": {
    "block_height": -1,
    "block_index": -1,
    "hash": "ed778d3dae7a992a94f754cd013fa3e36ffd91062624c0d8167a506e89ba773a",
    "addresses": [
      "mjifgpTzeHEF3ieEQ7zBvPVsyMVnS2v7Kq",
      "zFRA6p2sxKTmb13F6gAadYyMCyGqqdz22o"
    ],
    "total": 6000,
    "fees": 1366,
    "size": 399,
    "vsize": 399,
    "preference": "low",
    "relayed_by": "2.176.203.191",
    "received": "2023-05-26T09:30:42.717789528Z",
    "ver": 1,
    "double_spend": false,
    "vin_sz": 1,
    "vout_sz": 1,
    "confirmations": 0,
    "inputs": [
      {
        "prev_hash": "5411056e23291f5d1994c6fd3c4786907845a84210055ceaaa557f914e8b23ce",
        "output_index": 1,
        "script": "4730440220501f4d5452e3cf7363f00222adac796a526e5d37d504ca766d950b7e082799cc022070b2ad6aa0c6e7fad8e9156a72aba96c8b43b1451db8489589d63dfa85f3ca5b014104b744ba84a3feb2643322be6862ba5998fd96641fb6080111139c39433a4b598333168486ac7278553a220312a7d2df2e1832e218a2143454246bb0082cb6558e",
        "output_value": 7366,
        "sequence": 4294967295,
        "addresses": [
          "mjifgpTzeHEF3ieEQ7zBvPVsyMVnS2v7Kq"
        ],
        "script_type": "pay-to-pubkey-hash",
        "age": 2435515
      }
    ],
    "outputs": [
      {
        "value": 6000,
        "script": "52410491b20bdadeddad98612187bd9b8875ef6b369d70324cdab1b5ed09e34f2e36de1fc2c73c90b9260398064d5d23d0045cd3bc0782fc36f2f243203e8b7671c04941047a63cb2312f18640bae77279fcce86b42ceb3eb72e2c38a92cf76612adc59c2e7441b5796a0933a76156ac5aab766a2c0a361c020a8444c41cecd80f073187aa4104e564dbf9318ce02d7570517a5ab8287492d483e5857a8a7d66997526a68040facf4c49afa694d3ca890368f145f0f8553eebfd2a30150f7f9ee6535850317ee453ae",
        "addresses": [
          "zFRA6p2sxKTmb13F6gAadYyMCyGqqdz22o"
        ],
        "script_type": "pay-to-multi-pubkey-hash"
      }
    ]
  }
}

Process finished with exit code 0
"""