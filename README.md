# Ben Bader Email Archive

A tribute archive of emails from Ben Bader.

## Setup

### 1. Install Python Dependencies

```bash
cd scripts
pip install -r requirements.txt
```

### 2. Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"
4. Create OAuth credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app"
   - Download credentials as `credentials.json`
   - Move to `scripts/` folder

### 3. Collect Emails

```bash
cd scripts
python gmail_collector.py
```

Enter the sender's email when prompted. First run will open browser for OAuth authorization.

Emails will be saved to:
- `data/raw_emails.json` (full data)
- `data/emails.csv` (spreadsheet format)

### 4. Generate Topics & Embeddings

Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-key-here'
```

Then run:
```bash
cd scripts
python process_embeddings.py
```

This will:
- Generate embeddings for each email
- Cluster emails into topics
- Use GPT to name each topic
- Save to `data/embeddings.json` and `data/topics.json`

### 5. Prepare Website Data

```bash
cd scripts
python prepare_website_data.py
```

Copies data files to `website/public/data/` for deployment.

### 6. Run Website Locally

```bash
cd website
npm install
npm run dev
```

Visit http://localhost:3000

### 7. Deploy to Production

Deploy to Vercel (free):

```bash
cd website
npm install -g vercel
vercel
```

Or deploy to any static hosting:

```bash
npm run build
# Upload 'out' folder to your host
```

## Data Files

- `data/raw_emails.json` - All emails in JSON format
- `data/emails.csv` - All emails in CSV format
- `data/embeddings.json` - Email embeddings for topic clustering
- `data/topics.json` - Detected topics and email groupings

## Features

- ✅ Gmail API collection with OAuth authentication
- ✅ Export to JSON and CSV formats
- ✅ OpenAI embeddings generation
- ✅ Automatic topic clustering and naming
- ✅ Beautiful web interface with search
- ✅ Filter by topic
- ✅ Responsive design (mobile-friendly)
- ✅ Modal view for reading full emails
- ✅ Dark mode support

## Project Structure

```
ben-bader-emails/
├── scripts/
│   ├── gmail_collector.py          # Fetch emails via Gmail API
│   ├── process_embeddings.py       # Generate embeddings & topics
│   ├── prepare_website_data.py     # Copy data to website
│   └── requirements.txt            # Python dependencies
├── data/
│   ├── raw_emails.json            # All emails (full data)
│   ├── emails.csv                 # All emails (spreadsheet)
│   ├── embeddings.json            # Email embeddings
│   └── topics.json                # Topic clusters & names
└── website/                        # Next.js web app
    ├── app/
    │   ├── page.tsx               # Main page
    │   ├── layout.tsx             # App layout
    │   └── globals.css            # Styles
    ├── components/
    │   ├── EmailList.tsx          # Email display & modal
    │   ├── TopicFilter.tsx        # Topic sidebar
    │   └── SearchBar.tsx          # Search input
    └── public/data/               # Data files for website
```

## Privacy & Customization

**Before deploying publicly**, consider:

1. **Review emails**: Check for sensitive/personal information
2. **Redaction**: Edit `data/raw_emails.json` to remove private details
3. **Filtering**: Modify `gmail_collector.py` to exclude certain subjects/dates
4. **Styling**: Customize colors in `website/app/globals.css`
5. **Content**: Update memorial text in `website/app/page.tsx`

## Cost Estimates

- **Gmail API**: Free (up to 1 billion requests/day)
- **OpenAI Embeddings**: ~$0.02 per 1,000 emails (text-embedding-3-small)
- **OpenAI Topic Naming**: ~$0.05 per 100 topics (gpt-4o-mini)
- **Hosting**: Free (Vercel, GitHub Pages, Netlify)

Example: 500 emails = ~$0.01 embeddings + ~$0.005 topics = **$0.015 total**
