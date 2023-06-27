# 810198438 -> 8438+1

import struct
import time

import bitcoin.wallet
from bitcoin.core import b2lx, Hash

from utils import *


def get_P2PKH_script(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]


def get_my_public_key():
    bitcoin.SelectParams('mainnet')
    WIF_private_key = '5JUUqpXwREFX5emdDCRS5dt7R6m1KxrvaUWjtUFzgo1VEPVUPLr'
    private_key = bitcoin.wallet.CBitcoinSecret(WIF_private_key)
    public_key = private_key.pub
    print('My address: ', bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(public_key))
    return public_key


def get_threshold(bits):
    exponent = bits[2:4]
    exponent2 = 8 * (int(exponent, 16) - 3)
    coefficient = bits[4:]

    _threshold = format(int(coefficient, 16) * (2 ** exponent2), 'x')
    threshold_byte = bytes.fromhex(str(_threshold).zfill(64))
    print('Threshold: ', str(_threshold).zfill(64))

    return threshold_byte


def create_coinbase_transaction(base_amount_to_send, coinbase_txid_to_spend, coinbase_utxo_index,
                                output_script, coinbase_script_sig):
    txin = create_txin(coinbase_txid_to_spend, coinbase_utxo_index)
    txout = create_txout(base_amount_to_send, output_script)
    tx = CMutableTransaction([txin], [txout])
    txin.scriptSig = coinbase_script_sig
    return tx


def get_merkle_root(_coinbase_tx):
    return b2lx(_coinbase_tx.GetTxid()), b2x(_coinbase_tx.serialize())


def get_partial_header(version, last_block_hash, merkle_root, bits):
    time_now = int(time.time())
    return struct.pack("<L", version) + bytes.fromhex(last_block_hash)[::-1] + bytes.fromhex(merkle_root)[
                                                                               ::-1] + struct.pack('<LL', time_now,
                                                                                                   int(bits, 16))


def mine_block(partial_header, target):
    nonce = 0
    while nonce <= 0xFFFFFFFF:
        header = partial_header + struct.pack('<L', nonce)
        block_hash = Hash(header)
        if block_hash[::-1] < target:
            print('Nonce found : ', nonce)
            return header, block_hash
        nonce += 1
    raise BaseException('Cannot find a suitable nonce to mine a block')


if __name__ == '__main__':
    print("Block number: ", 8438)
    last_block_hash = '000000009505ec73031ca38a87a4cc884075f1f75096845e24b1b74f5d133e20'
    print("Hash: ", last_block_hash)
    block_version = 2
    bits = '0x1f010000'  # for first four bits to be zero
    block_reward = 50  # block reward during the block time
    coinbase_txid_to_spend = '0' * 64
    coinbase_utxo_index = int('0xFFFFFFFF', 16)

    coinbase_hex_data = '810198438KianoushArshi'.encode('utf-8').hex()
    print('Coinbase hexadecimal data: ', coinbase_hex_data)

    output_script = get_P2PKH_script(get_my_public_key())
    coinbase_script_sig = CScript([int(coinbase_hex_data, 16).to_bytes(len(coinbase_hex_data) // 2, 'big')])
    coinbase_tx = create_coinbase_transaction(block_reward, coinbase_txid_to_spend, coinbase_utxo_index,
                                              output_script, coinbase_script_sig)
    merkle_root, block_body = get_merkle_root(coinbase_tx)
    threshold = get_threshold(bits)
    partial_header = get_partial_header(block_version, last_block_hash, merkle_root, bits)

    header, block_hash = mine_block(partial_header, threshold)

    print('Block hash: ', b2lx(block_hash))
    print('merkle_root: ', merkle_root)
    print('Block header: ', b2x(header))
    print('Block body: ', block_body)
