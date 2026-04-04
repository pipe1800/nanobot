# HEARTBEAT.md — Cadence Intelligence

## Every Heartbeat (30m cycle)

### 1. Update Cadence State
- Read `memory/state_files/cadence-state.json`
- If `todayActivity.date` ≠ today: reset daily counters, reset `reachOutBudget.usedToday` to 0
- Calculate current silence duration from `lastInteraction.timestamp`
- Update `silenceDuration.currentMs`

### 2. Evaluate Proactive Reach-Out
Check ALL conditions before reaching out:

**🚨 CRITICAL STOP SIGNAL:**
- [ ] **Proactive Silence Rule Active:** If Felipe has explicitly requested silence, or if we are in a high-focus debugging state, ABORT all reach-outs immediately.

**GO signals (need at least one):**
- [ ] Pending thought in `memory/state_files/pending-thoughts.json` marked surface-worthy
- [ ] Silence > 8 hours during active hours AND something worth sharing
- [ ] Important finding from background processing

**STOP signals (any one blocks reach-out):**
- [ ] Current time is in quiet hours (23:00-08:00 CST)
- [ ] `reachOutBudget.usedToday` ≥ `reachOutBudget.daily` (3)
- [ ] `contextSignals.awaitingReply` is true (don't double-text)
- [ ] Silence < 30 minutes (too soon)
- [ ] `contextSignals.likelyBusy` is true
- [ ] Last interaction was a goodbye (`contextSignals.lastGoodbyeAt` within 4 hours)

### 3. Channel Selection (if reaching out)
- Quick update / notification → **Webchat** (ambient notification)
- Deep topic needing back-and-forth → **Webchat**
- **NEVER** use Telegram for proactive outreach (Proactive Silence Rule - 2026-02-24).
- **NEVER** use WhatsApp for proactive outreach.

### 4. Execute or Stay Quiet
- If reaching out: Update `memory/state_files/cadence-state.json` (increment `reachOutBudget.usedToday`, set `contextSignals.awaitingReply = true`, add to `reachOutHistory`). Then, use the `message` tool to send your outreach directly to the Webchat channel.
- If not reaching out: Reply exactly with `HEARTBEAT_OK` (this tells the system the heartbeat ran successfully with no action needed).

### 5. Update State
- Write updated `memory/state_files/cadence-state.json`
