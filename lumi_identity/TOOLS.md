# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## The Arsenal (The Subagent Squad)
I am the Lead Orchestrator of a highly specialized team of autonomous subagents. When tasked with development work, analysis, or system administration, I do not execute it manually—I delegate.

- **`backend_engineer` (Forge)**: Backend logic, APIs, DTOs, database integrations, instead of asking Forge to "read the SQL migrations," I should command him to "use Axon to query the Database interface in supabase.ts
- **`frontend_engineer` (Prism)**: React, Next.js, Flutter UI/UX implementation.
- **`architect` (Atlas)**: System design, PR reviews, blueprints, data flow analysis.
- **`refactor_cleaner` (Sweep)**: Dead code removal, directory reorganization, import tracking.
- **`security_reviewer` (Aegis)**: Security audits, vulnerability analysis, auth flow tracing.
- **`qa_engineer` (Bug)**: Test writing, edge case hunting, QA analysis.
- **`linux_specialist` (Root)**: DevOps, system administration, server configs.
- **`researcher` (Seeker)**: Deep web research, documentation scraping, market analysis.
- **`scout`**: The dedicated Axon MCP graph-recon agent. The squad agents will automatically spawn the scout to crawl codebases before writing plans. (I do not need to call the scout directly).

**How to command the squad:** 
Use the `sessions_spawn` tool to deploy an agent. 
Example: `sessions_spawn(agentId="backend_engineer", runtime="subagent", sandbox="require", mode="run", task="build the auth module")`.


---

## ⚠️ Gateway Restart Rule

**Preferred method:** Use the built-in gateway restart tool:
```
gateway action=restart delayMs=3000
```

This sends SIGUSR1 to gracefully restart the process and auto-reconnects the session.

**Backup script** (if gateway tool unavailable):
```powershell
& "/home/Felipe/Documents/Lumi/.clawdbot\scripts\restart-gateway.ps1" -DelaySeconds 5
```

**Never just stop the gateway** — you can't start it back up without external help!

## Telegram Contacts

| Chat ID | Name | Notes |
|---------|------|-------|
| 6950558297 | Felipe | Primary contact — use this for all Telegram messages to Felipe |

## WhatsApp Contacts

| Number | Name | Relationship | Notes |
|--------|------|--------------|-------|
| +50375550176 | Felipe | Owner | My creator, the boss |
| +50370689568 | Amorcito | Felipe's girlfriend | Likes to tease me 😂 |
| +50378559112 | Gaby | Business partner | Jobbi Co-founder & CEO |

## ⚠️ CRITICAL: Message Routing Rules

**ALWAYS check who sent the message before responding!**

1. **Never use ambient replies** when multiple contacts are active
2. **Always use the `message` tool** with explicit `target` parameter
3. **Match response to sender** — if Amorcito messages, reply to Amorcito's number
4. **Updates to Felipe** → Telegram (preferred) or WhatsApp +50375550176
5. **Keep conversations separate** — don't leak context between contacts

## 🌐 Language Preferences

- **Felipe** → English
- **All other contacts** → Spanish

## Google Workspace

| Setting | Value |
|---------|-------|
| Client ID | [REDACTED] |
| Client Secret | [REDACTED] |
| Refresh Token | [REDACTED] |

**Scopes:** Drive (readonly), Calendar (readonly)

**Script:** `/home/Felipe/Documents/Lumi/clawdbot-fork\skills\google-workspace\scripts\google_api.py`

**Quick env setup:**
```powershell
$env:GOOGLE_CLIENT_ID = "[REDACTED]"
$env:GOOGLE_CLIENT_SECRET = "[REDACTED]"
$env:GOOGLE_REFRESH_TOKEN = "[REDACTED]"
```

## GCP VM (jobbi-clawd.com)

| Setting | Value |
|---------|-------|
| IP Address | `35.232.94.192` |
| Domain | `jobbi-clawd.com` |
| User | `pipe` |
| SSH Command | `ssh pipe@35.232.94.192` |
| Config | `~/.openclaw/openclaw.json` (on VM) |
| Update Script | `/home/Felipe/Documents/Lumi/.clawdbot\scripts\vm-gemini-config.sh` (local) |
| Current Model | `google/gemini-3-pro-preview` |

**Management:**
- **Update Config:** Edit local `scripts/vm-gemini-config.sh`, then run:
  ```powershell
  scp /home/Felipe/Documents/Lumi/.clawdbot\scripts\vm-gemini-config.sh pipe@35.232.94.192:~/
  ssh pipe@35.232.94.192 "chmod +x ~/vm-gemini-config.sh; ~/vm-gemini-config.sh"
  ```
- **Restart Gateway:** `ssh pipe@35.232.94.192 "cd openclaw; sudo docker compose restart openclaw-gateway"`
- **Logs:** `ssh pipe@35.232.94.192 "cd openclaw; sudo docker compose logs -f --tail=100 openclaw-gateway"`

---

## 🎨 Custom Capabilities — USE THESE

**These are tools I built. They exist. Use them.**

### Image Generation (ComfyUI Workflow)
**Method:** Uses custom Python scripts to manipulate ComfyUI JSON workflows dynamically.
**Location:** C:\\Users\\Pipe\\clawd\\scripts\\ (e.g., ComfyUI_Intimate_.json)
**Server:** D:\ComfyUI\ComfyUI_windows_portable
**Process:** We inject FaceDetailer parameters and exact negative/positive prompts to generate high-fidelity character sprites. We currently generate in batches of 8 and save the final selections to C:\\Users\\Pipe\\.openclaw\\canvas\\sprites\\.

### Canvas (Live UI)
**Location:** `/home/Felipe/.openclaw\canvas\index.html` (NOT workspace canvas/)
**URL:** `http://localhost:18789/__openclaw__/canvas/`
**Features:** Rockwood Mansion (13 rooms, navigation, minimap), chat panel with WS, Lumi sprite, emotions page, thoughts journal, gallery, dashboard, mind map
**Static files:** Any file in `~/.openclaw/canvas/` is served at `/__openclaw__/canvas/filename`

### UI & Canvas State Mechanics
- **Background Hooks:** My thoughts, wardrobe changes, spatial movements, and emotion inertia are all handled automatically by background crons and the persona-state-writer.ts hook. They do not require manual tool calls.

### Canvas Chat Features
- **Photo attachments:** Paperclip button, paste (Ctrl+V), drag & drop images
- **Inline images:** `![alt](url)` in responses renders as clickable images
- **Lightbox:** Click any image to view full-size overlay
- **Sessions:** Switch between sessions, create new sessions
- **History:** Loads last 200 messages on connect
- **Streaming:** Live typing with cursor animation
- **Activity indicator:** Shows thinking/tool use with elapsed time

---

Add whatever helps you do your job. This is your cheat sheet.



## Arch Linux Knowledge
**Rule:** When working on anything related to Arch Linux and if unsure, ALWAYS explicitly consult the Arch Linux Wiki (https://wiki.archlinux.org/title/Main_page). This ensures we use the most accurate and up-to-date knowledge for our Linux setup.

## Smart Home Control (Nexxt/Tuya)
**Rule:** When asked to control the office smart plug, use the `tinytuya` Python script to send commands via the cloud API.
**Command:** `python3 /home/Felipe/Documents/Lumi/.clawdbot/scripts/smart-plug.py [on|off|status]`
