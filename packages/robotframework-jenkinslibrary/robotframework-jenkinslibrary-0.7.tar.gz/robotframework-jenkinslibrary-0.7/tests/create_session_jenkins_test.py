import unittest
from JenkinsLibrary.jenkins_face import JenkinsFace


class createSessionJenkinsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.jenkins = JenkinsFace()

    def test_delete_snapshot_with_delete_key(self):
        self.jenkins.create_session_jenkins()

        self.assertIsNotNone(self._session)

    if __name__ == '__main__':
        unittest.main()
