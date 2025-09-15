from tools.scraper.bydfi_scraper import parse_symbols_from_html


def test_parse_symbols_from_html():
    html = open("tests/fixtures/sample_markets.html").read()
    symbols = parse_symbols_from_html(html)
    assert "BTCUSDT" in symbols
    assert "ETHUSDT" in symbols
    assert "ABCUSDT" in symbols
    assert len(symbols) == 3
