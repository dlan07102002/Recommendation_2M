import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import redis

from recommender.content_based import get_mlt_recommendations

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Connect to Redis using environment variables
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0
)

@app.route('/api/v1/recommendations', methods=['GET'])
def recommend():
    """Endpoint to get post recommendations."""
    # Get post_id from query parameters
    post_id = request.args.get('post_id')
    print(f"Received request for post_id: {post_id}")
    # Check if post_id is provided
    if not post_id:
        return jsonify({"error": "post_id parameter is required"}), 400

    # Define the cache key for Redis
    cache_key = f"recommendations:mlt:{post_id}"

    try:
        # Check for cached result in Redis
        cached_recommendations = redis_client.get(cache_key)
        if cached_recommendations:
            # If found, decode and return the cached result
            return jsonify(json.loads(cached_recommendations)), 200
        print(f"No cache found for post_id: {post_id}. Fetching from Elasticsearch.")
        # If not in cache, fetch recommendations from Elasticsearch
        recommendations = get_mlt_recommendations(post_id)

        # Cache the new recommendations in Redis with a 30-minute expiration
        # redis_client.setex(cache_key, 1800, json.dumps(recommendations))

        # Return the recommendations as a JSON response
        return jsonify(recommendations), 200

    except Exception as e:
        # Handle potential errors, such as Redis connection issues
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('FLASK_PORT', 5000)))