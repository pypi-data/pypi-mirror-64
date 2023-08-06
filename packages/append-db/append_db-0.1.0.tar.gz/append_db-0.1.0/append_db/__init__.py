import logging
import os
import tempfile
import unittest

__version__ = "0.1.0"

logger = logging.getLogger(__name__)


class AppendDbV1:
    def __init__(self, path):
        _mkdir(path)
        self.path = path
        self.fp_index = open(_jp(path, "index.i64"), "a+b")
        self.fp_data = open(_jp(path, "data.txt"), "a+b")

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.path)})"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp_index.close()
        self.fp_data.close()

    def __len__(self):
        s = os.fstat(self.fp_index.fileno()).st_size
        if s % 8 != 0:
            logger.warning("Incompletely written index for %s with %s B.", self.path, s)
        return s // 8

    def __getitem__(self, i: int):
        i = range(len(self))[i]
        ib1, ib2 = self._ib1_of(i), self._ib2_of(i)
        self.fp_data.seek(ib1)
        return self.fp_data.read(ib2 - ib1).decode("utf-8")

    def append(self, t: str):
        b = t.encode("utf-8")
        l = len(self)
        ib1 = self._ib1_of(l)
        self.fp_data.seek(ib1)
        dib = self.fp_data.write(b)
        self.fp_index.seek(l * 8)
        try:
            self.fp_index.write(self._bytes(ib1 + dib))
        except OSError:
            self.fp_index.truncate(l * 8)
            raise
        self.flush()

    def flush(self):
        self.fp_data.flush()
        self.fp_index.flush()

    def _ib1_of(self, i):
        return 0 if i == 0 else self._ib_of(i - 1)

    def _ib2_of(self, i):
        return self._ib_of(i)

    def _ib_of(self, i):
        self.fp_index.seek(i * 8)
        return self._int(self.fp_index.read(8))

    @staticmethod
    def _bytes(i: int):
        return i.to_bytes(8, "little", signed=False)

    @staticmethod
    def _int(b: bytes):
        return int.from_bytes(b, "little", signed=False)


def _mkdir(path):
    os.makedirs(path, exist_ok=True)


def _jp(path, *more):
    return os.path.normpath(os.path.sep.join((path, os.path.sep.join(more))))


class _Tester(unittest.TestCase):
    def test_1(self):
        def assert_err(fn, es):
            got_error = False
            try:
                fn()
            except es:
                got_error = True
            assert got_error, fn

        with tempfile.TemporaryDirectory() as td:
            with AppendDbV1(_jp(td, "l1")) as ad:
                self.assertEqual(len(ad), 0)
                with self.assertRaises(IndexError):
                    ad[0]
                with self.assertRaises(IndexError):
                    ad[-1]
                ad.append("どうだろう？\n")
                with self.assertRaises(IndexError):
                    ad[-2]
                with self.assertRaises(IndexError):
                    ad[1]
                self.assertEqual(len(ad), 1)
                self.assertEqual(ad[0], "どうだろう？\n")
                self.assertEqual(ad[-1], "どうだろう？\n")
                ad.append("もう1つ\n")
                self.assertEqual(len(ad), 2)
                self.assertEqual(ad[0], "どうだろう？\n")
                self.assertEqual(ad[-1], "もう1つ\n")
                self.assertEqual(ad[1], "もう1つ\n")
                with self.assertRaises(IndexError):
                    ad[-3]
                with self.assertRaises(IndexError):
                    ad[2]
            with AppendDbV1(_jp(td, "l1")) as ad:
                self.assertEqual(len(ad), 2)
                self.assertEqual(ad[1], "もう1つ\n")
                self.assertEqual(ad[0], "どうだろう？\n")
                ad.append("OK??\n")
                self.assertEqual(ad[2], "OK??\n")


if __name__ == "__main__":
    unittest.main()
