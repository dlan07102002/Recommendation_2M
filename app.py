import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import logging
import redis

from recommender.content_based import get_mlt_recommendations
from config.logging_config import setup_logging

# Load environment variables from .env file
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

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
    logger.info(f"Received request for post_id: {post_id}")
    # Check if post_id is provided
    if not post_id:
        logger.warning("post_id parameter is required but not provided.")
        return jsonify({"error": "post_id parameter is required"}), 400

    # Define the cache key for Redis
    cache_key = f"recommendations:mlt:{post_id}"

    try:
        # Check for cached result in Redis
        cached_recommendations = redis_client.get(cache_key)
        if cached_recommendations:
            logger.info(f"Recommendations for post_id: {post_id} found in cache.")
            # If found, decode and return the cached result
            return jsonify(json.loads(cached_recommendations)), 200
        logger.info(f"No cache found for post_id: {post_id}. Fetching from Elasticsearch.")
        # If not in cache, fetch recommendations from Elasticsearch
        recommendations = get_mlt_recommendations(post_id)

        # Cache the new recommendations in Redis with a 30-minute expiration
        # redis_client.setex(cache_key, 1800, json.dumps(recommendations))

        # Return the recommendations as a JSON response
        return jsonify(recommendations), 200

    except Exception as e:
        logger.error(f"An error occurred during recommendation process: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info(f"Starting Flask app in debug mode on port {int(os.getenv('FLASK_PORT', 5000))}")
    app.run(debug=True, port=int(os.getenv('FLASK_PORT', 5000)))