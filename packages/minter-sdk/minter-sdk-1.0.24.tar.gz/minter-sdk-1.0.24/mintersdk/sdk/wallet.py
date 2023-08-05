"""
@author: Roman Matusevich
"""
import binascii
import hashlib

import hmac
from mnemonic.mnemonic import Mnemonic
from mintersdk.two1.bitcoin.crypto import HDKey, HDPrivateKey, bitcoin_curve
from mintersdk import MinterHelper, PREFIX_PUBKEY, PREFIX_ADDR


class MinterWallet(object):
    """
    Minter wallet class
    """

    # Amount of entropy bits
    BIP44_ENTROPY_BITS = 128

    # Address path for creating wallet from the seed
    BIP44_SEED_ADDRESS_PATH = "m/44'/60'/0'/0/0"

    # Master seed
    MASTER_SEED = b'Bitcoin seed'

    @classmethod
    def create(cls, mnemonic=None):
        """
        Create Minter wallet
        Args:
            mnemonic (str): Mnemonic phrase
        Returns:
            dict
        """

        # Create mnemonic phrase if None
        if not mnemonic:
            _mnemonic = Mnemonic(language='english')
            mnemonic = _mnemonic.generate(cls.BIP44_ENTROPY_BITS)

        if len(mnemonic.split(' ')) != 12:
            raise Exception('Mnemonic phrase should have 12 words.')

        # Mnemonic to seed (bytes)
        seed = Mnemonic.to_seed(mnemonic, '')

        # Generate master key from master seed
        _I = hmac.new(cls.MASTER_SEED, seed, hashlib.sha512).hexdigest()

        master_key = HDPrivateKey(
            key=int.from_bytes(binascii.unhexlify(_I[:64]), 'big'),
            chain_code=binascii.unhexlify(_I[64:]),
            index=0,
            depth=0
        )

        # Get child keys from master key by path
        keys = HDKey.from_path(master_key, cls.BIP44_SEED_ADDRESS_PATH)

        # Get private key
        private_key = binascii.hexlify(bytes(keys[-1]._key))

        # Get public key
        public_key = cls.get_public_from_private(private_key)

        # Get address
        address = cls.get_address_from_public_key(public_key)

        return {
            'address': address,
            'private_key': private_key.decode(),
            'mnemonic': mnemonic,
            'seed': binascii.hexlify(seed).decode()
        }

    @classmethod
    def get_public_from_private(cls, private_key):
        """
        Get public key from private key
        Args:
            private_key (bytes): hex bytes of private key
        Returns:
            str
        """

        public_key = bitcoin_curve.public_key(
            int.from_bytes(binascii.unhexlify(private_key), 'big')
        )

        return MinterHelper.prefix_add(
            binascii.hexlify(bytes(public_key)).decode()[2:], PREFIX_PUBKEY
        )

    @classmethod
    def get_address_from_public_key(cls, public_key):
        """
        Args:
            public_key (str)
        Returns:
            str
        """
        # Create keccak hash
        _keccak = MinterHelper.keccak_hash(
            binascii.unhexlify(MinterHelper.prefix_remove(public_key))
        )

        return MinterHelper.prefix_add(_keccak[-40:], PREFIX_ADDR)
