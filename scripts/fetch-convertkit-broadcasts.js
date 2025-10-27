const https = require('https');
const fs = require('fs');
const path = require('path');

const API_SECRET = 's8uxn6UitzJMsegEHsfbVvUk-40yTq6Z4AoFzEHw2dc';
const BASE_URL = 'api.kit.com';

async function fetchBroadcasts(page = 1, allBroadcasts = []) {
  return new Promise((resolve, reject) => {
    const url = `/v3/broadcasts?api_secret=${API_SECRET}&page=${page}`;

    console.log(`Fetching page ${page}...`);

    https.get({ hostname: BASE_URL, path: url }, (res) => {
      let data = '';

      res.on('data', chunk => data += chunk);

      res.on('end', () => {
        try {
          const json = JSON.parse(data);

          if (json.broadcasts && json.broadcasts.length > 0) {
            allBroadcasts.push(...json.broadcasts);
            console.log(`  Found ${json.broadcasts.length} broadcasts on page ${page}`);

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

async function fetchBroadcastContent(broadcastId) {
  return new Promise((resolve, reject) => {
    const url = `/v3/broadcasts/${broadcastId}?api_secret=${API_SECRET}`;

    https.get({ hostname: BASE_URL, path: url }, (res) => {
      let data = '';

      res.on('data', chunk => data += chunk);

      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.broadcast);
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
    console.log('Fetching ConvertKit broadcasts...\n');

    const broadcasts = await fetchBroadcasts();

    console.log(`\n✓ Retrieved ${broadcasts.length} total broadcast IDs`);
    console.log('\nFetching full content for each broadcast...\n');

    const fullBroadcasts = [];

    for (let i = 0; i < broadcasts.length; i++) {
      const broadcast = broadcasts[i];
      process.stdout.write(`\r[${i + 1}/${broadcasts.length}] Fetching: ${broadcast.subject.substring(0, 50)}...`);

      try {
        const fullBroadcast = await fetchBroadcastContent(broadcast.id);
        fullBroadcasts.push(fullBroadcast);
        await delay(100); // 100ms delay between requests
      } catch (err) {
        console.error(`\n  Error fetching broadcast ${broadcast.id}: ${err.message}`);
      }
    }

    console.log(`\n\n✓ Retrieved full content for ${fullBroadcasts.length} broadcasts`);

    const outputPath = path.join(__dirname, '../data/convertkit-broadcasts-full.json');
    fs.writeFileSync(outputPath, JSON.stringify(fullBroadcasts, null, 2));

    console.log(`✓ Saved to: ${outputPath}`);

    console.log('\nSample broadcast with content:');
    if (fullBroadcasts.length > 0) {
      const sample = fullBroadcasts[0];
      console.log(`  ID: ${sample.id}`);
      console.log(`  Subject: ${sample.subject}`);
      console.log(`  Created: ${sample.created_at}`);
      console.log(`  Content preview: ${sample.content ? sample.content.substring(0, 100) : 'N/A'}...`);
    }

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
})();
