
from tempfile import NamedTemporaryFile
from unittest import TestCase

from sqlalchemy.sql.functions import count

from ch2.commands.activities import activities
from ch2.commands.args import bootstrap_file, m, V, DEV, mm, FAST
from ch2.commands.constants import constants
from ch2.config.default import default
from ch2.sql.tables.activity import ActivityJournal
from ch2.sql.tables.pipeline import PipelineType
from ch2.sql.tables.statistic import StatisticJournal, StatisticJournalFloat, StatisticName
from ch2.stats.names import RAW_ELEVATION, ELEVATION, ACTIVE_DISTANCE, ACTIVE_TIME
from ch2.stats.pipeline import run_pipeline


class TestActivities(TestCase):

    def test_activities(self):

        with NamedTemporaryFile() as f:

            args, sys, db = bootstrap_file(f, m(V), '5')

            bootstrap_file(f, m(V), '5', mm(DEV), configurator=default)

            args, sys, db = bootstrap_file(f, m(V), '5', 'constants', 'set', 'FTHR.%', '154')
            constants(args, sys, db)

            args, sys, db = bootstrap_file(f, m(V), '5', 'constants', 'show', 'FTHR.%')
            constants(args, sys, db)

            args, sys, db = bootstrap_file(f, m(V), '5', 'constants', 'set', 'SRTM1.dir',
                                      '/home/andrew/archive/srtm1')
            constants(args, sys, db)

            args, sys, db = bootstrap_file(f, m(V), '5', mm(DEV), 'activities', mm(FAST),
                                      'data/test/source/personal/2018-08-27-rec.fit')
            activities(args, sys, db)

            # run('sqlite3 %s ".dump"' % f.name, shell=True)

            run_pipeline(sys, db, PipelineType.STATISTIC, force=True, start='2018-01-01', n_cpu=1)

            # run('sqlite3 %s ".dump"' % f.name, shell=True)

            with db.session_context() as s:
                n_raw = s.query(count(StatisticJournalFloat.id)). \
                    join(StatisticName). \
                    filter(StatisticName.name == RAW_ELEVATION).scalar()
                self.assertEqual(2099, n_raw)
                n_fix = s.query(count(StatisticJournalFloat.id)). \
                    join(StatisticName). \
                    filter(StatisticName.name == ELEVATION).scalar()
                self.assertEqual(2099, n_fix)
                # WHY does this jump aroud?
                n = s.query(count(StatisticJournal.id)).scalar()
                # self.assertEqual(50403, n)
                self.assertTrue(n > 30000)
                self.assertTrue(n < 100000)
                journal = s.query(ActivityJournal).one()
                self.assertNotEqual(journal.start, journal.finish)

    def test_segment_bug(self):
        with NamedTemporaryFile() as f:
            args, sys, db = bootstrap_file(f, m(V), '5', mm(DEV), configurator=default)
            paths = ['/home/andrew/archive/fit/bike/cotic/2016-07-27-pm-z4.fit']
            run_pipeline(sys, db, PipelineType.ACTIVITY, paths=paths, force=True)

    def __assert_basic_stats(self, s):
        for name in [ACTIVE_DISTANCE, ACTIVE_TIME]:
            stat = s.query(StatisticJournal). \
                join(StatisticName). \
                filter(StatisticName.name == name).one_or_none()
            print(f'{name} = {stat}')
            self.assertTrue(stat, f'No value for {name}')

    def test_florian(self):
        with NamedTemporaryFile() as f:
            bootstrap_file(f, m(V), '5')
            bootstrap_file(f, m(V), '5', mm(DEV), configurator=default)
            args, sys, db = bootstrap_file(f, m(V), '5', mm(DEV),
                                      'activities', mm(FAST),
                                      'data/test/source/private/florian.fit')
            activities(args, sys, db)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            run_pipeline(sys, db, PipelineType.STATISTIC, n_cpu=1)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            with db.session_context() as s:
                self.__assert_basic_stats(s)

    def test_michael(self):
        with NamedTemporaryFile() as f:
            bootstrap_file(f, m(V), '5')
            bootstrap_file(f, m(V), '5', mm(DEV), configurator=default)
            args,sys,  db = bootstrap_file(f, m(V), '5', mm(DEV),
                                      'activities', mm(FAST),
                                      'data/test/source/other/2019-05-09-051352-Running-iWatchSeries3.fit')
            activities(args, sys, db)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            run_pipeline(sys, db, PipelineType.STATISTIC, n_cpu=1)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            with db.session_context() as s:
                self.__assert_basic_stats(s)

    def test_heart_alarms(self):
        with NamedTemporaryFile() as f:
            bootstrap_file(f, m(V), '5')
            bootstrap_file(f, m(V), '5', mm(DEV), configurator=default)
            args, sys, db = bootstrap_file(f, m(V), '5', mm(DEV),
                                      'activities', mm(FAST),
                                      'data/test/source/personal/2016-07-19-mpu-s-z2.fit')
            activities(args, sys, db)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            run_pipeline(sys, db, PipelineType.STATISTIC, n_cpu=1)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            with db.session_context() as s:
                stat = s.query(StatisticJournal). \
                    join(StatisticName). \
                    filter(StatisticName.name == ACTIVE_DISTANCE).one()
                self.assertGreater(stat.value, 30)

    def test_920(self):
        for src in '920xt-2019-05-16_19-42-54.fit', '920xt-2019-05-16_19-42-54.fit':
            with NamedTemporaryFile() as f:
                bootstrap_file(f, m(V), '5')
                bootstrap_file(f, m(V), '5', mm(DEV), configurator=default)
                args, sys, db = bootstrap_file(f, m(V), '5', mm(DEV), 'activities', mm(FAST),
                                               f'data/test/source/other/{src}')
                activities(args, sys, db)
                # run('sqlite3 %s ".dump"' % f.name, shell=True)
                run_pipeline(sys, db, PipelineType.STATISTIC, n_cpu=1)
                # run('sqlite3 %s ".dump"' % f.name, shell=True)
                with db.session_context() as s:
                    self.__assert_basic_stats(s)
