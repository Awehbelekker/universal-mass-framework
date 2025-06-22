import unittest
import os
from core.project_importer import ProjectImporter

class TestProjectImporter(unittest.TestCase):
    def test_import_project(self):
        # Create a temp directory with files
        os.makedirs('temp_project/subdir', exist_ok=True)
        with open('temp_project/file1.txt', 'w') as f:
            f.write('test')
        with open('temp_project/subdir/file2.txt', 'w') as f:
            f.write('test2')
        importer = ProjectImporter('.')
        data = importer.import_project('temp_project')
        
        # Normalize paths for cross-platform compatibility
        file_paths = [path.replace('\\', '/') for path in data['files']]
        folder_paths = [path.replace('\\', '/') for path in data['folders']]
        
        self.assertIn('temp_project/file1.txt', file_paths)
        self.assertIn('temp_project/subdir', folder_paths)
        # Cleanup
        os.remove('temp_project/file1.txt')
        os.remove('temp_project/subdir/file2.txt')
        os.rmdir('temp_project/subdir')
        os.rmdir('temp_project')

if __name__ == "__main__":
    unittest.main()
