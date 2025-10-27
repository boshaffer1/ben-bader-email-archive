# Fix OAuth Redirect URI Error

## Step 1: Go to OAuth Client Settings

1. Visit: https://console.cloud.google.com/apis/credentials
2. Find your OAuth client (the one you created: "ben emails")
3. Click on the client name to edit it

## Step 2: Add Authorized Redirect URIs

In the "Authorized redirect URIs" section, click "+ ADD URI" and add ALL of these:

```
http://localhost:8080/
http://localhost:8080
http://localhost/
http://localhost
urn:ietf:wg:oauth:2.0:oob
```

**Important**: Add each one separately (5 total URIs)

## Step 3: Save and Wait

1. Click "SAVE" at the bottom
2. Wait 2-3 minutes for changes to take effect

## Step 4: Delete Token and Retry

```bash
cd '/Users/boshaffer/ben bader emails/scripts'
rm -f token.pickle
python3 gmail_collector.py
```

---

## If Still Not Working: Use Desktop App Type

Make sure your OAuth client is set to **Application type: Desktop app**

If it says "Web application", delete it and create a new one:
1. Delete current OAuth client
2. Create Credentials → OAuth client ID
3. Choose **Desktop app** (not Web application)
4. Download JSON → replace credentials.json
5. Try again

---

## Screenshot for Reference

The settings page should look like this:

**Application type**: Desktop app
**Authorized redirect URIs**: (add the 5 URIs listed above)

Once you see all 5 URIs listed, click Save and wait 2 minutes.
