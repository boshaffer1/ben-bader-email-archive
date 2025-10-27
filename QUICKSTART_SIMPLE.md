# Quick Start - Simple Version (No AI)

Get the tribute site up in 3 steps:

## Step 1: Gmail API Setup (5 min)

1. Go to https://console.cloud.google.com/
k
2. Create project → Enable Gmail API
3. Credentials → OAuth Client ID → Desktop App
4. Download `credentials.json` → Move to `scripts/` folder

[Detailed instructions in README.md if needed]

## Step 2: Collect Emails (5 min)

```bash
cd scripts
pip install -r requirements.txt
python gmail_collector.py
```

Enter sender's email when prompted.
Browser opens for authorization (first time only).

**Emails saved to**: `data/raw_emails.json` & `data/emails.csv`

## Step 3: Launch Website (2 min)

```bash
python prepare_website_data.py
cd ../website
npm install
npm run dev
```

**Visit**: http://localhost:3000

---

## Deploy (Optional)

**Vercel** (free, recommended):
```bash
cd website
npx vercel
```

**Or build static site**:
```bash
npm run build
npm run export
```

Upload `out/` folder to any static host.

---

## Add AI Topics Later (Optional)

If you want topic clustering:

```bash
export OPENAI_API_KEY='sk-...'
cd scripts
python process_embeddings.py
python prepare_website_data.py
```

Topics will auto-appear on website.

---

## That's It!

- ✅ All emails searchable
- ✅ Full email reader
- ✅ Mobile-friendly
- ✅ Dark mode
- ✅ Free hosting
