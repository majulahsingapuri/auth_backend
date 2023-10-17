from django.contrib.postgres.search import TrigramWordSimilarity
from django.db import models


class FuzzySearchable(models.QuerySet):
    def fuzzy_search(self, query, field="name"):
        if not query:
            return self
        return (
            self.annotate(similarity=TrigramWordSimilarity(query, field))
            .filter(**{f"{field}__trigram_word_similar": query})
            .order_by("-similarity")
        )
