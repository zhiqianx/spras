import filecmp
from pathlib import Path

import pandas as pd
import src.analysis.ml.ml as ml

INPUT_DIR = 'test/ml/input/'
OUT_DIR = 'test/ml/output/'
EXPECT_DIR = 'test/ml/expected/'


class TestML:
    @classmethod
    def setup_class(cls):
        """
        Create the expected output directory
        """
        Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

        

    def test_summarize_networks(self):
        dataframe = ml.summarize_networks([INPUT_DIR + 'test-s1/s1.txt', INPUT_DIR + 'test-s2/s2.txt', INPUT_DIR + 'test-s3/s3.txt',
                                           INPUT_DIR + 'test-longName/longName.txt', INPUT_DIR + 'test-longName2/test-longName2.txt',
                                           INPUT_DIR + 'test-empty/empty.txt'])
        dataframe.to_csv(OUT_DIR + 'dataframe.csv')
        assert filecmp.cmp(OUT_DIR + 'dataframe.csv', EXPECT_DIR + 'expected_df.csv')

    def test_pca(self):
        dataframe = ml.summarize_networks([INPUT_DIR + 'test-s1/s1.txt', INPUT_DIR + 'test-s2/s2.txt', INPUT_DIR + 'test-s3/s3.txt'])
        ml.pca(dataframe, OUT_DIR + 'pca.png', OUT_DIR + 'pca-components.txt',
               OUT_DIR + 'pca-coordinates.csv')
        coord = pd.read_table(OUT_DIR + 'pca-coordinates.csv')
        coord = coord.round(5)  # round values to 5 digits to account for numeric differences across machines
        expected = pd.read_table(EXPECT_DIR + 'expected_coords.csv')
        expected = expected.round(5)

        assert coord.equals(expected)

    def test_hac(self):
        dataframe = ml.summarize_networks([INPUT_DIR + 'test-s1/s1.txt', INPUT_DIR + 'test-s2/s2.txt', INPUT_DIR + 'test-s3/s3.txt'])
        ml.hac(dataframe, OUT_DIR + 'hac.png', OUT_DIR + 'hac-clusters.txt')

        assert filecmp.cmp(OUT_DIR + 'hac-clusters.txt', EXPECT_DIR + 'expected_clusters.txt')
