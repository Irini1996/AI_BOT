from django.db import models
from django.utils import timezone
import hashlib
import json


class SearchQuery(models.Model):
    """
    Αποθηκεύει τις ερωτήσεις και τα αποτελέσματα web scraping
    """
    query_text = models.TextField(help_text="Η ερώτηση του χρήστη")
    query_hash = models.CharField(
        max_length=64, 
        unique=True, 
        db_index=True,
        help_text="SHA256 hash της ερώτησης για γρήγορη αναζήτηση"
    )
    search_results = models.JSONField(
        default=list,
        help_text="Αποτελέσματα από web scraping (URLs, titles, snippets)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    times_accessed = models.IntegerField(
        default=0,
        help_text="Πόσες φορές έχει ζητηθεί αυτή η ερώτηση"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Search Query"
        verbose_name_plural = "Search Queries"
        indexes = [
            models.Index(fields=['query_hash']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.query_text[:50]}... ({self.times_accessed} hits)"
    
    @classmethod
    def get_or_create_query(cls, query_text):
        """
        Δημιουργεί hash για την ερώτηση και την αποθηκεύει
        Αν υπάρχει ήδη, αυξάνει το counter
        """
        # Normalize το query (lowercase, trim spaces)
        normalized_query = query_text.lower().strip()
        
        # Δημιουργία SHA256 hash
        query_hash = hashlib.sha256(normalized_query.encode()).hexdigest()
        
        # Get or create
        obj, created = cls.objects.get_or_create(
            query_hash=query_hash,
            defaults={'query_text': query_text}
        )
        
        # Αν δεν είναι νέο, αύξησε το counter
        if not created:
            obj.times_accessed += 1
            obj.save()
        
        return obj, created


class AIResponse(models.Model):
    """
    Αποθηκεύει τις απαντήσεις από το AI (Ollama)
    """
    search_query = models.ForeignKey(
        SearchQuery,
        on_delete=models.CASCADE,
        related_name='ai_responses',
        help_text="Σε ποια ερώτηση αντιστοιχεί αυτή η απάντηση"
    )
    response_text = models.TextField(help_text="Η απάντηση του AI")
    model_used = models.CharField(
        max_length=100,
        default="llama3.1:8b",
        help_text="Ποιο AI model χρησιμοποιήθηκε"
    )
    response_time = models.FloatField(
        help_text="Χρόνος απάντησης σε δευτερόλεπτα"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_from_cache = models.BooleanField(
        default=False,
        help_text="Ήταν cached η απάντηση;"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "AI Response"
        verbose_name_plural = "AI Responses"
    
    def __str__(self):
        cache_status = "CACHED" if self.is_from_cache else "NEW"
        return f"[{cache_status}] {self.response_text[:50]}..."


class WebScrapedData(models.Model):
    """
    Αποθηκεύει τα scraped data από websites
    """
    search_query = models.ForeignKey(
        SearchQuery,
        on_delete=models.CASCADE,
        related_name='scraped_data',
        help_text="Για ποια ερώτηση έγινε το scraping"
    )
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=500, blank=True)
    content = models.TextField(help_text="Το κείμενο που βρέθηκε")
    snippet = models.TextField(
        max_length=500,
        blank=True,
        help_text="Σύντομο απόσπασμα"
    )
    scraped_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scraped_at']
        verbose_name = "Web Scraped Data"
        verbose_name_plural = "Web Scraped Data"
    
    def __str__(self):
        return f"{self.title[:50]} - {self.url[:50]}"