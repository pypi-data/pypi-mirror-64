
from abc import abstractmethod
from logging import getLogger
from time import time

from ..pipeline import MultiProcPipeline, LoaderMixin
from ... import FatalException
from ...fit.format.read import filtered_records
from ...fit.profile.profile import read_fit
from ...lib.date import to_time
from ...lib.io import modified_file_scans
from ...lib.log import log_current_exception
from ...sql import Timestamp

log = getLogger(__name__)


class AbortImport(Exception):
    pass


class AbortImportButMarkScanned(AbortImport):
    pass


class FitReaderMixin(LoaderMixin):

    def __init__(self, *args, paths=None, **kargs):
        self.paths = paths
        super().__init__(*args, **kargs)

    def _delete(self, s):
        # forcing does two things:
        # first, it by-passes the checks on last-scan date and duplicates
        # second, we delete any overlapping activities on load (when we know the times)
        # (without force, overlapping activities trigger an error)
        pass

    def _missing(self, s):
        return modified_file_scans(s, self.paths, self.owner_out, self.force)

    def _run_one(self, s, file_scan):
        try:
            self._read(s, file_scan)
            file_scan.last_scan = time()
        except AbortImportButMarkScanned as e:
            log.warning(f'Could not process {file_scan} (scanned)')
            # log_current_exception()
            file_scan.last_scan = time()
        except FatalException:
            raise
        except Exception as e:
            log.warning(f'Could not process {file_scan} (ignored)')
            log_current_exception()

    def _read(self, s, file_scan):
        source, data = self._read_data(s, file_scan)
        s.commit()
        with Timestamp(owner=self.owner_out, source=source).on_success(s):
            loader = self._get_loader(s)
            self._load_data(s, loader, data)
            loader.load()
        return loader  # returned so coverage can be accessed

    def _read_fit_file(self, path, *options):
        types, messages, records = filtered_records(read_fit(path))
        return [record.as_dict(*options)
                for _, _, record in sorted(records,
                                           key=lambda r: r[2].timestamp if r[2].timestamp else to_time(0.0))]

    def _first(self, path, records, *names):
        return self.__assert_contained(path, records, names, 0)

    def _last(self, path, records, *names):
        return self.__assert_contained(path, records, names, -1)

    def __assert_contained(self, path, records, names, index):
        try:
            return [record for record in records if record.name in names][index]
        except IndexError:
            log.debug(f'No {names} entry(s) in {path}')
            raise AbortImportButMarkScanned()

    @abstractmethod
    def _read_data(self, s, file_scan):
        raise NotImplementedError()

    @abstractmethod
    def _load_data(self, s, loader, data):
        raise NotImplementedError()


def quote(text):
    return '"' + text + '"'


class MultiProcFitReader(FitReaderMixin, MultiProcPipeline):

    def _args(self, missing, start, finish):
        paths = ' '.join(quote(file_scan.path) for file_scan in missing[start:finish+1])
        log.info(f'Starting worker for {missing[start]} - {missing[finish]}')
        return paths
