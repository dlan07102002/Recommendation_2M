import os
from elasticsearch import Elasticsearch, exceptions

def get_mlt_recommendations(post_id, num_results=10):
    """
    Generates recommendations for a given post_id using Elasticsearch's More Like This (MLT) query.

    Args:
        post_id (str): The ID of the post to get recommendations for.
        num_results (int): The number of recommendations to return.

    Returns:
        list: A list of recommended post_ids.
    """
    try:
        # Connect to Elasticsearch using environment variables
        es = Elasticsearch([{'host': os.getenv('ES_HOST'), 'port': int(os.getenv('ES_PORT'))}])

        # Define the More Like This query
        mlt_query = {
            "query": {
                "more_like_this": {
                    "fields": ["title", "description", "category"],
                    "like": [
                        {
                            "_index": "posts",
                            "_id": post_id
                        }
                    ],
                    "min_term_freq": 1,
                    "max_query_terms": 12
                }
            },
            "size": num_results
        }

        # Execute the search query
        response = es.search(index="posts", body=mlt_query)

        # Extract the recommended post_ids from the response
        recommended_post_ids = [hit['_id'] for hit in response['hits']['hits']]

        return recommended_post_ids

    except exceptions.ConnectionError:
        # Handle connection errors to Elasticsearch
        print("Error: Could not connect to Elasticsearch.")
        return []
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return []