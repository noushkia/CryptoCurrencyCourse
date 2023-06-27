# my Address: mnmxhdY6G4EeNHmHcKvuGCSkRCQAkfDM1i

from mechanisms.conf import *
from utils import *

my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)


def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]


def get_txin_scriptPubKey():
    return [OP_TRUE]  # OP_CHECKSIG works as well


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, [txout], txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]


def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = get_txin_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.032
    txid_to_spend = '53d7af7e0f7318b01f8dc5044a3318e803f7aaf2c24f18f43389e6854527cfde'  # TxHash of UTXO
    utxo_index = 1  # UTXO index among transaction outputs
    ######################################################################

    print('Base58 address: ', my_address)  # Prints your address in base58
    print('Public key: ', my_public_key.hex())  # Print your public key in hex
    print('Private key: ', my_private_key.hex())  # Print your private key in hex

    txout_scriptPubKey = P2PKH_scriptPubKey(my_address)

    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)  # Report the hash of transaction which is printed in this section result

"""
Base58 address:  mjifgpTzeHEF3ieEQ7zBvPVsyMVnS2v7Kq
Public key:  04b744ba84a3feb2643322be6862ba5998fd96641fb6080111139c39433a4b598333168486ac7278553a220312a7d2df2e1832e218a2143454246bb0082cb6558e
Private key:  ad89fc0acd6a77a4ed77f97a3b4c8ecb72057d7cada8d31ab67cfdb0f671a4a4
201 Created
{
  "tx": {
    "block_height": -1,
    "block_index": -1,
    "hash": "62d01c7e1d60304d9886525ccc516382b14b70bb896b12767f13516a8ed589cb",
    "addresses": [
      "n2GKxgUJkQSjDxsxytKK196iYbXU3FSqFe"
    ],
    "total": 6999,
    "fees": 1001,
    "size": 223,
    "vsize": 223,
    "preference": "low",
    "relayed_by": "2.176.203.191",
    "received": "2023-05-26T08:48:16.114201292Z",
    "ver": 1,
    "double_spend": false,
    "vin_sz": 1,
    "vout_sz": 1,
    "confirmations": 0,
    "inputs": [
      {
        "prev_hash": "0f4bf19773dc261bf095ddecb10bacb6a81d7a8461d0ce8a19b2cc006bd138ca",
        "output_index": 1,
        "script": "47304402202fdfbcc27de2498cdc15656d4108f691e1ab113f653c3924267d70d7fe018d4902206176510860f0aa5cbe32aa57427006dd5b7c8035bbda3213ccfd9f9b28f5e4de014104b744ba84a3feb2643322be6862ba5998fd96641fb6080111139c39433a4b598333168486ac7278553a220312a7d2df2e1832e218a2143454246bb0082cb6558e",
        "output_value": 8000,
        "sequence": 4294967295,
        "script_type": "unknown",
        "age": 2435514
      }
    ],
    "outputs": [
      {
        "value": 6999,
        "script": "76a914e3967ce647ca88e2963a06358b5bf8955be70f9588ac",
        "addresses": [
          "n2GKxgUJkQSjDxsxytKK196iYbXU3FSqFe"
        ],
        "script_type": "pay-to-pubkey-hash"
      }
    ]
  }
}

Process finished with exit code 0
"""

"""
{
  "tx": {
    "block_height": -1,
    "block_index": -1,
    "hash": "f3f1395b51da572f1b6b5594e2c4206c67b98fa2ccb7879f8d775ec86b131eed",
    "addresses": [
      "n2GKxgUJkQSjDxsxytKK196iYbXU3FSqFe"
    ],
    "total": 3200000,
    "fees": 100000,
    "size": 224,
    "vsize": 224,
    "preference": "high",
    "relayed_by": "2.176.203.191",
    "received": "2023-05-26T09:01:11.533596959Z",
    "ver": 1,
    "double_spend": false,
    "vin_sz": 1,
    "vout_sz": 1,
    "confirmations": 0,
    "inputs": [
      {
        "prev_hash": "53d7af7e0f7318b01f8dc5044a3318e803f7aaf2c24f18f43389e6854527cfde",
        "output_index": 1,
        "script": "48304502210091523b745a616d246c9ea8839881bf0ad5e568eb063c7f917a447b06dabdf2d5022008a524ff1ab38c9fae68eea62f070494eee5e1e4bc43112f3acea4941db03877014104b744ba84a3feb2643322be6862ba5998fd96641fb6080111139c39433a4b598333168486ac7278553a220312a7d2df2e1832e218a2143454246bb0082cb6558e",
        "output_value": 3300000,
        "sequence": 4294967295,
        "script_type": "unknown",
        "age": 2435500
      }
    ],
    "outputs": [
      {
        "value": 3200000,
        "script": "76a914e3967ce647ca88e2963a06358b5bf8955be70f9588ac",
        "addresses": [
          "n2GKxgUJkQSjDxsxytKK196iYbXU3FSqFe"
        ],
        "script_type": "pay-to-pubkey-hash"
      }
    ]
  }
}

Process finished with exit code 0
"""
