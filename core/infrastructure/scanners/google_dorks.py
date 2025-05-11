import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

from dotenv import load_dotenv
import logging
from typing import List, Dict, Optional

# ---------------- Configuración de Logging ----------------
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_env()-> Optional[Dict[str,str]]:
#load environment variables from .env file
   load_dotenv()
   api_key=os.getenv("API_KEY")#
   search_engine_id=os.getenv("SEARCH_ENGINE_ID")#
   if not api_key or not search_engine_id:
    logging.error("API_KEY or SEARCH_ENGINE_ID not found in environment variables.")
    return None
   return {
    'api_key': api_key,
    'search_engine_id': search_engine_id
   }


def perfom_google_search(api_key: str, search_engine_id: str, query: str,start:int=1, lang:str='lang_es')-> Optional[List[Dict]]:
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'start': start,
        'lr': lang
    }

    try:
        response = requests.get(base_url, params=params,timeout=10)
        response.raise_for_status() #raise an errorr for bad response
        data = response.json()
        return data.get('items', [])

    except ConnectionError:
        logging.error("Connection error occurred.")
    except Timeout:
        logging.error("Request timed out.")
    except RequestException as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None        
        

   #ejecucion principal
# def main():
#     env_vars = load_env()
#     print(env_vars)
#
#     if env_vars is None:
#         logging.error("Failed to load environment variables.")
#         return
#     
#     query = 'filetype:sql "MySQL dump" (pass | password | passcode )'
#     results = perfom_google_search(
#         api_key=env_vars['api_key'],
#         search_engine_id=env_vars['search_engine_id'],
#         query=query
#     )
#
#     if results:
#         for index, result in enumerate(results):
#             title = result.get('title')
#             link = result.get('link')
#             snippet = result.get('snippet')
#             logging.info(f"Result {index + 1}:")
#             logging.info(f"Title: {title}")
#             logging.info(f"Link: {link}")
#             logging.info(f"Snippet: {snippet}")
#     else:
#         logging.info("No results found.")


#uso de 2 docker mas para el analisis
def main():
    env_vars = load_env()

    if env_vars is None:
        logging.error("Failed to load environment variables.")
        return

    dorks = [
        'filetype:sql "MySQL dump" (pass | password | passcode )',  # el original
        'inurl:wp-config.php',                                       # Dork 1
        'ext:zip | ext:rar | ext:tar backup'                         # Dork 2
    ]

    for query in dorks:
        logging.info(f"\n\n🔍 Ejecutando búsqueda para: {query}")
        results = perfom_google_search(
            api_key=env_vars['api_key'],
            search_engine_id=env_vars['search_engine_id'],
            query=query
        )

        if results:
            for index, result in enumerate(results):
                title = result.get('title')
                link = result.get('link')
                snippet = result.get('snippet')
                logging.info(f"Result {index + 1}:")
                logging.info(f"Title: {title}")
                logging.info(f"Link: {link}")
                logging.info(f"Snippet: {snippet}")
        else:
            logging.info("No se encontraron resultados.")


def perform_dorks(query):
    env_vars = load_env()
    if env_vars is None:
        return []

    api_key = env_vars["api_key"]
    search_engine_id = env_vars["search_engine_id"]

    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'lr': 'lang_es',
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        print(response.json())  # 👈 AQUÍ VA CTM
        response.raise_for_status()
        return response.json().get('items', [])
    except Exception as e:
        print(f"❌ Error en perform_dorks: {e}")
        return []




if __name__ == "__main__":
    main()




