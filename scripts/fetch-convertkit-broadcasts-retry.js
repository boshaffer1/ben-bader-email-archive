const https = require('https');
const fs = require('fs');
const path = require('path');

const API_SECRET = 's8uxn6UitzJMsegEHsfbVvUk-40yTq6Z4AoFzEHw2dc';
const BASE_URL = 'api.kit.com';
const DELAY_MS = 500; // Increased delay between requests
const MAX_RETRIES = 3;

async function fetchBroadcasts(page = 1, allBroadcasts = []) {
  return new Promise((resolve, reject) => {
    const url = `/v3/broadcasts?api_secret=${API_SECRET}&page=${page}`;

    https.get({ hostname: BASE_URL, path: url }, (res) => {
      let data = '';

      res.on('data', chunk => data += chunk);

      res.on('end', () => {
        try {
          const json = JSON.parse(data);

          if (json.broadcasts && json.broadcasts.length > 0) {
            allBroadcasts.push(...json.broadcasts);

            if (json.broadcasts.length === 50) {
              fetchBroadcasts(page + 1, allBroadcasts).then(resolve).catch(reject);
            } else {
              resolve(allBroadcasts);
            }
          } else {
            resolve(allBroadcasts);
          }
        } catch (err) {
          reject(err);
        }
      });
    }).on('error', reject);
  });
}

async function fetchBroadcastContent(broadcastId, retryCount = 0) {
  return new Promise((resolve, reject) => {
    const url = `/v3/broadcasts/${broadcastId}?api_secret=${API_SECRET}`;

    https.get({ hostname: BASE_URL, path: url }, (res) => {
      let data = '';

      res.on('data', chunk => data += chunk);

      res.on('end', async () => {
        try {
          // Check if we got a rate limit response
          if (data.includes('Retry later')) {
            if (retryCount < MAX_RETRIES) {
              const waitTime = Math.pow(2, retryCount) * 2000; // Exponential backoff: 2s, 4s, 8s
              console.log(`\n  Rate limited. Waiting ${waitTime/1000}s before retry ${retryCount + 1}/${MAX_RETRIES}...`);
              await delay(waitTime);
              const result = await fetchBroadcastContent(broadcastId, retryCount + 1);
              resolve(result);
            } else {
              reject(new Error('Rate limited - max retries exceeded'));
            }
          } else {
            const json = JSON.parse(data);
            resolve(json.broadcast);
          }
        } catch (err) {
          reject(err);
        }
      });
    }).on('error', reject);
  });
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  try {
    const outputPath = path.join(__dirname, '../data/convertkit-broadcasts-full.json');

    // Load existing broadcasts if available
    let existingBroadcasts = [];
    if (fs.existsSync(outputPath)) {
      console.log('Loading existing broadcasts...');
      existingBroadcasts = JSON.parse(fs.readFileSync(outputPath, 'utf8'));
      console.log(`Found ${existingBroadcasts.length} existing broadcasts\n`);
    }

    // Get list of all broadcast IDs
    console.log('Fetching broadcast list...\n');
    const broadcasts = await fetchBroadcasts();
    console.log(`\n✓ Retrieved ${broadcasts.length} total broadcast IDs`);

    // Create a Set of existing IDs for fast lookup
    const existingIds = new Set(existingBroadcasts.map(b => b.id));
    const remaining = broadcasts.filter(b => !existingIds.has(b.id));

    console.log(`✓ ${existingBroadcasts.length} already fetched`);
    console.log(`✓ ${remaining.length} remaining to fetch\n`);

    if (remaining.length === 0) {
      console.log('All broadcasts already fetched!');
      return;
    }

    console.log('Fetching full content...\n');

    const fullBroadcasts = [...existingBroadcasts];
    let successCount = 0;
    let failCount = 0;

    for (let i = 0; i < remaining.length; i++) {
      const broadcast = remaining[i];
      const totalProgress = existingBroadcasts.length + i + 1;

      process.stdout.write(`\r[${totalProgress}/${broadcasts.length}] ${broadcast.subject.substring(0, 50)}...`);

      try {
        const fullBroadcast = await fetchBroadcastContent(broadcast.id);
        fullBroadcasts.push(fullBroadcast);
        successCount++;

        // Save progress every 10 broadcasts
        if ((i + 1) % 10 === 0) {
          fs.writeFileSync(outputPath, JSON.stringify(fullBroadcasts, null, 2));
        }

        await delay(DELAY_MS);
      } catch (err) {
        console.error(`\n  ✗ Failed: ${broadcast.id} - ${err.message}`);
        failCount++;

        // If we hit too many failures in a row, stop
        if (failCount > 5) {
          console.log('\n\nToo many failures. Saving progress and stopping...');
          break;
        }
      }
    }

    // Final save
    fs.writeFileSync(outputPath, JSON.stringify(fullBroadcasts, null, 2));

    console.log(`\n\n✓ Retrieved full content for ${fullBroadcasts.length} total broadcasts`);
    console.log(`✓ Successfully fetched ${successCount} new broadcasts`);
    if (failCount > 0) {
      console.log(`✗ Failed to fetch ${failCount} broadcasts`);
    }
    console.log(`✓ Saved to: ${outputPath}`);

    if (fullBroadcasts.length > 0) {
      const sample = fullBroadcasts[0];
      console.log('\nSample broadcast with content:');
      console.log(`  ID: ${sample.id}`);
      console.log(`  Subject: ${sample.subject}`);
      console.log(`  Created: ${sample.created_at}`);
      console.log(`  Content length: ${sample.content ? sample.content.length : 0} characters`);
    }

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
})();
