# -*- coding: utf-8 -*-

"""Tests for converting WikiPathways."""

import os
import unittest

from pathme.export_utils import get_paths_in_folder
from pathme.wikipathways.utils import get_file_name_from_url, merge_two_dicts
from tests.constants import WP22, WP_TEST_RESOURCES


class TestUtils(unittest.TestCase):
    """Tests for utils."""

    def test_get_wikipathways_files(self):
        """Test getting WikiPathways files."""
        files = get_paths_in_folder(WP_TEST_RESOURCES)

        self.assertEqual(len(files), 7)
        self.assertEqual(os.path.join(WP_TEST_RESOURCES, WP22), WP22)

    def test_merge_dict(self):
        """Test merging of two dictionaries."""
        dict_1 = {1: 'uno'}
        dict_2 = {2: 'dos'}
        merged_dict = merge_two_dicts(dict_1, dict_2)

        self.assertEqual(merged_dict, {1: 'uno', 2: 'dos'})

    def test_url(self):
        """Test get url."""
        world = get_file_name_from_url('https://hello/world')

        self.assertEqual(world, 'world')
