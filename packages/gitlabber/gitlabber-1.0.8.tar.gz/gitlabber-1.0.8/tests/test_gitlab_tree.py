# from unittest import TestCase, mock
# from gitlabber import gitlab_tree

# URL="http://url"
# TOKEN="token"

# groups = [{ 'id': '1', 'name': 'test'}]  

# class GitlabTreeTestCase(TestCase):

#     @mock.patch('gitlabber.gitlab_tree.Gitlab')
#     def test_get_tree(self, mock_gitlab):
#         mock_gitlab.groups.return_value = mock.MagicMock()
#         mock_gitlab.groups
        
#         mock_gitlab.groups.return_value.list.return_value = groups
#         gl = gitlab_tree.GitlabTree(URL, TOKEN, includes=[], excludes=[], in_file=None, out_file=None)
#         gl.load_tree()
#         mock_gitlab.groups.list.assert_called()
