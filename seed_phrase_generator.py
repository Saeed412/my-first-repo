"""Seed phrase generator for multiple wallet technologies."""
from __future__ import annotations

import argparse
import secrets
from pathlib import Path
from typing import Iterable, List

DATA_DIR = Path("data")
DEFAULT_WORDLIST = DATA_DIR / "demo_wordlist.txt"

WALLET_PROFILES = {
    "ledger": {
        "name": "Ledger",
        "technology": "BIP39",
        "word_counts": [24],
        "notes": "Hardware wallet with optional passphrase support.",
    },
    "trezor": {
        "name": "Trezor",
        "technology": "BIP39",
        "word_counts": [12, 24],
        "notes": "Supports 12 or 24-word seed phrases.",
    },
    "metamask": {
        "name": "MetaMask",
        "technology": "BIP39",
        "word_counts": [12],
        "notes": "Browser wallet that uses 12-word mnemonics.",
    },
    "trust": {
        "name": "Trust Wallet",
        "technology": "BIP39",
        "word_counts": [12],
        "notes": "Mobile wallet with 12-word recovery phrases.",
    },
    "coinbase": {
        "name": "Coinbase Wallet",
        "technology": "BIP39",
        "word_counts": [12],
        "notes": "Coinbase's self-custody wallet.",
    },
    "keystone": {
        "name": "Keystone",
        "technology": "BIP39 or SLIP39 (Shamir)",
        "word_counts": [12, 24],
        "notes": "Air-gapped hardware wallet; Shamir backups require specialized handling.",
    },
    "safe": {
        "name": "Safe (formerly Gnosis Safe)",
        "technology": "BIP39",
        "word_counts": [12],
        "notes": "Multi-signature smart contract wallet.",
    },
    "bitbox": {
        "name": "BitBox02",
        "technology": "BIP39",
        "word_counts": [12, 24],
        "notes": "Swiss-made hardware wallet.",
    },
    "edge": {
        "name": "Edge Wallet",
        "technology": "Edge Mnemonic",
        "word_counts": [12],
        "notes": "Uses Edge's own mnemonic scheme but length aligns with BIP39.",
    },
}


def ensure_wordlist(path: Path = DEFAULT_WORDLIST) -> List[str]:
    """Load the configured wordlist or raise a helpful error."""

    if not path.exists():
        raise FileNotFoundError(
            f"Wordlist '{path}' not found. Provide a custom list or run the"
            " bundled generator to create demo words."
        )
    words = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    if len(words) < 2048:
        raise ValueError(
            "Wordlist must contain at least 2048 entries to mirror BIP39 entropy."
        )
    return words


def select_wallet_profile(name: str | None):
    if name is None:
        return None
    key = name.lower()
    profile = WALLET_PROFILES.get(key)
    if profile is None:
        raise KeyError(
            f"Unknown wallet '{name}'. Use --list-wallets to inspect available options."
        )
    return profile


def generate_seed_phrase(words: List[str], word_count: int) -> List[str]:
    if word_count <= 0:
        raise ValueError("Word count must be positive.")
    return [words[secrets.randbelow(len(words))] for _ in range(word_count)]


def list_wallets() -> str:
    lines: List[str] = []
    for key, profile in sorted(WALLET_PROFILES.items()):
        counts = ", ".join(str(c) for c in profile["word_counts"])
        lines.append(
            f"{profile['name']} ({key})\n  Technology: {profile['technology']}\n"
            f"  Supported lengths: {counts}\n  Notes: {profile['notes']}"
        )
    return "\n\n".join(lines)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate wallet seed phrases across different technologies."
    )
    parser.add_argument(
        "--wallet",
        help="Wallet identifier (see --list-wallets).",
    )
    parser.add_argument(
        "--word-count",
        type=int,
        help="Override the number of words in the phrase if the wallet supports it.",
    )
    parser.add_argument(
        "--wordlist",
        type=Path,
        default=DEFAULT_WORDLIST,
        help="Path to a newline-delimited wordlist (defaults to the demo list).",
    )
    parser.add_argument(
        "--list-wallets",
        action="store_true",
        help="Display supported wallet presets and exit.",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list_wallets:
        print(list_wallets())
        return 0

    profile = select_wallet_profile(args.wallet)

    if profile is None and args.word_count is None:
        raise SystemExit(
            "Specify --wallet or --word-count to control the mnemonic length."
        )

    words = ensure_wordlist(args.wordlist)

    if profile is None:
        if args.word_count is None:
            raise SystemExit("A word count is required when no wallet preset is used.")
        word_count = args.word_count
        tech = "Custom"
        wallet_name = "Custom"
    else:
        supported = profile["word_counts"]
        if args.word_count is not None:
            if args.word_count not in supported:
                raise SystemExit(
                    f"{profile['name']} supports {supported}, but {args.word_count} was requested."
                )
            word_count = args.word_count
        else:
            word_count = supported[0]
        tech = profile["technology"]
        wallet_name = profile["name"]

    mnemonic_words = generate_seed_phrase(words, word_count)
    print(
        f"Wallet: {wallet_name}\nTechnology: {tech}\nWords: {word_count}\n"
        f"Seed phrase:\n{' '.join(mnemonic_words)}"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
