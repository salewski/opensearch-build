import os
import unittest
from unittest.mock import MagicMock, call, patch

from sign_workflow.signer import Signer


class TestSigner(unittest.TestCase):
    @patch("sign_workflow.signer.GitRepository")
    def test_accepted_file_types_asc(self, git_repo):
        artifacts = [
            "bad-xml.xml",
            "the-jar.jar",
            "the-zip.zip",
            "the-war.war",
            "the-pom.pom",
            "the-module.module",
            "the-tar.tar.gz",
            "random-file.txt",
            "something-1.0.0.0.jar",
        ]
        expected = [
            call(os.path.join("path", "the-jar.jar"), ".asc"),
            call(os.path.join("path", "the-zip.zip"), ".asc"),
            call(os.path.join("path", "the-war.war"), ".asc"),
            call(os.path.join("path", "the-pom.pom"), ".asc"),
            call(os.path.join("path", "the-module.module"), ".asc"),
            call(os.path.join("path", "the-tar.tar.gz"), ".asc"),
            call(os.path.join("path", "something-1.0.0.0.jar"), ".asc"),
        ]
        signer = Signer()
        signer.sign = MagicMock()
        signer.sign_artifacts(artifacts, "path", ".asc")
        self.assertEqual(signer.sign.call_args_list, expected)

    @patch("sign_workflow.signer.GitRepository")
    def test_accepted_file_types_sig(self, git_repo):
        artifacts = [
            "bad-xml.xml",
            "the-jar.jar",
            "the-zip.zip",
            "the-war.war",
            "the-pom.pom",
            "the-module.module",
            "the-tar.tar.gz",
            "random-file.txt",
            "something-1.0.0.0.jar",
        ]
        expected = [
            call(os.path.join("path", "the-jar.jar"), ".sig"),
            call(os.path.join("path", "the-zip.zip"), ".sig"),
            call(os.path.join("path", "the-war.war"), ".sig"),
            call(os.path.join("path", "the-pom.pom"), ".sig"),
            call(os.path.join("path", "the-module.module"), ".sig"),
            call(os.path.join("path", "the-tar.tar.gz"), ".sig"),
            call(os.path.join("path", "something-1.0.0.0.jar"), ".sig"),
        ]
        signer = Signer()
        signer.sign = MagicMock()
        signer.sign_artifacts(artifacts, "path", ".sig")
        self.assertEqual(signer.sign.call_args_list, expected)

    @patch(
        "sign_workflow.signer.Signer.get_repo_url",
        return_value="https://github.com/opensearch-project/.github",
    )
    @patch("sign_workflow.signer.GitRepository.execute")
    def test_signer_checks_out_tool(self, mock_execute, mock_signer):
        Signer()
        self.assertEqual(mock_execute.call_count, 2)
        mock_execute.assert_has_calls([call("./bootstrap"), call("rm config.cfg")])

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_verify_asc(self, mock_repo):
        signer = Signer()
        signer.verify("/path/the-jar.jar.asc")
        mock_repo.assert_has_calls([call().execute("gpg --verify-files /path/the-jar.jar.asc")])

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_verify_sig(self, mock_repo):
        signer = Signer()
        signer.verify("/path/the-jar.jar.sig")
        mock_repo.assert_has_calls([call().execute("gpg --verify-files /path/the-jar.jar.sig")])

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_sign_asc(self, mock_repo):
        signer = Signer()
        signer.sign("/path/the-jar.jar", ".asc")
        mock_repo.assert_has_calls([call().execute("./opensearch-signer-client -i /path/the-jar.jar -o /path/the-jar.jar.asc -p pgp")])

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_sign_sig(self, mock_repo):
        signer = Signer()
        signer.sign("/path/the-jar.jar", ".sig")
        mock_repo.assert_has_calls([call().execute("./opensearch-signer-client -i /path/the-jar.jar -o /path/the-jar.jar.sig -p pgp")])
