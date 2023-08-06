"""Test the cinestats.movie module.
"""
import cinestats


class TestMovie:
    def test_init(self):
        """Test basic initialisation of a Movie object."""
        m = cinestats.Movie(title='Foo', date='2017-10-01')

        assert m.title == 'Foo'
        assert m.date == '2017-10-01'


class TestMovieDatabase:
    def test_init(self):
        """Test basic initialisation of a MovieDatabase object."""
        m1 = cinestats.Movie(title='Foo', date='2017-10-01')
        m2 = cinestats.Movie(title='Bar', date='2017-10-02')

        mdb = cinestats.MovieDatabase([m1, m2])

        assert len(mdb) == 2
        assert mdb[0] == m1
        assert mdb[1] == m2

    def test_remove_duplicates(self):
        """Test removing of duplicates."""
        m1 = cinestats.Movie(title='Foo', date='2017-10-01')
        m2 = cinestats.Movie(title='Bar', date='2017-10-02')

        # Create database with duplicate entry.
        mdb = cinestats.MovieDatabase([m1, m2, m2])

        # Aim to remove duplicate.
        mdb.remove_duplicates()

        assert len(mdb) == 2
