# Quick Start Guide

Follow these steps to create the email archive:

## Step 1: Set Up Gmail API (5 min)

1. Visit https://console.cloud.google.com/
2. Create a new project: "Ben Bader Emails"
3. Click "Enable APIs & Services"
4. Search for "Gmail API" → Enable
5. Go to Credentials → Create OAuth Client ID → Desktop App
6. Download `credentials.json`
7. Move it to the `scripts/` folder

## Step 2: Collect Emails (5-10 min)

```bash
cd scripts
pip install -r requirements.txt
python gmail_collector.py
```

When prompted, enter the sender's email address.

Browser will open for Gmail authorization (first time only).

## Step 3: Generate Topics (5-10 min)

Get an OpenAI API key from https://platform.openai.com/api-keys

```bash
export OPENAI_API_KEY='sk-...'
python process_embeddings.py
```

## Step 4: Prepare & Launch Website (2 min)

```bash
python prepare_website_data.py
cd ../website
npm install
npm run dev
```

Visit http://localhost:3000

## Step 5: Deploy (Optional)

**Vercel (recommended)**:
```bash
npm install -g vercel
vercel
```

**Or export static site**:
```bash
npm run build
```

Then upload to any static host.

---

## Troubleshooting

**Gmail API Error**: Make sure `credentials.json` is in `scripts/` folder

**OpenAI Error**: Check API key is set: `echo $OPENAI_API_KEY`

**Website blank**: Run `prepare_website_data.py` to copy data files

**Need help?**: Check README.md for detailed instructions
