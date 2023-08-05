from subprocess import PIPE, Popen as popen
from unittest import TestCase, mock
from gitlabber import gitlab_tree

from gitlabber import __version__ as VERSION
URL="http://url"
TOKEN="token"


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['gitlabber', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('usage:' in str(output))

        output = popen(['gitlabber', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('usage:' in str(output))
