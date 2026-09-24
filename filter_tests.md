# Firewall Test Evidence

Run these from machines on the relevant subnet in your lab, after applying
`firewall_rules.sh`. Fill in the actual command output you get — the
values below are placeholders to show the expected format.

## Test 1 — Permitted connection (staff network → service)

```
$ nc -zv <server_ip> 443
```
- **Expected outcome:** Connection succeeds (open/connected)
- **Actual result:** _(paste real output here)_

## Test 2 — Blocked connection (guest network → service)

```
$ nc -zv <server_ip> 443
```
- **Expected outcome:** Connection refused / times out (dropped by firewall)
- **Actual result:** _(paste real output here)_

## Test 3 — Blocked connection (unauthorised external source → service)

```
$ nc -zv <server_ip> 443
```
- **Expected outcome:** Connection refused / times out (dropped by firewall)
- **Actual result:** _(paste real output here)_

## Summary

| Test | Source | Expected | Actual | Pass/Fail |
|------|--------|----------|--------|-----------|
| 1 | Staff subnet | Allowed | | |
| 2 | Guest subnet | Blocked | | |
| 3 | External/unauthorised | Blocked | | |
