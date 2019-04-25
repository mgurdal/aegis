from typing import Hashable, Iterable


def match_any(
        required: Iterable[Hashable], provided: Iterable[Hashable]) -> bool:
    required_scopes = set(required)
    provided_scopes = set(provided)

    scopes_matches = required_scopes.intersection(provided_scopes) != set()

    return scopes_matches


def match_exact(
        required: Iterable[Hashable], provided: Iterable[Hashable]) -> bool:
    required_scopes = set(required)
    provided_scopes = set(provided)

    scopes_matches = required_scopes == provided_scopes

    return scopes_matches


def match_all(
        required: Iterable[Hashable], provided: Iterable[Hashable]) -> bool:
    required_scopes = set(required)
    provided_scopes = set(provided)

    scopes_matches = required_scopes.issubset(provided_scopes)

    return scopes_matches
