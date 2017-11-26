import unittest
from izabela_tyrna import Get_Data

class Test_Log_File(unittest.TestCase):

    def setUp(self):
        self.check = Get_Data() 

    def test(self):
        log = self.check.read_file('changes_python.log')
        r = len(log)
        self.assertEqual(5255, r)
        commits = self.check.get_commits(log)
        self.assertEqual(422, len(commits))
        date = self.check.get_dates(commits['date'])
        commits["date"] = date
        result = len(commits["date"][20])
        self.assertEqual(10,result)
        
if __name__ == '__main__':
    unittest.main()
    
