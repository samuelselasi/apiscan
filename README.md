# APIScan

APIScan is a Linux-first, safe-by-default API security scanner that performs practical checks against public APIs on the internet.

It is designed for developers and security learners who want quick feedback on common API security weaknesses without running noisy or destructive scans.

## What it checks (v0.1)

APIScan focuses on lightweight, non-invasive checks:

- TLS and HTTPS checks
- Security headers audit
- CORS configuration checks
- Rate limiting heuristics
- Basic information leak detection

Outputs:
- Terminal summary and tables
- JSON report
- HTML report

## Installation

```bash
git clone <your-repo-url>
cd apiscan
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Basic usage

Scan a public API:

```bash
apiscan https://api.github.com
```

Scan multiple paths:

```bash
apiscan https://api.github.com --paths / /rate_limit /users/octocat
```

Control speed and timeouts:

```bash
apiscan https://api.github.com --paths / /users/octocat --concurrency 15 --timeout 10
```

## Reports

Use an output directory to keep reports organized:

```bash
apiscan https://api.github.com --paths / /rate_limit --output-dir reports/
```

This will generate:
- reports/apiscan_report.json
- reports/apiscan_report.html

Custom filenames:

```bash
apiscan https://api.github.com --paths / --output-dir reports/ --json github.json --report-html github.html
```

## Endpoint discovery

APIScan can automatically discover endpoints from OpenAPI or Swagger specs.

```bash
apiscan https://petstore.swagger.io --discover --max-paths 25 --output-dir reports/
```

Combine discovery with manual paths:

```bash
apiscan https://api.example.com --discover --paths / /health --max-paths 30
```

## CLI options

| Option | Description |
|------|-------------|
| url | Base URL of the target API |
| --paths | One or more paths to scan |
| --discover | Attempt OpenAPI/Swagger discovery |
| --max-paths | Maximum number of paths to scan |
| --concurrency | Concurrent requests |
| --timeout | Request timeout in seconds |
| --output-dir | Directory to store outputs |
| --json | Write JSON report |
| --report-html | Write HTML report |

## Safety note

APIScan is designed to be safe and lightweight. It does not perform brute force attacks, exploit payloads, or destructive actions. Only scan systems you are authorized to test.

## Roadmap

- Smarter authentication checks
- OpenAPI deep analysis
- Severity scoring improvements
- PDF export
- CI and PyPI release
