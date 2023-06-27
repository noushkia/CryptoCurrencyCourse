from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x

from mechanisms.conf import *
from utils import *
from transactionQ2_1 import MultiSig_output_script, first_person_private_key, second_person_private_key


def P2PKH_output_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]


def P2MS_scriptSig(txin, txout, txin_scriptPubKey):
    first_person_signature = create_OP_CHECKSIG_signature(txin, [txout], txin_scriptPubKey, first_person_private_key)
    second_person_signature = create_OP_CHECKSIG_signature(txin, [txout], txin_scriptPubKey, second_person_private_key)

    return [OP_0, first_person_signature, second_person_signature]


def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = MultiSig_output_script()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2MS_scriptSig(txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send = 0.00004
    txid_to_spend = 'ed778d3dae7a992a94f754cd013fa3e36ffd91062624c0d8167a506e89ba773a'
    utxo_index = 0

    txout_scriptPubKey = P2PKH_output_scriptPubKey(my_public_key)

    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)

"""
{
  "tx": {
    "block_height": -1,
    "block_index": -1,
    "hash": "71a184d310728808ad71b5587b889b07d575a28a4512c9f5fc7d7d4c86a82309",
    "addresses": [
      "mjifgpTzeHEF3ieEQ7zBvPVsyMVnS2v7Kq",
      "zFRA6p2sxKTmb13F6gAadYyMCyGqqdz22o"
    ],
    "total": 4000,
    "fees": 2000,
    "size": 231,
    "vsize": 231,
    "preference": "low",
    "relayed_by": "2.176.203.191",
    "received": "2023-05-26T09:39:02.967303221Z",
    "ver": 1,
    "double_spend": false,
    "vin_sz": 1,
    "vout_sz": 1,
    "confirmations": 0,
    "inputs": [
      {
        "prev_hash": "ed778d3dae7a992a94f754cd013fa3e36ffd91062624c0d8167a506e89ba773a",
        "output_index": 0,
        "script": "0047304402204231af12a0faf08824d6c3cf8d54d72bdd281b6ebcc3a3e7a8669e7bc2c2c2a1022049c316e597c07072b09186abb87885b34725aa4a08dccaba2a22792b872a8f7301483045022100c6e45d61a67b48df491a16ccea8806864fc2ae2b85ab85f395a40711bf58d66f0220289307bef292ce5fb549b6ffd5aa2d6c3340eaa1c79b544fa4fe37c5613ee57001",
        "output_value": 6000,
        "sequence": 4294967295,
        "addresses": [
          "zFRA6p2sxKTmb13F6gAadYyMCyGqqdz22o"
        ],
        "script_type": "pay-to-multi-pubkey-hash",
        "age": 0
      }
    ],
    "outputs": [
      {
        "value": 4000,
        "script": "76a9142e17a1a5cbdd07f543fa4ea2724893887a7f3d6c88ac",
        "addresses": [
          "mjifgpTzeHEF3ieEQ7zBvPVsyMVnS2v7Kq"
        ],
        "script_type": "pay-to-pubkey-hash"
      }
    ]
  }
}
"""
