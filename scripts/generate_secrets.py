#!/usr/bin/env python3
"""Generate SECRET_KEY and JWT_SECRET_KEY and update a .env file safely.

Usage examples:
  # Generate and print secrets, update .env in-place (with backup)
  python3 scripts/generate_secrets.py --env .env --show

  # Generate and update without printing secrets
  python3 scripts/generate_secrets.py --env .env

This script:
 - creates a timestamped backup of the target .env (unless --no-backup)
 - replaces existing SECRET_KEY and JWT_SECRET_KEY lines, or appends them
 - prints minimal status output; use --show to print the generated values

Security notes:
 - Do NOT commit your .env to git. Keep secrets in a secrets manager in production.
 - This script is intended for local dev convenience.
"""

import argparse
import datetime
import os
import re
import secrets
import sys


def generate_secret(nbytes: int) -> str:
    # token_urlsafe provides a URL-safe Base64-ish string
    return secrets.token_urlsafe(nbytes)


def backup_file(path: str) -> str:
    ts = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    bak = f"{path}.bak.{ts}"
    with open(path, 'r', encoding='utf-8') as r, open(bak, 'w', encoding='utf-8') as w:
        w.write(r.read())
    return bak


def replace_or_append(env_path: str, key: str, value: str, data: str) -> str:
    pattern = re.compile(rf'(?m)^{re.escape(key)}=.*$')
    if pattern.search(data):
        return pattern.sub(f'{key}={value}', data)
    else:
        # ensure there is a trailing newline
        if not data.endswith('\n'):
            data += '\n'
        return data + f'{key}={value}\n'


def main():
    parser = argparse.ArgumentParser(description='Generate and inject SECRET_KEY and JWT_SECRET_KEY into a .env file')
    parser.add_argument('--env', default='.env', help='Path to .env file to update')
    parser.add_argument('--nbytes', type=int, default=48, help='Number of random bytes to use for token_urlsafe')
    parser.add_argument('--show', action='store_true', help='Print generated secrets to stdout (handle carefully)')
    parser.add_argument('--no-backup', action='store_true', help='Do not create a backup of the .env file')
    args = parser.parse_args()

    env_path = args.env
    if not os.path.exists(env_path):
        print(f'Error: env file not found at {env_path}', file=sys.stderr)
        sys.exit(2)

    secret = generate_secret(args.nbytes)
    jwt_secret = generate_secret(args.nbytes)

    # Read current env
    with open(env_path, 'r', encoding='utf-8') as f:
        data = f.read()

    # Backup
    if not args.no_backup:
        bak = backup_file(env_path)
        print(f'Backup created: {bak}')

    # Replace or append
    data = replace_or_append(env_path, 'SECRET_KEY', secret, data)
    data = replace_or_append(env_path, 'JWT_SECRET_KEY', jwt_secret, data)

    # Write atomically
    tmp = env_path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(data)
    os.replace(tmp, env_path)

    print(f'Updated {env_path} with new SECRET_KEY and JWT_SECRET_KEY')
    if args.show:
        print('\nCopy/store these securely:')
        print('SECRET_KEY=' + secret)
        print('JWT_SECRET_KEY=' + jwt_secret)
    else:
        print('Generated secrets were NOT printed. Use --show to display them (careful!).')


if __name__ == '__main__':
    main()
