# my public Address: mvw1uJQNoPAwwcEDZmdfax3F1GveG28Ewo

from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x

from mechanisms.conf import *
from utils import *

my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)


def no_return_scriptPubKey():
    return [OP_RETURN]


def public_spendable_scriptPubKey():
    return [OP_TRUE]


def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]


def P2PKH_scriptSig(txin, first_txout, second_txout, txin_scriptPubKey):
    txouts = [first_txout, second_txout]
    signature = create_OP_CHECKSIG_signature(txin, txouts, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key]


def send_from_P2PKH_transaction(first_amount_to_send, second_amount_to_send, txid_to_spend, utxo_index,
                                first_txout_scriptPubKey, second_txout_scriptPubKey):
    first_txout = create_txout(first_amount_to_send, first_txout_scriptPubKey)
    second_txout = create_txout(second_amount_to_send, second_txout_scriptPubKey)
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, first_txout, second_txout, txin_scriptPubKey)

    txouts = [first_txout, second_txout]
    new_tx = create_signed_transaction(txin, txouts, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    first_amount_to_send = 0.0000155
    second_amount_to_send = 0.00008
    txid_to_spend = '751f316b52821848b1a615969bffdb078cf9552286d6c4593142087f7eeb412c'  # TxHash of UTXO
    utxo_index = 1  # UTXO index among transaction outputs
    ######################################################################

    print('Base58 address: ', my_address)  # Prints your address in base58
    print('Public key: ', my_public_key.hex())  # Print your public key in hex
    print('Private key: ', my_private_key.hex())  # Print your private key in hex
    first_txout_scriptPubKey = no_return_scriptPubKey()
    second_txout_scriptPubKey = public_spendable_scriptPubKey()
    response = send_from_P2PKH_transaction(first_amount_to_send, second_amount_to_send, txid_to_spend, utxo_index,
                                           first_txout_scriptPubKey, second_txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)  # Report the hash of transaction which is printed in this section result

    """
    Base58 address:  mvw1uJQNoPAwwcEDZmdfax3F1GveG28Ewo
    Public key:  0488066b8774e54ad2d57f964ffc03da9c9b171e36faba29c1cd0789ff98f0a64648a0ab6d4cc9b316e5ba3774ccc12256d8e417fbdd2b9713676b549a5027e350
    Private key:  4a03b64a24c0eab2b212652f2b56ca4f5e2216f349bef3b6535ec591145b18a1
    201 Created
    {
      "tx": {
        "block_height": -1,
        "block_index": -1,
        "hash": "53d7af7e0f7318b01f8dc5044a3318e803f7aaf2c24f18f43389e6854527cfde",
        "addresses": [
          "mvw1uJQNoPAwwcEDZmdfax3F1GveG28Ewo"
        ],
        "total": 3310000,
        "fees": 299222,
        "size": 209,
        "vsize": 209,
        "preference": "high",
        "relayed_by": "2.176.203.191",
        "received": "2023-05-26T06:30:42.997112574Z",
        "ver": 1,
        "double_spend": false,
        "vin_sz": 1,
        "vout_sz": 2,
        "confirmations": 0,
        "inputs": [
          {
            "prev_hash": "87087bf2d321d9dfd592264e1e2227167690a946f1b4d310d0fb0429453a6f76",
            "output_index": 0,
            "script": "47304402201c10890d7d2c13cff9f17d6852ad4a613b9712d83fcdaa0d09f60e66435d91f50220579ce0e0bb1d420dd81f1a7ed51a6eb2d9b6d0a6f16653dcaed45f855520f8f601410488066b8774e54ad2d57f964ffc03da9c9b171e36faba29c1cd0789ff98f0a64648a0ab6d4cc9b316e5ba3774ccc12256d8e417fbdd2b9713676b549a5027e350",
            "output_value": 3609222,
            "sequence": 4294967295,
            "addresses": [
              "mvw1uJQNoPAwwcEDZmdfax3F1GveG28Ewo"
            ],
            "script_type": "pay-to-pubkey-hash",
            "age": 2435407
          }
        ],
        "outputs": [
          {
            "value": 10000,
            "script": "6a",
            "addresses": null,
            "script_type": "null-data"
          },
          {
            "value": 3300000,
            "script": "ac",
            "addresses": null,
            "script_type": "unknown"
          }
        ]
      }
    }
    """
