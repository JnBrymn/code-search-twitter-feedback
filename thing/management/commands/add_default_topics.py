from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from thing.models import Topic


class Command(BaseCommand):
    help = 'Add default topic'

    def handle(self, *args, **options):
        topics = [{
            "short_name": "special_chars",
            "description": "the ability to match on characters like (, [, etc.",
        }, {
            "short_name": "exact_match",
            "description": "the ability to match on an exact sequence of characters, even in the middle of a word",
        }, {
            "short_name": "regex",
            "description": "the ability to use regular expressions to match",
        }, {
            "short_name": "search_branches",
            "description": "the ability to use search for code in branches besides master (possibly including dev branches)",
        }, {
            "short_name": "dependencies",
            "description": "the ability to filter matches based upon what libraries are used in the repo",
        }, {
            "short_name": "boost_definitions",
            "description": "definitions are boosted to appear toward the top of search results, maybe even filter out non-definitions",
        }, {
            "short_name": "more_facets",
            "description": "facet by other things: repos, directory",
        }, {
            "short_name": "deduplicate",
            "description": "deduplicate files that have tons of duplicates in global search (example: search GetObjectRequest)",
        }, {
            "short_name": "boost_filenames",
            "description": "if a filename matches, boost it toward the top",
        }, {
            "short_name": "boost_implementation",
            "description": "business logic should appear above test files, vendored files, config files, etc. - maybe even filter out test files",
        }, {
            "short_name": "case_sensitivity",
            "description": "ability to make case sensitive queries",
        }, {
            "short_name": "already_exists",
            "description": "tweet expresses a need for a feature that already exists, they just were not aware of it",
        }, {
            "short_name": "other",
            "description": "interesting but uncommon request",
        }, {
            "short_name": "forks",
            "description": "search or exclude forks",
        }, {
            "short_name": "unhelpful",
            "description": "unhelpful tweets",
        }, {
            "short_name": "boolean",
            "description": "combine clauses together using boolean logic",
        }, {
            "short_name": "archived",
            "description": "exclude archived repos (possible bug)",
        }]

        for topic in topics:
            try:
                Topic.objects.create(**topic)
            except IntegrityError:
                pass
