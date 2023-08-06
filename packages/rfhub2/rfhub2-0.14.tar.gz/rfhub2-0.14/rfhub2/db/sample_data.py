from datetime import datetime, timezone
from sqlalchemy.orm.session import Session

from rfhub2.db.base import Collection, Keyword, KeywordStatistics


def recreate_data(session: Session) -> None:
    session.query(Keyword).delete()
    session.query(Collection).delete()
    session.query(KeywordStatistics).delete()
    keywords = [
        Keyword(
            name="Test setup",
            doc="Prepare test environment, use teardown after this one",
        ),
        Keyword(name="Some keyword", doc="Perform some check"),
        Keyword(name="Teardown", doc="Clean up environment"),
    ]
    keywords_2 = [Keyword(name="zzz", doc="zzzzzz")]
    collections = [
        Collection(name="First collection", type="robot", keywords=keywords),
        Collection(name="Second collection", type="Robot", keywords=keywords_2),
        Collection(name="Third", type="Library"),
    ]
    statistics = [
        KeywordStatistics(
            collection="First collection",
            keyword="Test setup",
            execution_time=datetime(2019, 12, 21, 2, 30, 0, tzinfo=timezone.utc),
            times_used=10,
            total_elapsed=1000,
            min_elapsed=10,
            max_elapsed=100,
        ),
        KeywordStatistics(
            collection="First collection",
            keyword="Some keyword",
            execution_time=datetime(2019, 12, 21, 2, 30, 0, tzinfo=timezone.utc),
            times_used=5,
            total_elapsed=3000,
            min_elapsed=300,
            max_elapsed=1500,
        ),
        KeywordStatistics(
            collection="First collection",
            keyword="Some keyword",
            execution_time=datetime(2019, 12, 20, 1, 30, 0, tzinfo=timezone.utc),
            times_used=5,
            total_elapsed=2000,
            min_elapsed=200,
            max_elapsed=1000,
        ),
        KeywordStatistics(
            collection="Second collection",
            keyword="Old keyword",
            execution_time=datetime(2019, 12, 21, 1, 30, 0, tzinfo=timezone.utc),
            times_used=5,
            total_elapsed=2500,
            min_elapsed=200,
            max_elapsed=1000,
        ),
        KeywordStatistics(
            collection="Second collection",
            keyword="Old keyword",
            execution_time=datetime(2019, 12, 21, 2, 30, 0, tzinfo=timezone.utc),
            times_used=5,
            total_elapsed=2500,
            min_elapsed=100,
            max_elapsed=1000,
        ),
        KeywordStatistics(
            collection="Second collection",
            keyword="Old keyword",
            execution_time=datetime(2019, 12, 21, 3, 30, 0, tzinfo=timezone.utc),
            times_used=5,
            total_elapsed=2500,
            min_elapsed=200,
            max_elapsed=1100,
        ),
    ]
    session.add_all(collections)
    session.add_all(statistics)
    session.commit()
