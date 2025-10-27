#!/usr/bin/env python3
"""
Email Embeddings & Topic Generator
Generates embeddings for emails and clusters them into topics
"""

import json
import os
from openai import OpenAI
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
from collections import defaultdict

class EmailTopicProcessor:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.embeddings = []
        self.emails = []

    def load_emails(self, filepath='../data/raw_emails.json'):
        """Load emails from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.emails = json.load(f)
        print(f"Loaded {len(self.emails)} emails")

    def generate_embeddings(self):
        """Generate embeddings for each email"""
        print("Generating embeddings...")

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

                if (i + 1) % 10 == 0:
                    print(f"Processed {i + 1}/{len(self.emails)} emails")

            except Exception as e:
                print(f"Error generating embedding for email {email['id']}: {e}")

        print(f"Generated {len(self.embeddings)} embeddings")

    def cluster_topics(self, n_clusters=10):
        """Cluster emails into topics using K-means"""
        if not self.embeddings:
            print("No embeddings found. Run generate_embeddings() first.")
            return None

        print(f"Clustering into {n_clusters} topics...")

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
        """Use GPT to generate descriptive names for each topic cluster"""
        print("Generating topic names...")

        topics = {}

        for topic_id, emails in topic_groups.items():
            subjects = [e['subject'] for e in emails[:10]]
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

                print(f"Topic {topic_id}: {topic_name} ({len(emails)} emails)")

            except Exception as e:
                print(f"Error generating name for topic {topic_id}: {e}")
                topics[f"topic_{topic_id}"] = {
                    'name': f"Topic {topic_id}",
                    'email_count': len(emails),
                    'emails': emails
                }

        return topics

    def save_embeddings(self, filepath='../data/embeddings.json'):
        """Save embeddings to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.embeddings, indent=2, fp=f)
        print(f"Saved embeddings to {filepath}")

    def save_topics(self, topics, filepath='../data/topics.json'):
        """Save topics to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(topics, indent=2, fp=f, ensure_ascii=False)
        print(f"Saved topics to {filepath}")


def main():
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment")
        api_key = input("Enter OpenAI API key (or press Enter to set env var): ").strip()

        if not api_key:
            print("Please set OPENAI_API_KEY environment variable and try again")
            return

    processor = EmailTopicProcessor(api_key)

    processor.load_emails()

    processor.generate_embeddings()
    processor.save_embeddings()

    n_clusters = min(10, len(processor.emails) // 5)
    if n_clusters < 2:
        n_clusters = 2

    topic_groups = processor.cluster_topics(n_clusters=n_clusters)

    if topic_groups:
        topics = processor.generate_topic_names(topic_groups)
        processor.save_topics(topics)

        print(f"\n✓ Successfully processed {len(processor.emails)} emails into {len(topics)} topics")


if __name__ == '__main__':
    main()
