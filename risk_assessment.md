# Risk Assessment — Polytechnic Student Records System

## a. Assets, Vulnerabilities, and Consequences

| # | Asset | Vulnerability | Possible Consequence |
|---|-------|----------------|------------------------|
| 1 | Central student records server | Guest network can reach the records server | Unauthorised access, theft or tampering of student data |
| 2 | Staff login credentials | Weak/reused passwords across staff accounts | Account compromise leading to unauthorised data access or modification |
| 3 | Inter-campus file transfer channel | Files transferred between campuses are unencrypted | Interception (eavesdropping) of student records in transit |

*(Software running on the server is also outdated, which compounds risks 1 and 3 — missing patches make exploitation of both easier.)*

## b. Risk Ranking (Likelihood × Impact)

| Rank | Risk | Likelihood | Impact | Reasoning |
|------|------|-----------|--------|-----------|
| 1 | Guest network access to records server | High | High | No segmentation currently exists, and repeated connection attempts from an unfamiliar external address show active probing — an easy, already-being-attempted path to the most sensitive asset. |
| 2 | Weak staff passwords | Medium–High | High | Weak passwords are common and easy to brute-force or guess, and a compromised staff account gives legitimate-looking access to records. |
| 3 | Unencrypted inter-campus transfer | Medium | Medium | Requires the attacker to be positioned on the network path between campuses, which is a narrower opportunity than the other two, but exposure of data in transit is still a real confidentiality breach. |

## c. Recommended Controls

| Risk | Recommended Control |
|------|----------------------|
| Guest network access to records server | Network segmentation (VLANs) + firewall rules that explicitly deny guest → records-server traffic, permitting only the authorised staff subnet |
| Weak staff passwords | Enforce a strong password policy plus multi-factor authentication (MFA) for all staff accounts with access to the records server |
| Unencrypted inter-campus transfer | Encrypt transfers in transit (e.g. SFTP/SCP or a TLS-secured channel) instead of plaintext protocols like FTP |

*(Additional note: outdated software should be addressed with a regular patch-management schedule — this reduces the attack surface for all three risks above.)*
