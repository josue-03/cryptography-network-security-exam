# Cryptography & Network Security — Integrated Situation

ETTCS801 exam project: risk assessment, an encryption/integrity toolkit,
firewall traffic filtering, and a LaTeX technical report, for the
polytechnic student-records scenario.

## Project structure

```
cryptography-network-security-exam/
├── README.md
├── risk_assessment.md       # Part 1: assets, vulnerabilities, risk ranking, controls
├── firewall_rules.sh        # Part 3: iptables rules (guest/staff/other)
├── filter_tests.md          # Part 3d: test commands + results
├── report/
│   └── report.tex           # Part 5: overall LaTeX technical report
├── src/
│   └── crypto_toolkit.py    # Part 2: encrypt / decrypt / hash / verify
├── docs/                    # screenshots, test evidence, compiled report.pdf
└── .gitignore                # excludes secret.key and sample data
```

## Part 2 — Encryption & integrity toolkit

### Requirements
- Python 3.8+
- `pip install cryptography`

### Usage

```bash
cd src

# 1. Generate an encryption key (kept OUTSIDE the repo — do not commit it)
python3 crypto_toolkit.py genkey

# 2. Encrypt the sample record
python3 crypto_toolkit.py encrypt sample_record.txt sample_record.enc

# 3. Compute and save its SHA-256 hash
python3 crypto_toolkit.py hash sample_record.enc

# 4. Verify integrity later (detects tampering)
python3 crypto_toolkit.py verify sample_record.enc sample_record.enc.sha256

# 5. Decrypt and confirm it matches the original
python3 crypto_toolkit.py decrypt sample_record.enc sample_record.dec
diff sample_record.txt sample_record.dec   # no output = identical
```

The programme handles missing files and invalid input without crashing
(see `try/except` blocks in `crypto_toolkit.py`).

**Security note:** `secret.key` and any real/sample student data must
never be pushed to GitHub — both are listed in `.gitignore`. Only use
dummy sample data supplied for the exam.

## Part 3 — Network traffic filtering

Edit the interface/subnet/port variables at the top of `firewall_rules.sh`
to match your lab environment, then, on the authorised lab machine:

```bash
sudo bash firewall_rules.sh
```

This will:
- Block the guest subnet from reaching the records-server port
- Allow the staff subnet to reach that port
- Drop all other inbound traffic to that port

Test results (1 permitted + 2 blocked connections) are recorded in
`filter_tests.md`.

## Part 5 — LaTeX report

Compile with:

```bash
cd report
pdflatex report.tex
```

This produces `report.pdf`, which should be committed alongside
`report.tex`.

## Reproducing the whole project

1. Clone the repo
2. Follow "Part 2" above to run and test the toolkit
3. Follow "Part 3" above to apply and test firewall rules in the lab
4. Compile the report as in "Part 5"
5. All commands and outputs used for grading are recorded in
   `filter_tests.md` and `docs/`
