#!/usr/bin/env python3
"""Fetch live symbols from BYDFI public APIs and write out_symbols_live.csv"""
import re
from pathlib import Path
import requests


def norm_symbol(s: str) -> str:
    if not s:
        return ''
    s = str(s).upper()
    # replace separators with underscore
    s = s.replace('-', '_')
    # ensure it ends with USDT
    if s.endswith('_USDT'):
        base = s[:-5]
    elif s.endswith('USDT'):
        base = s[:-4]
    else:
        # if contains USDT inside like BROCCOLIUSDT
        m = re.match(r'^(.*)USDT$', s)
        base = m.group(1) if m else s
    # strip non-alnum
    base = re.sub(r'[^A-Z0-9]', '', base)
    return base + 'USDT' if base else ''


def fetch_exchange_info():
    url = 'https://www.bydfi.com/swap/public/common/exchangeInfo'
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json().get('data', [])


def fetch_home_symbols():
    url = 'https://www.bydfi.com/api/public/home/symbols?upper=true'
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json().get('data', {})


def fetch_spot_list():
    url = 'https://www.bydfi.com/api/spot/product/list'
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json().get('data', [])


def main():
    symbols = set()

    try:
        for item in fetch_exchange_info():
            # prefer baseSymbol or symbol
            base = item.get('baseSymbol') or item.get('symbol') or ''
            s = norm_symbol(base)
            if s.endswith('USDT'):
                symbols.add(s)
    except Exception as e:
        print('exchangeInfo error', e)

    try:
        home = fetch_home_symbols()
        for key in ('spot_symbols', 'symbols', 'spotSymbols'):
            for item in home.get(key, []) if isinstance(home.get(key, []), list) else []:
                # various keys: code, name, baseCoin, quoteCoin
                base = item.get('baseCoin') or item.get('code') or item.get('name') or ''
                quote = item.get('quoteCoin') or item.get('unit') or ''
                if quote and str(quote).upper() == 'USDT':
                    s = norm_symbol(base)
                    if s.endswith('USDT'):
                        symbols.add(s)
    except Exception as e:
        print('home symbols error', e)

    try:
        for item in fetch_spot_list():
            quote = item.get('quoteCoin') or ''
            if quote and str(quote).upper() == 'USDT':
                base = item.get('baseCoin') or item.get('symbol') or item.get('alias') or ''
                s = norm_symbol(base)
                if s.endswith('USDT'):
                    symbols.add(s)
    except Exception as e:
        print('spot list error', e)

    out = Path('out_symbols_live.csv')
    out.write_text('\n'.join(sorted(symbols)) + '\n')
    print('wrote', out.absolute(), 'count', len(symbols))


if __name__ == '__main__':
    main()
