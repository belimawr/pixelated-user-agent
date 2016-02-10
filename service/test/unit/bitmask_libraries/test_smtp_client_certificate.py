#
# Copyright (c) 2016 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
import os
import unittest
import tempdir
from pixelated.bitmask_libraries import session
from leap.srp_session import SRPSession
from mockito import mock, unstub, when, verify, never, any as ANY

from pixelated.bitmask_libraries.session import SmtpClientCertificate


class TestSmtpClientCertificate(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempdir.TempDir()
        self.provider = mock()
        self.provider.domain = 'some-provider.tld'
        self.auth = SRPSession('username', 'token', 'uuid', 'session_id')
        self.pem_path = os.path.join(self.tmp_dir.name, 'providers', 'some-provider.tld', 'keys', 'client', 'smtp.pem')

    def tearDown(self):
        self.tmp_dir.dissolve()
        unstub()

    def test_download_certificate(self):
        downloader = mock()
        when(session).SmtpCertDownloader(self.provider, self.auth).thenReturn(downloader)

        cert = SmtpClientCertificate(self.provider, self.auth, self.tmp_dir.name)
        result = cert.cert_path()

        self.assertEqual(self.pem_path, result)
        verify(downloader).download_to(self.pem_path)

    def test_skip_download_if_already_downloaded(self):

        downloader = mock()
        when(session).SmtpCertDownloader(self.provider, self.auth).thenReturn(downloader)
        when(os.path).exists(self.pem_path).thenReturn(True)

        cert = SmtpClientCertificate(self.provider, self.auth, self.tmp_dir.name)
        result = cert.cert_path()

        self.assertEqual(self.pem_path, result)
        verify(downloader, never).download_to(ANY())
