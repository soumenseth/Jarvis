from googlesearch import search
from urllib.parse import urlparse


class GoogleSearch:
    def __init__(self, search_query, num_results=10, stop=10, pause=2):
        self.search_query = search_query
        self.num_results = num_results
        self.stop = stop
        self.pause = pause

    def get_query_result(self):
        search_results = {}
        for r in search(self.search_query, tld="co.in", num=self.num_results, stop=self.stop, pause=self.pause):
            domain = urlparse(r).netloc
            if domain in search_results.keys():
                search_results[domain]['links'].append(r)
                search_results[domain]['count'] += 1
            else:
                search_results.update({
                    domain: {
                        'links': [r],
                        'count': 1
                    }
                })
        return search_results


if __name__ == "__main__":
    gsearch = GoogleSearch(search_query="python pandas keyerror", num_results=20, stop=20).get_query_result()
    print(gsearch)