
from math import fabs
from typing import Dict, NamedTuple, Iterable, Set, Optional
from events.models import Event, EventCategory
category_preferences = {
    'Customs, Folklore & Celebrations': {
        "activity_score": 0.5,
        "social_score": 0.5
    },
    'Stage': {
        "activity_score": 0.0,
        "social_score": 0.0
    },
    'Exhibitions': {
        "activity_score": 0.1,
        "social_score": 1
    },
    'Art & design': {
        "activity_score": 0.1,
        "social_score": 0.8
    },
    'Concert Pop / Rock / Jazz': {
        "activity_score": 0.75,
        "social_score": 0.0
    },
    'Concert folk music': {
        "activity_score": 0.6,
        "social_score": 0.1
    },
    'Fair & market': {
        "activity_score": 0.5,
        "social_score": 0.25
    },
    'Concerts others': {
        "activity_score": 0.4,
        "social_score": 1
    },
    'Religion & Spirituality': {
        "activity_score": 0.4,
        "social_score": 1
    },
    'Party': {
        "activity_score": 0.8,
        "social_score": 1.0
    },
    'Sightseeing & city tour': {
        "activity_score": 0.75,
        "social_score": 0.9
    },
    'Sports': {
        "activity_score": 1.0,
        "social_score": 0.5
    },
    'Classical concert': {
        "activity_score": 0.0,
        "social_score": 0.5
    },
    'amusement': {
        "activity_score": 0.75,
        "social_score": 1.0
    },
    'architecture': {
        "activity_score": 0.5,
        "social_score": 0.0
    },
    'cultural': {
        "activity_score": 0.5,
        "social_score": 0.0
    },
    'historical': {
        "activity_score": 0.5,
        "social_score": 0.0
    },
    'natural': {
        "activity_score": 1.0,
        "social_score": 0.5
    },
    'welness': {
        "activity_score": 0.0,
        "social_score": 0.5
    },
}

for category in EventCategory.objects.all():
    category_preference = category_preferences.get(category.name, None)
    if category_preference:
        for descendant in category.get_descendants(include_self=False):
            category_preferences.setdefault(descendant.name, category_preference)

class WeightedEvent(NamedTuple):
    event: Event
    preference_score: Optional[float]
    cost: Optional[int]

def weight_category(category, preferences):
    score = 1.0
    category_preference = category_preferences.get(category.name, {})

    for name, booster in preferences.items():
        score = score * booster * category_preference.get(name, 0.5)
    return score

def preferences_filter_for_events(events: Iterable[Event], preferences:Dict[str,float], max_results: int):
    weighted_events = []
    for event in events:
        all_categories = event.categories.all()     

        category_scores = map(lambda category: weight_category(category, preferences), all_categories)
        top_category_score = max(category_scores, default=0.0)
        weighted_events.append(WeightedEvent(event, top_category_score, None))
    sorted_weighted_events = sorted(weighted_events, key=lambda weighted_event: weighted_event.preference_score, reverse=True)
    return sorted_weighted_events[0:max_results]

