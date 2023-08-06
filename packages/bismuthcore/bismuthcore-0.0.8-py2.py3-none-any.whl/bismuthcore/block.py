
"""
Bismuth core Block Class
"""

from bismuthcore.transaction import Transaction

__version__ = "0.0.1"


class Block:
    """A generic Bismuth Block with its transactions"""

    # Inner storage is compact, binary form
    __slots__ = ('transactions', )

    def __init__(self, transactions: list):
        """Default constructor with list of binary, non verbose,
        Transactions instances, mining transaction at the end."""
        self.transactions = transactions

    def to_listofdicts(self, legacy: bool=False, decode_pubkey: bool=False) -> list:
        """
        The block as a list of Transactions, converted to the required dict format.
        :param legacy:
        :param decode_pubkey:
        :return:
        """
        # Could be better as tuple, but may constraint higher level usage (may need to add something to the list) - to be checked later on
        return [transaction.to_dict(legacy=legacy, decode_pubkey=decode_pubkey) for transaction in self.transactions]

    def to_listoftuples(self) -> list:
        """
        The block as a list of Transactions, converted to legacy tuples.
        :return:
        """
        return [transaction.to_tuple() for transaction in self.transactions]
