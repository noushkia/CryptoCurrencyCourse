from mechanisms.conf import *
from utils import *

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

def prime_scriptSig():
    return [prime_1, prime_2]


def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]


def send_prime_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = prime_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = prime_scriptSig()

    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send = 0.000005
    txid_to_spend = '74b76b48dfc9f4aac53fc1300881bcd6da17b9b6c0b065b234e04b27431dc769'
    utxo_index = 0

    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)

    response = send_prime_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)

    """
    {
      "tx": {
        "block_height": -1,
        "block_index": -1,
        "hash": "bedc25abd69f87ad1ea15acb2dea44de29727ea227d0f6a338c52ceda01fdde5",
        "addresses": [
          "mjifgpTzeHEF3ieEQ7zBvPVsyMVnS2v7Kq"
        ],
        "total": 500,
        "fees": 500,
        "size": 87,
        "vsize": 87,
        "preference": "low",
        "relayed_by": "2.176.203.191",
        "received": "2023-05-26T16:12:24.96908925Z",
        "ver": 1,
        "double_spend": false,
        "vin_sz": 1,
        "vout_sz": 1,
        "confirmations": 0,
        "inputs": [
          {
            "prev_hash": "74b76b48dfc9f4aac53fc1300881bcd6da17b9b6c0b065b234e04b27431dc769",
            "output_index": 0,
            "script": "5d5b",
            "output_value": 1000,
            "sequence": 4294967295,
            "script_type": "unknown",
            "age": 0
          }
        ],
        "outputs": [
          {
            "value": 500,
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