#!/usr/bin/env python3
"""
Test Email Embeddings with 10 emails
"""

import json
import os
from openai import OpenAI
from sklearn.cluster import KMeans
import numpy as np
from collections import defaultdict

class EmailTopicTester:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.embeddings = []
        self.emails = []

    def load_emails(self, filepath='../data/raw_emails.json', limit=10):
        """Load first N emails from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            all_emails = json.load(f)
            self.emails = all_emails[:limit]
        print(f"Loaded {len(self.emails)} emails for testing")
        print("\nEmail subjects:")
        for i, email in enumerate(self.emails, 1):
            print(f"{i}. {email['subject']}")

    def generate_embeddings(self):
        """Generate embeddings for each email"""
        print("\n🔄 Generating embeddings...")

        for i, email in enumerate(self.emails):
            text = f"{email['subject']}\n\n{email['body'][:2000]}"

            try:
                response = self.client.embeddings.create(
                    input=text,
                    model="text-embedding-3-small"
                )

                embedding = response.data[0].embedding
                self.embeddings.append({
                    'email_id': email['id'],
                    'embedding': embedding
                })

                print(f"✓ Processed {i + 1}/{len(self.emails)}")

            except Exception as e:
                print(f"✗ Error with email {email['id']}: {e}")

        print(f"\n✅ Generated {len(self.embeddings)} embeddings")

    def cluster_topics(self, n_clusters=3):
        """Cluster emails into topics"""
        if not self.embeddings:
            print("No embeddings found")
            return None

        print(f"\n🔄 Clustering into {n_clusters} topics...")

        embedding_vectors = np.array([e['embedding'] for e in self.embeddings])

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(embedding_vectors)

        topic_groups = defaultdict(list)

        for i, cluster_id in enumerate(clusters):
            email_id = self.embeddings[i]['email_id']
            email = next((e for e in self.emails if e['id'] == email_id), None)

            if email:
                topic_groups[int(cluster_id)].append({
                    'id': email['id'],
                    'subject': email['subject'],
                    'date': email['date'],
                    'snippet': email['snippet']
                })

        return topic_groups

    def generate_topic_names(self, topic_groups):
        """Use GPT to generate topic names"""
        print("\n🔄 Generating AI topic names...\n")

        topics = {}

        for topic_id, emails in topic_groups.items():
            subjects = [e['subject'] for e in emails]
            subjects_text = "\n".join(subjects)

            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{
                        "role": "system",
                        "content": "You are analyzing email subject lines. Generate a short, descriptive topic name (2-4 words) that captures the common theme."
                    }, {
                        "role": "user",
                        "content": f"Email subjects:\n{subjects_text}\n\nTopic name:"
                    }],
                    max_tokens=20,
                    temperature=0.3
                )

                topic_name = response.choices[0].message.content.strip()

                topics[f"topic_{topic_id}"] = {
                    'name': topic_name,
                    'email_count': len(emails),
                    'emails': emails
                }

                print(f"📁 Topic {topic_id + 1}: '{topic_name}' ({len(emails)} emails)")
                for email in emails:
                    print(f"   - {email['subject']}")
                print()

            except Exception as e:
                print(f"Error with topic {topic_id}: {e}")
                topics[f"topic_{topic_id}"] = {
                    'name': f"Topic {topic_id}",
                    'email_count': len(emails),
                    'emails': emails
                }

        return topics

    def save_topics(self, topics, filepath='../data/topics_test.json'):
        """Save test topics"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(topics, indent=2, fp=f, ensure_ascii=False)
        print(f"💾 Saved test topics to {filepath}")


def main():
    print("=" * 60)
    print("EMAIL TOPIC CLUSTERING TEST (10 emails)")
    print("=" * 60)

    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("\n⚠️  OPENAI_API_KEY not found")
        api_key = input("Enter OpenAI API key: ").strip()

        if not api_key:
            print("❌ API key required")
            return

    processor = EmailTopicTester(api_key)

    processor.load_emails(limit=10)

    processor.generate_embeddings()

    # Test with 3 clusters for 10 emails
    topic_groups = processor.cluster_topics(n_clusters=3)

    if topic_groups:
        topics = processor.generate_topic_names(topic_groups)
        processor.save_topics(topics)

        print("\n" + "=" * 60)
        print(f"✅ SUCCESS! Created {len(topics)} topics from 10 emails")
        print("=" * 60)
        print("\nTo use these topics on your website:")
        print("1. Copy topics_test.json to topics.json")
        print("2. Run: python prepare_website_data.py")
        print("3. Refresh your website to see the topic filter")


if __name__ == '__main__':
    main()
