# Supervisor Strategy — "assume absent until called" (2026-09-01)

Policy: **no decision blocks on the supervisor.** Where his input would be
needed, we adopt the best evidence-backed default, document it, and batch
everything he might veto into ONE message for whenever Farzam chooses to
contact him. The approved proposal v05 is the authority until he overrides.

## A. What ONLY he (or the university) can provide — the real ask-list
1. **Defense formalities (IAU S&R specific):** exact thesis template/chapter
   structure; whether an MSc defense requires a **published/submitted paper**
   (common in IAU engineering); iThenticate/similarity threshold; defense
   committee composition expectations.
2. **Supervision status:** is he still formally within his capacity to sign
   the defense forms (ظرفیت راهنمایی), per the form's own warning clause?
   (Political risk if half-abandoned — clarify early, cheap to ask.)
3. **IranDoc/سازمان سنجش status:** title-similarity registration confirmed?
   (The form's فرم شماره 3 references irandoc/sika — verify the clearance
   actually happened.)
4. **His endorsement of two technical adjudications** (protective, not
   blocking — both are already defensible from the approved text):
   a. RQ0 = O1 (pipeline as committed system, recurrent encoder as internal
      comparison — no amendment needed);
   b. Two-tier environment (abstract env trains; Mininet-WiFi+Ryu delivers
      the proposal's own "Emulation vs Simulation" chapter).

## B. What we self-served (no longer questions)
- Domain scope highway vs urban → **both** (abstract env makes scenario
  cost ≈ 0; CMC'21 lesson: mobility scenarios are the credibility core).
- Contribution framing → application-level novelty (from approved proposal).
- Baseline set → B0–B6 incl. proposal-mandated Marwein.
- Metric contract → proposal formulas (E_lb, QoS, R) as primary + Jain/
  lead-time as robustness additions.
- Tools → Python/NumPy/SUMO/Mininet-WiFi/Ryu — all named in the proposal.

## C. The ONE message (send whenever; in Persian or English)
> استاد سلام، پیشرفت کار: مرور ادبیات کامل، چارچوب روش تصمیم‌گیری، و سناریوهای
> شبیه‌سازی تعیین شده‌اند. چند سؤال کوتاه برای هماهنگی:
> 1. آیا برای دفاع مقاله استخراجی الزامی است؟ قالب و چک‌لیست دانشگاه چیست؟
> 2. آیا ظرفیت راهنمایی برای دفاع فعال است؟ (طبق فرم پروپوزال)
> 3. تأیید ایران‌داک/سکا انجام شده؟
> 4. دو تصمیم فنی (تفسیر DQN+LSTM به‌صورت پیش‌بینی‌ساز→تصمیم‌گیر طبق متن مصوب،
>    و محیط شبیه‌سازی دومرحله‌ای) — اگر اعتراضی دارید بفرمایید.
> 5. زمان تماس/جلسه مناسب شما؟

## D. Cadence if he stays silent
Self-serve everything (B), keep the audit trail (this repo = the
decision log he'd want to see), and re-ask formally once per month. The
repo's GitOps history doubles as the progress report for any intervention
by the department (مدیرگروه) if supervision ever formally fails.
