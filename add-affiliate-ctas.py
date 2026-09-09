#!/usr/bin/env python3
"""Deprecated: Wise affiliate CTAs were removed (brand-unsafe personal invite URL).

This script previously injected Wise invite CTAs into compare/city/salary-needed pages.
Do not reintroduce monetization affiliate links here. Kept as a no-op so old docs/scripts
that call it do not silently re-add CTAs.
"""
import sys

def main():
    print("add-affiliate-ctas.py: no-op — Wise affiliate CTAs have been removed from the repo.")
    print("Refusing to inject affiliate CTAs. Exit.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
