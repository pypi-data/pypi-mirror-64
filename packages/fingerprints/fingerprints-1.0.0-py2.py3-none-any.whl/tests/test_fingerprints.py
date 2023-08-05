from unittest import TestCase

import fingerprints

fp = fingerprints.generate


class FingerprintsTest(TestCase):

    def test_normal_names(self):
        self.assertEqual(fp('Mr. Boaty McBoatface'), 'boaty mcboatface')
        self.assertEqual(fp('Open S.A.R.L.'), 'open sarl')
        self.assertEqual(fp("Johnson's Coffee Shop"), 'coffee johnsons shop')
        self.assertEqual(fp('New York, New York'), 'new york')

    def test_replacers(self):
        self.assertEqual(fp('Foo Limited'), 'foo ltd')
        self.assertEqual(fp('Foo International bla Limited'), 'bla foo intl ltd')  # noqa
        self.assertEqual(fp('Foo International Limited'), 'foo intl ltd')

    def test_cyrillic(self):
        self.assertEqual(fp('РАДИК ІВАН ЛЬВОВИЧ'), 'ivan lvovic radik')
        self.assertEqual(fp('КУШНАРЬОВ ДМИТРО ВІТАЛІЙОВИЧ'), 'dmitro kusnarov vitalijovic')  # noqa
        self.assertEqual(fp('Порошенко Петро Олексійович'), 'oleksijovic petro porosenko')  # noqa

    def test_turcic(self):
        self.assertEqual(fp('FUAD ALIYEV ƏHMƏD OĞLU'), 'ahmad aliyev fuad oglu')  # noqa

    def test_german(self):
        self.assertEqual(fp('Siemens Aktiengesellschaft'), 'ag siemens')  # noqa
        self.assertEqual(fp('Software und- Systemgesellschaft mit beschr Haftung'),  # noqa
                         'gmbh software systemgesellschaft und')  # noqa

    def test_company(self):
        self.assertEqual(fp('S.R.L. "Magic-Arrow" ICS'), 'arrow ics magic srl')  # noqa

    def test_brackets(self):
        self.assertEqual(fp('Foo (Bar) CORPORATION'), 'corp foo')  # noqa

    def test_remove(self):
        rem = fingerprints.remove_types('Siemens Aktiengesellschaft')
        self.assertEqual(rem, 'Siemens')  # noqa
        rem = fingerprints.remove_types('Siemens AG')
        self.assertEqual(rem, 'Siemens')  # noqa
        rem = fingerprints.remove_types('Foo Limited')
        self.assertEqual(rem, 'Foo')
