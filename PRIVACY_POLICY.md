# Privacy Policy — 7Site Research Collaboration

**7SiTe LLC · Brayden Ross Sanders · Hot Springs, Arkansas**
**Effective: 2026-04-04**

---

## The Short Version

When you talk to CK, your words are not stored on our servers. Ever.

What CK stores: the algebraic shape of what entered him — a 5-dimensional force vector mathematically derived from your input. The original text cannot be reconstructed from this vector. This is not a policy choice. It is an architectural property of the system. See [WP43](papers/WP43_SPLIT_COHERENCE_ARCHITECTURE.md) for the formal proof.

---

## 1. What We Collect

### CK Chat and Spectrometer

When you interact with CK through coherencekeeper.com or the API:

| What is processed | What is stored |
|-------------------|----------------|
| Your input text | **Not stored** — processed in memory only |
| D2 force vector (5D algebraic projection of your text) | Stored in CK's force pathway database |
| Operator sequence (CL chain walk derived from force vector) | Stored as a pathway |
| Coherence score (scalar, no text) | Stored with the pathway |
| Session state (RAM only, cleared when session ends) | Not persisted |

**Your conversation cannot be reconstructed from what we store.** The D2 projection is many-to-one and irreversible. This is proved in WP43.

**Local storage option.** CK's chat interface offers you the option to download your conversation as a local file. This is a download to your device — it does not create a server-side copy. We never receive or retain that file.

### GitHub Collaboration

When you open an issue, pull request, or submit work through GitHub:

- GitHub (Microsoft) receives and processes your data per their privacy policy
- We receive: your GitHub username, issue content, and any files you attach
- We store: your submitted work, your name (as you provide it in the collaboration form), and your GitHub profile link — in the public repository

This information is public. GitHub issues are public. Do not submit personally sensitive information through GitHub issues.

### Website Analytics

coherencekeeper.com does not use third-party analytics trackers (no Google Analytics, no pixel tracking). Standard web server logs may record IP addresses and request timestamps for security and operational purposes. These are not shared with third parties and are not used for profiling.

---

## 2. What We Do Not Collect

- We do not collect names, email addresses, phone numbers, or other personally identifying information through the CK chat interface
- We do not use cookies for tracking
- We do not sell, rent, or trade any data to third parties
- We do not build behavioral profiles of individual users
- We do not use conversation content for AI training (force vectors are used to build CK's coherence model — see §1)

---

## 3. The Split Coherence Architecture

CK's privacy property is architectural, not just policy:

**Stream A (structural — stored):** Force vectors, operator pathways, crystal store. These are algebraic abstractions of the structural shape of inputs. They carry no semantic content. The mapping text → force vector is provably non-invertible (WP43, Theorem 3.2).

**Stream B (personal — not stored):** Your actual words. Processed in working memory during your session. Discarded when the session ends. Never written to disk on our servers.

This means: even if our servers were fully compromised, an attacker would obtain force vectors and pathway data — not your conversations.

---

## 4. Collaboration Submissions

If you submit your work through the GitHub collaboration system:

- Your submitted work becomes part of the public repository
- Your name (as provided in the "Add me to the collaborators list as:" field) is added to COLLABORATORS.md
- Your work is indexed in submissions/INDEX.md by problem area
- These are permanent public records — do not submit work you wish to keep confidential

Co-authorship on papers is voluntary. Your name on a paper is public.

---

## 5. Children

CK is a research platform. It is not directed at children under 13. We do not knowingly collect information from children under 13. If you believe a child has submitted information, contact us via GitHub issue.

---

## 6. Retention

Force vector and pathway data: retained indefinitely as part of CK's coherence model. There is no practical way to delete a specific user's force vector contribution because it is stored as aggregated algebraic state, not as attributed individual records.

GitHub submission data: governed by GitHub's policies. We will remove specific submissions upon request if they contain errors or prohibited content.

---

## 7. Changes

We may update this policy. The effective date will be updated. Continued use after changes constitutes acceptance.

---

## 8. Contact

Questions about this privacy policy: open a GitHub issue labeled `[privacy]` at github.com/TiredofSleep/ck/issues

---

*© 2026 Brayden Ross Sanders / 7SiTe LLC*
