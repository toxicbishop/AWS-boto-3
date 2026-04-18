# AWS EC2 Manager

A lightweight Flask dashboard for managing Amazon EC2 instances through the AWS SDK for Python (`boto3`). List every instance in your region, and start, stop, or reboot them from a clean web UI — with optional local HTTPS.

## Features

- **Instance listing** — shows ID, Name tag, state, type, and public/private IP.
- **One-click actions** — start, stop, and reboot instances directly from the dashboard.
- **Flash notifications** — success, info, warning, and error feedback on every action.
- **Local HTTPS** — auto-enabled when `cert.pem` and `key.pem` exist; falls back to HTTP otherwise.
- **Makefile automation** — generate certs and run the app with a single command.

## Prerequisites

- Python 3.8+
- An AWS account with an IAM user that has EC2 permissions (e.g. `AmazonEC2FullAccess` for testing, scoped policies for production).
- AWS credentials configured locally via `aws configure`, environment variables, or `~/.aws/credentials`.

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure AWS credentials (one of):
aws configure
# or export AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_DEFAULT_REGION
```

## Running the app

```bash
# Plain HTTP (dev)
python app.py

# HTTPS with self-signed certs
make certs   # generates cert.pem + key.pem via scripts/generate_certs.py
make run     # runs the app (generates certs first if missing)

# Clean up generated certs
make clean
```

The app starts on `https://localhost:5000` when certs are present, otherwise `http://localhost:5000`.

## Configuration

The AWS region is set in `app.py:8` (`get_ec2_client`). Change `region_name` to target a different region, or refactor it to read from an environment variable.

## Supported operations

| Action    | Route                            | boto3 call          |
|-----------|----------------------------------|---------------------|
| List      | `GET /`                          | `describe_instances` |
| Start     | `GET /action/start/<id>`         | `start_instances`    |
| Stop      | `GET /action/stop/<id>`          | `stop_instances`     |
| Reboot    | `GET /action/reboot/<id>`        | `reboot_instances`   |

## Project structure

```
.
├── app.py                   # Flask app + EC2 routes
├── requirements.txt         # flask, boto3
├── Makefile                 # certs / run / clean targets
├── scripts/
│   └── generate_certs.py    # self-signed cert generator
└── templates/
    └── test.html            # dashboard UI
```

## Security notes

- `app.secret_key` in `app.py:5` is a placeholder — replace it with a value from `secrets.token_hex()` or an environment variable before deploying anywhere real.
- Never commit AWS credentials or `cert.pem` / `key.pem` to git; they're covered by `.gitignore`.
- The self-signed cert is for **local development only**. Use a real certificate (Let's Encrypt, ACM) in production.

## License

Unlicensed — internal / educational use.
