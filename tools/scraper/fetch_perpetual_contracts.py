#!/usr/bin/env python3
"""Fetch perpetual contract symbols (USDT-margined) from BYDFI swap exchangeInfo."""
from pathlib import Path
import requests


def main():
    url = 'https://www.bydfi.com/swap/public/common/exchangeInfo'
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json().get('data', [])

    symbols = set()
    # contractType: likely 2 for perpetual (observed in exchangeInfo)
    for it in data:
        settle = str(it.get('settleCoin') or '').upper()
        contract_type = it.get('contractType')
        # include trades where settle coin is USDT and contractType indicates perpetual (2)
        if settle == 'USDT' and (contract_type == 2 or contract_type == '2'):
            base = it.get('baseSymbol') or it.get('symbol') or ''
            if base:
                # normalize
                b = str(base).upper().replace('-', '').replace('_', '')
                if not b.endswith('USDT'):
                    b = b + 'USDT'
                symbols.add(b)

    out = Path('out_symbols_live.csv')
    out.write_text('\n'.join(sorted(symbols)) + '\n')
    print('wrote', out.absolute(), 'count', len(symbols))


if __name__ == '__main__':
    main()
