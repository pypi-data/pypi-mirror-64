from .loader import BrukerLoader
import os
import tqdm
import pickle
import zipfile
import datetime
bar_fmt = '{l_bar}{bar:20}{r_bar}{bar:-20b}'


class NamedTuple(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class BackupCache:
    def __init__(self):
        self._init_dataset_class()

    def logging(self, message, method):
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_data.append(NamedTuple(datetime=now, method=method, message=message))

    @property
    def num_raw(self):
        return len(self.raw_data)

    @property
    def num_bck(self):
        return len(self.bck_data)

    def _init_dataset_class(self):
        # dataset
        self.raw_data = []
        self.bck_data = []
        self.log_data = []

    def get_rpath_obj(self, raw_path):
        if len(self.raw_data):
            rpath_obj = [r for r in self.raw_data if r.path == raw_path]
            if len(rpath_obj):
                return rpath_obj[0]
            else:
                return None
        else:
            return None

    def get_bpath_obj(self, path, by_raw=False):
        if len(self.bck_data):
            if by_raw:
                rpath_obj = self.get_rpath_obj(path)
                if rpath_obj is None:
                    return []
                else:
                    return [b for b in self.bck_data if b.data_pid == rpath_obj.data_pid]
            else:
                data_pid = [b for b in self.bck_data if b.path == path][0].data_pid
                return [b for b in self.bck_data if b.data_pid == data_pid]
        else:
            return []

    def isin(self, path, raw=True):
        if raw:
            list_data = self.raw_data
        else:
            list_data = self.bck_data
        _history = [d for d in list_data if d.path == path]
        if len(_history):
            return True
        else:
            return False

    def set_raw(self, dir_path, removed=False):
        if not self.isin(dir_path, raw=True):  # continue if the path is not saved in this cache obj
            if os.path.isdir(dir_path):
                raw = BrukerLoader(dir_path)
                garbage = False if raw.is_pvdataset else True
                rawobj = NamedTuple(data_pid=self.num_raw,
                                    path=dir_path,
                                    garbage=garbage,
                                    removed=removed,
                                    backup=False)
                self.raw_data.append(rawobj)
            else:
                if removed:
                    rawobj = NamedTuple(data_pid=self.num_raw,
                                        path=dir_path,
                                        garbage=None,
                                        removed=removed, backup=True)
                    self.raw_data.append(rawobj)
                else:
                    self.logging('{} is not directory. [raw dataset must be a directory]'.format(dir_path),
                                 'set_raw')

    def set_bck(self, file_path):
        if not self.isin(file_path, raw=False):  # continue if the path is not saved in this cache obj
            issued = False
            try:
                bck = BrukerLoader(file_path)
                raw_path = bck.pvobj.path
                garbage = False if bck.is_pvdataset else True
                crashed = False
            except zipfile.BadZipFile:
                self.logging('{} is crashed.'.format(file_path),
                             'set_bck')
                bck = None
                raw_path = None
                garbage = True
                crashed = True
            rpath_obj = self.get_rpath_obj(raw_path)
            if rpath_obj is None:
                self.set_raw(raw_path, removed=True)
                rpath_obj = self.get_rpath_obj(raw_path)
                rpath_obj.garbage = garbage
                if crashed:
                    issued = True
            else:
                if bck is None:
                    issued = True
                else:
                    raw = BrukerLoader(raw_path)
                    if raw.num_recos != bck.num_recos:
                        issued = True
            bckobj = NamedTuple(data_pid=self.num_bck, path=file_path, garbage=garbage,
                                crashed=crashed, issued=issued)
            if not crashed:
                rpath_obj.backup = True
            self.bck_data.append(bckobj)

    def is_duplicated(self, file_path):
        if not self.isin(file_path, raw=False):
            if len(self.get_bpath_obj(file_path, by_raw=False)):
                return True
            else:
                return False
        else:
            # file_path has been registered into the cache
            return None


class BackupCacheHandler:
    def __init__(self, raw_path, backup_path, fname='.brk-backup_cache'):
        """ Handler class for backup data

        Args:
            raw_path:       path for raw dataset
            backup_path:    path for backup dataset
            fname:          file name to pickle cache data
        """
        self._cache = None
        self._rpath = os.path.expanduser(raw_path)
        self._bpath = os.path.expanduser(backup_path)
        self._cache_path = os.path.join(self._bpath, fname)
        self._load_pickle()
        self._parse_info()

    def _load_pickle(self):
        if os.path.exists(self._cache_path):
            try:
                with open(self._cache_path, 'rb') as cache:
                    self._cache = pickle.load(cache)
            except EOFError:
                os.remove(self._cache_path)
                self._cache = BackupCache()
        else:
            self._cache = BackupCache()
        self._save_pickle()

    def _save_pickle(self):
        with open(self._cache_path, 'wb') as f:
            pickle.dump(self._cache, f)

    def logging(self, message, method):
        method = 'Handler.{}'.format(method)
        self._cache.logging(message, method)

    @property
    def get_rpath_obj(self):
        return self._cache.get_rpath_obj

    @property
    def get_bpath_obj(self):
        return self._cache.get_bpath_obj

    @property
    def bck_data(self):
        return self._cache.bck_data

    @property
    def raw_data(self):
        return self._cache.raw_data

    def _parse_info(self):
        print('\n-- Parsing data information from folders --')
        list_of_raw = sorted([d for d in os.listdir(self._rpath) if
                              os.path.isdir(os.path.join(self._rpath, d))])
        list_of_brk = sorted([d for d in os.listdir(self._bpath) if
                              (os.path.isfile(os.path.join(self._bpath, d)) and
                               (d.endswith('zip') or d.endswith('PvDatasets')))])

        # parse dataset
        print('\nScanning raw dataset and update cache...')
        for r in tqdm.tqdm(list_of_raw, bar_format=bar_fmt):
            dir_path = os.path.abspath(os.path.join(self._rpath, r))
            self._cache.set_raw(dir_path)
        self._save_pickle()

        print('\nScanning backup dataset and update cache...')
        for b in tqdm.tqdm(list_of_brk, bar_format=bar_fmt):
            file_path = os.path.abspath(os.path.join(self._bpath, b))
            self._cache.set_bck(file_path)
        self._save_pickle()

        # update raw dataset information
        print('\nScanning raw dataset cache...')
        for r in tqdm.tqdm(self.raw_data, bar_format=bar_fmt):
            if not os.path.exists(r.path):
                if not r.removed:
                    r.removed = True
        self._save_pickle()

        print('Reviewing backup dataset cache...')
        for b in tqdm.tqdm(self.bck_data[:], bar_format=bar_fmt):
            if not os.path.exists(b.path):
                self.bck_data.remove(b)
        self._save_pickle()

    def get_duplicated(self):
        pass

    def get_crashed(self):
        pass

    def get_incompleted(self):
        pass

    def get_completed(self):
        pass
