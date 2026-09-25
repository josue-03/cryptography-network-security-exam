# Firewall Test Evidence

## Test 1 — Permitted connection (staff network → service)

$ nc -vz -s 192.168.10.5 127.0.0.1 8080
Connection to 127.0.0.1 8080 port [tcp/http-alt] succeeded!

- Expected outcome: Connection succeeds
- Actual result: Succeeded (as expected)

## Test 2 — Blocked connection (guest network → service)

$ nc -vz -s 192.168.20.5 127.0.0.1 8080
nc: connect to 127.0.0.1 port 8080 (tcp) failed: Connection timed out

- Expected outcome: Blocked
- Actual result: Timed out / blocked (as expected)

## Test 3 — Blocked connection (unauthorised external source → service)

$ nc -vz -s 172.16.0.5 127.0.0.1 8080
nc: connect to 127.0.0.1 port 8080 (tcp) failed: Connection timed out

- Expected outcome: Blocked
- Actual result: Timed out / blocked (as expected)

## Summary

| Test | Source | Expected | Actual | Pass/Fail |
|------|--------|----------|--------|-----------|
| 1 | Staff subnet (192.168.10.5) | Allowed | Succeeded | Pass |
| 2 | Guest subnet (192.168.20.5) | Blocked | Timed out | Pass |
| 3 | External (172.16.0.5) | Blocked | Timed out | Pass |
