# Seed Phrase Generator

This repository contains a small command-line utility that builds mnemonic seed phrases
for a range of popular wallet vendors and technologies. The generator uses a configurable
word list and wallet presets to ensure the number of words matches the expectations for
that vendor.

> **Security notice:** The bundled word list is automatically generated for demonstration
> purposes. Replace `data/demo_wordlist.txt` with an audited list (for example the official
> BIP39 English list) before using the tool for real funds.

## Features

- Presets for well-known wallets such as Ledger, Trezor, MetaMask, Trust Wallet, and more.
- Support for custom word counts and custom word lists.
- Random phrase creation using Python's `secrets` module.
- Simple CLI to explore supported wallets.

## Installation

This project requires Python 3.9 or newer. Clone the repository and install any optional
virtual environment you prefer.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No external dependencies are required.

## Usage

List the supported wallet presets:

```bash
python seed_phrase_generator.py --list-wallets
```

Generate a seed phrase for a known wallet (defaults to its first supported length):

```bash
python seed_phrase_generator.py --wallet trezor
```

Override the word count when the wallet supports multiple lengths:

```bash
python seed_phrase_generator.py --wallet ledger --word-count 24
```

Provide your own word list:

```bash
python seed_phrase_generator.py --wallet metamask --wordlist path/to/english.txt
```

Generate a custom phrase without a preset:

```bash
python seed_phrase_generator.py --word-count 15 --wordlist data/demo_wordlist.txt
```

The generator prints the wallet/technology metadata and the randomly selected mnemonic
words.

## Customising the word list

The default word list in `data/demo_wordlist.txt` contains 2,048 pronounceable placeholder
words generated from syllable combinations. Replace this file with a newline-delimited list
of real mnemonic words (such as the BIP39 English list) for production scenarios.
