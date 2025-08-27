import os
import logging
from elasticsearch import Elasticsearch, exceptions

logger = logging.getLogger(__name__)

def get_mlt_recommendations(post_id, num_results=10):
    """
    Generates recommendations for a given post_id using Elasticsearch's More Like This (MLT) query.

    Args:
        post_id (str): The ID of the post to get recommendations for.
        num_results (int): The number of recommendations to return.

    Returns:
        list: A list of recommended post_ids.
    """
    logger.info(f"Entering get_mlt_recommendations for post_id: {post_id}, num_results: {num_results}")
    try:
        es_host = os.getenv('ES_HOST')
        es_port = os.getenv('ES_PORT')

        logger.debug(f"Environment variables - ES_HOST: {es_host}, ES_PORT: {es_port}")

        # Connect to Elasticsearch using environment variables
        # Prioritize HTTPS with fingerprint if available, otherwise fall back to HTTP
        es_client_params = {
            'host': es_host,
            'port': int(es_port),
            'scheme': 'http' # Default to http
        }

        es = Elasticsearch([es_client_params])
        
        if not es.ping():
            logger.error("ERROR: Could not connect to Elasticsearch! Please check ES_HOST, ES_PORT, scheme, and credentials.")
            return []
        logger.info("Successfully connected to Elasticsearch.")

        # Define the More Like This query
        mlt_query = {
            "query": {
                "more_like_this": {
                    "fields": [ "content"],
                    "like": [
                        {
                            "_index": "post_com_idx",
                            "_id": post_id
                        }
                    ],
                    "min_term_freq": 1,
                    "min_doc_freq": 1,
                    "max_query_terms": 12
                }
            },
            "size": num_results
        }
        logger.debug(f"MLT query constructed: {mlt_query}")

        # Execute the search query
        response = es.search(index="post_com_idx", body=mlt_query)
        logger.debug(f"Elasticsearch response received: {response}")

        # Extract the recommended post_ids from the response
        recommended_post_ids = [hit['_id'] for hit in response['hits']['hits']]
        logger.info(f"Recommended post IDs: {recommended_post_ids}")

        return response.body

    except exceptions.ConnectionError as ce:
        logger.error(f"Connection Error: Could not connect to Elasticsearch. Details: {ce}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return []