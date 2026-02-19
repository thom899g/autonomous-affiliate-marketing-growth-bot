import google.auth
from shopify import Shopify

class GoogleAnalyticsIntegration:
    def __init__(self, api_key: str):
        self.client = google.auth.api_key.ApiKeyCredentials(api_key)
        
    def fetch_data(self, start_date: str, end_date: str) -> Dict:
        """
        Fetches analytics data from Google Analytics.
        Args:
            start_date: Start date for the report.
            end_date: End date for the report.
        Returns:
            Dictionary containing analytics data.
        """
        try:
            response = requests.get(
                f'https://www.googleapis.com/analytics/v3/data/ga',
                params={
                    'ids': 'ga:123456789',
                    'start-date': start_date,
                    'end-date': end_date
                },
                headers={'Authorization': f'Bearer {self.client._token}'}
            )
            response.raise_for_status()
            
            return response.json()['data']
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch Google Analytics data: {str(e)}")
            raise

class ShopifyIntegration:
    def __init__(self, shop_url: str, api_key: str):
        self.client = Shopify(shop_url, api_key)
        
    def get_products(self) -> List[Dict]:
        """
        Retrieves all products from Shopify.
        Returns:
            List of product dictionaries.
        """
        try:
            products = []
            cursor = None
            
            while True:
                params = {'limit': 50}
                if cursor:
                    params['cursor'] = cursor
                
                response = self.client.get('products', params=params)
                products.extend(response.body()['products'])
                
                if not response.headers.get('Link'):
                    break
                cursor = response.headers.get('Link').split('&')[1].split('=')[1]
            
            return products
        except Exception as e:
            logging.error(f"Failed to fetch Shopify products: {str(e)}")
            raise