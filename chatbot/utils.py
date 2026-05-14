import requests
import json
import time


def ask_ollama(prompt, model="llama3.1:8b"):
    """
    Στέλνει ερώτηση στο Ollama και παίρνει απάντηση
    
    Args:
        prompt: Η ερώτηση (string)
        model: Το AI model (default: llama3.1:8b)
    
    Returns:
        dict: {'response': 'η απάντηση', 'time': 2.5}
    """
    
    start_time = time.time()
    
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        response_text = result.get('response', '')
        
        end_time = time.time()
        response_time = end_time - start_time
        
        return {
            'response': response_text,
            'time': response_time
        }
    
    except Exception as e:
        return {
            'response': f'Error: {str(e)}',
            'time': 0
        }


def google_search(query, num_results=5):
    """
    Ψάχνει στο Google και επιστρέφει URLs
    
    Args:
        query: Η ερώτηση
        num_results: Πόσα αποτελέσματα να φέρει
    
    Returns:
        list: Λίστα με dictionaries {'title': '...', 'url': '...', 'snippet': '...'}
    """
    from bs4 import BeautifulSoup
    
    search_url = f"https://www.google.com/search?q={query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        search_results = soup.find_all('div', class_='g')
        
        for result in search_results[:num_results]:
            try:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                snippet_elem = result.find('div', class_='VwiC3b')
                
                if title_elem and link_elem:
                    title = title_elem.get_text()
                    url = link_elem.get('href')
                    snippet = snippet_elem.get_text() if snippet_elem else ''
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
            except:
                continue
        
        return results
    
    except Exception as e:
        print(f"Google search error: {e}")
        return []


def scrape_webpage(url):
    """
    Διαβάζει το περιεχόμενο μιας σελίδας
    
    Args:
        url: Το URL της σελίδας
    
    Returns:
        dict: {'title': '...', 'content': '...'}
    """
    from bs4 import BeautifulSoup
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Βρες τον τίτλο
        title = soup.find('title')
        title_text = title.get_text() if title else ''
        
        # Βρες το κύριο περιεχόμενο
        # Αφαίρεσε scripts και styles
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Πάρε το κείμενο
        content = soup.get_text()
        
        # Καθάρισε το κείμενο
        lines = (line.strip() for line in content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        content = ' '.join(chunk for chunk in chunks if chunk)
        
        # Κράτα μόνο τα πρώτα 5000 χαρακτήρες
        content = content[:5000]
        
        return {
            'title': title_text,
            'content': content
        }
    
    except Exception as e:
        print(f"Scraping error for {url}: {e}")
        return {
            'title': '',
            'content': ''
        }