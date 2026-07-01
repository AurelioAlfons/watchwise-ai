from app.services.tmdb_service import is_kid_appropriate, get_certification_filter


# --- is_kid_appropriate ---

def test_movie_g_rating_is_kid_appropriate():
    assert is_kid_appropriate("movie", "G") is True


def test_movie_pg_rating_is_kid_appropriate():
    assert is_kid_appropriate("movie", "PG") is True


def test_movie_pg13_rating_is_not_kid_appropriate():
    assert is_kid_appropriate("movie", "PG-13") is False


def test_movie_r_rating_is_not_kid_appropriate():
    assert is_kid_appropriate("movie", "R") is False


def test_tv_tvy_rating_is_kid_appropriate():
    assert is_kid_appropriate("tv", "TV-Y") is True


def test_tv_tvpg_rating_is_kid_appropriate():
    assert is_kid_appropriate("tv", "TV-PG") is True


def test_tv_tvma_rating_is_not_kid_appropriate():
    assert is_kid_appropriate("tv", "TV-MA") is False


def test_missing_rating_defaults_to_not_kid_appropriate():
    # Safety-first: no rating data available means we exclude it
    # rather than risk showing unrated content to a kids audience.
    assert is_kid_appropriate("movie", None) is False
    assert is_kid_appropriate("tv", None) is False


def test_missing_rating_empty_string_is_not_kid_appropriate():
    assert is_kid_appropriate("movie", "") is False


# --- get_certification_filter ---

def test_certification_filter_applies_for_kids_movie():
    result = get_certification_filter("kids", "movie")
    assert result == {
        "certification_country": "AU",
        "certification.lte": "PG",
    }


def test_certification_filter_empty_for_non_kids_movie():
    result = get_certification_filter("alone", "movie")
    assert result == {}


def test_certification_filter_empty_for_kids_tv():
    # TV can't be certification-filtered at the /discover level,
    # so this should return no extra params — filtering happens
    # as a post-filter instead, via is_kid_appropriate.
    result = get_certification_filter("kids", "tv")
    assert result == {}


def test_certification_filter_empty_when_watching_with_is_none():
    result = get_certification_filter(None, "movie")
    assert result == {}