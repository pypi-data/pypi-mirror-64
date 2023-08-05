import unittest
import torch
from pytorch_metric_learning.miners import HDCMiner
from pytorch_metric_learning.utils import common_functions as c_f

class TestHDCMiner(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.dist_miner = HDCMiner(filter_percentage=0.3, use_similarity=False, normalize_embeddings=False)
        self.normalized_dist_miner = HDCMiner(filter_percentage=0.3, use_similarity=False, normalize_embeddings=True)
        self.normalized_dist_miner_squared = HDCMiner(filter_percentage=0.3, use_similarity=False, normalize_embeddings=True, squared_distances=True)
        self.sim_miner = HDCMiner(filter_percentage=0.3, use_similarity=True, normalize_embeddings=True)
        self.labels = torch.LongTensor([0, 0, 1, 1, 1, 0])
        correct_a1 = torch.LongTensor([0, 5, 1, 5])
        correct_p = torch.LongTensor([5, 0, 5, 1])
        self.correct_pos_pairs = torch.stack([correct_a1, correct_p], dim=1)
        correct_a2 = torch.LongTensor([1, 2, 4, 5, 0, 2])
        correct_n = torch.LongTensor([2, 1, 5, 4, 2, 0])
        self.correct_neg_pairs = torch.stack([correct_a2, correct_n], dim=1)

    def test_dist_mining(self):
        embeddings = torch.arange(6).float().unsqueeze(1)
        a1, p, a2, n = self.dist_miner(embeddings, self.labels)
        pos_pairs = torch.stack([a1, p], dim=1)
        neg_pairs = torch.stack([a2, n], dim=1)
        self.helper(pos_pairs, neg_pairs)

    def test_normalized_dist_mining(self):
        angles = [0, 20, 40, 60, 80, 100]
        embeddings = torch.FloatTensor([c_f.angle_to_coord(a) for a in angles])
        a1, p, a2, n = self.normalized_dist_miner(embeddings, self.labels)
        pos_pairs = torch.stack([a1, p], dim=1)
        neg_pairs = torch.stack([a2, n], dim=1)
        self.helper(pos_pairs, neg_pairs)

    def test_normalized_dist_squared_mining(self):
        angles = [0, 20, 40, 60, 80, 100]
        embeddings = torch.FloatTensor([c_f.angle_to_coord(a) for a in angles])
        a1, p, a2, n = self.normalized_dist_miner_squared(embeddings, self.labels)
        pos_pairs = torch.stack([a1, p], dim=1)
        neg_pairs = torch.stack([a2, n], dim=1)
        self.helper(pos_pairs, neg_pairs)

    def test_sim_mining(self):
        angles = [0, 20, 40, 60, 80, 100]
        embeddings = torch.FloatTensor([c_f.angle_to_coord(a) for a in angles])
        a1, p, a2, n = self.sim_miner(embeddings, self.labels)
        pos_pairs = torch.stack([a1, p], dim=1)
        neg_pairs = torch.stack([a2, n], dim=1)
        self.helper(pos_pairs, neg_pairs)

    def helper(self, pos_pairs, neg_pairs):
        self.assertTrue(len(pos_pairs) == 4)
        self.assertTrue(len(neg_pairs) == 6) 

        diffs = pos_pairs[:,0] - pos_pairs[:,1]
        correct_diffs = self.correct_pos_pairs[:,0] - self.correct_pos_pairs[:,1]
        self.assertTrue(torch.equal(torch.abs(diffs), torch.abs(correct_diffs)))

        diffs = neg_pairs[:,0] - neg_pairs[:,1]
        correct_diffs = self.correct_neg_pairs[:,0] - self.correct_neg_pairs[:,1]
        self.assertTrue(torch.equal(torch.abs(diffs), torch.abs(correct_diffs)))

    def test_empty_output(self):
        batch_size = 32
        embeddings = torch.randn(batch_size, 64)
        labels = torch.arange(batch_size)
        for miner in [self.dist_miner, self.normalized_dist_miner, self.normalized_dist_miner_squared, self.sim_miner]:
            a1, p, _, _ = miner(embeddings, labels)
            self.assertTrue(len(a1)==0)
            self.assertTrue(len(p)==0)


if __name__ == '__main__':
    unittest.main()