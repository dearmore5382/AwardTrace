from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "app" / "page.tsx").read_text(encoding="utf-8")


def test_real_genlayer_sdk_and_injected_wallet():
    assert 'from "genlayer-js"' in PAGE
    assert "eth_requestAccounts" in PAGE
    assert 'client.connect("studionet")' in PAGE
    assert "writeContract" in PAGE


def test_finality_then_authoritative_readback():
    finality = PAGE.index("waitForTransactionReceipt")
    readback = PAGE.index("await readBack", finality)
    success = PAGE.index("authoritative state confirmed", readback)
    assert finality < readback < success


def test_no_embedded_private_key_or_fake_address():
    assert "PRIVATE_KEY" not in PAGE
    assert "0x382cE7BCB7e644e431b89088DbDa906712F3d618" not in PAGE
    assert "PENDING_PRIMARY_WALLET_DEPLOYMENT" not in PAGE
