import os
from elasticsearch import Elasticsearch, exceptions

# Configure logging for debugging

def get_mlt_recommendations(post_id, num_results=10):
    """
    Generates recommendations for a given post_id using Elasticsearch's More Like This (MLT) query.

    Args:
        post_id (str): The ID of the post to get recommendations for.
        num_results (int): The number of recommendations to return.

    Returns:
        list: A list of recommended post_ids.
    """
    print(f"Entering get_mlt_recommendations for post_id: {post_id}, num_results: {num_results}")
    try:
        es_host = os.getenv('ES_HOST')
        es_port = os.getenv('ES_PORT')

        print(f"Environment variables - ES_HOST: {es_host}, ES_PORT: {es_port}")

        # Connect to Elasticsearch using environment variables
        # Note: Fingerprint is only relevant for HTTPS connections.
        # Ensure ES_FINGERPRINT is set in your .env file.
        es = Elasticsearch(f"http://{es_host}:{es_port}")
        
        # es = Elasticsearch(f"http://{es_username}:{es_password}@{es_host}:{es_port}")
        print(F"Elasticsearch client url constructed.: http://{es_host}:{es_port}")
        print("Elasticsearch client initialized.")
        # if not es.ping():
        #     print("ERROR: Could not connect to Elasticsearch! Please check ES_HOST and ES_PORT.")
        #     return []
        print("Successfully connected to Elasticsearch.")

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
        print(f"MLT query constructed: {mlt_query}")

        # Execute the search query
        response = es.search(index="post_com_idx", body=mlt_query)
        print(f"Elasticsearch response received: {response}")

        # Extract the recommended post_ids from the response
        recommended_post_ids = [hit['_id'] for hit in response['hits']['hits']]
        print(f"Recommended post IDs: {recommended_post_ids}")

        return recommended_post_ids

    except exceptions.ConnectionError as ce:
        # Handle connection errors to Elasticsearch
        print(f"Connection Error: Could not connect to Elasticsearch. Details: {ce}")
        return []
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
        return []