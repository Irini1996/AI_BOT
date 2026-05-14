from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time

from .models import SearchQuery, AIResponse, WebScrapedData
from .utils import ask_ollama, google_search, scrape_webpage


@csrf_exempt
def chat(request):
    """
    Το κύριο endpoint για το chatbot
    
    POST /chat/
    Body: {"query": "Τι είναι η Python;"}
    
    Returns: {"response": "...", "time": 2.5, "cached": false}
    """
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        query_text = data.get('query', '').strip()
        
        if not query_text:
            return JsonResponse({'error': 'Query is required'}, status=400)
        
        # ΒΗΜΑ 1: Έλεγξε αν υπάρχει στη βάση
        search_query, created = SearchQuery.get_or_create_query(query_text)
        
        # ΒΗΜΑ 2: Αν υπάρχει ήδη απάντηση, επέστρεψέ την
        if not created:
            existing_response = search_query.ai_responses.first()
            if existing_response:
                return JsonResponse({
                    'response': existing_response.response_text,
                    'time': existing_response.response_time,
                    'cached': True,
                    'times_accessed': search_query.times_accessed
                })
        
        # ΒΗΜΑ 3: Νέα ερώτηση - Ψάξε online
        start_time = time.time()
        
        # Google Search
        search_results = google_search(query_text, num_results=3)
        search_query.search_results = search_results
        search_query.save()
        
        # Scrape τις σελίδες
        scraped_content = []
        for result in search_results[:3]:
            url = result.get('url')
            if url:
                webpage_data = scrape_webpage(url)
                
                # Αποθήκευση στη βάση
                WebScrapedData.objects.create(
                    search_query=search_query,
                    url=url,
                    title=webpage_data.get('title', ''),
                    content=webpage_data.get('content', ''),
                    snippet=result.get('snippet', '')
                )
                
                scraped_content.append(webpage_data.get('content', ''))
        
        # ΒΗΜΑ 4: Φτιάξε το prompt για το Ollama
        context = '\n\n'.join(scraped_content[:3])
        
        prompt = f"""Based on the following information from web search:

{context}

Please answer this question: {query_text}

Provide a clear, concise answer in Greek if the question is in Greek, otherwise in English."""
        
        # ΒΗΜΑ 5: Ρώτα το Ollama
        ai_result = ask_ollama(prompt)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # ΒΗΜΑ 6: Αποθήκευση της απάντησης
        AIResponse.objects.create(
            search_query=search_query,
            response_text=ai_result['response'],
            response_time=total_time,
            is_from_cache=False
        )
        
        # ΒΗΜΑ 7: Επιστροφή απάντησης
        return JsonResponse({
            'response': ai_result['response'],
            'time': total_time,
            'cached': False,
            'search_results_count': len(search_results)
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def index(request):
    """
    Η αρχική σελίδα (θα φτιάξουμε μετά)
    """
    from django.shortcuts import render
    return render(request, 'chatbot/index.html')