#!/usr/bin/env python3
"""
ZPHISHING APEX — Blockchain Verifier
Verify captured credentials on blockchain
"""

import hashlib
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

class BlockchainVerifier:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self._create_genesis_block()

    def _create_genesis_block(self):
        """Create genesis block"""
        genesis = self._create_block(
            index=0,
            previous_hash='0',
            data={'message': 'ZPHISHING APEX Genesis Block'},
            timestamp=time.time()
        )
        self.chain.append(genesis)

    def _create_block(self, index: int, previous_hash: str, data: Dict, timestamp: float) -> Dict:
        """Create new block"""
        block = {
            'index': index,
            'timestamp': timestamp,
            'data': data,
            'previous_hash': previous_hash,
            'nonce': 0
        }

        block['hash'] = self._mine_block(block)
        return block

    def _mine_block(self, block: Dict) -> str:
        """Mine block with proof of work"""
        target = '0' * self.difficulty

        while True:
            block_string = json.dumps(block, sort_keys=True)
            block_hash = hashlib.sha256(block_string.encode()).hexdigest()

            if block_hash[:self.difficulty] == target:
                return block_hash

            block['nonce'] += 1

    def hash_data(self, data: Dict) -> str:
        """Hash data for verification"""
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()

    def verify(self, data: Dict) -> Dict:
        """Verify data on blockchain"""
        data_hash = self.hash_data(data)

        # Add to blockchain
        previous_block = self.chain[-1]
        new_block = self._create_block(
            index=len(self.chain),
            previous_hash=previous_block['hash'],
            data={'hash': data_hash, 'verified': True},
            timestamp=time.time()
        )

        self.chain.append(new_block)

        return {
            'verified': True,
            'hash': data_hash,
            'block_index': new_block['index'],
            'block_hash': new_block['hash'],
            'timestamp': new_block['timestamp']
        }

    def verify_chain(self) -> bool:
        """Verify blockchain integrity"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Verify hash
            if current['previous_hash'] != previous['hash']:
                return False

            # Verify proof of work
            block_string = json.dumps({k: v for k, v in current.items() if k != 'hash'}, sort_keys=True)
            block_hash = hashlib.sha256(block_string.encode()).hexdigest()

            if block_hash != current['hash']:
                return False

        return True

    def get_chain(self) -> List[Dict]:
        """Get full blockchain"""
        return self.chain
