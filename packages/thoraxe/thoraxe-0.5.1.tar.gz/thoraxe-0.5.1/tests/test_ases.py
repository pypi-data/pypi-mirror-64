import os
import pytest
import pandas as pd
import networkx as nx
from thoraxe import subexons


@pytest.fixture(scope='module')
def mapk8(request):
    filename = request.module.__file__
    test_dir = os.path.dirname(filename)
    data_dir = os.path.join(test_dir, 'data')
    mapk8_dir = os.path.join(data_dir, 'MAPK8_output', 'thoraxe')
    return {
        'splice_graph': os.path.join(mapk8_dir, 'splice_graph.gml'),
        's_exon_table': os.path.join(mapk8_dir, 's_exon_table.csv'),
        'ases_table': os.path.join(mapk8_dir, 'ases_table.csv'),
        'path_table': os.path.join(mapk8_dir, 'path_table.csv')
    }


def test_ases(mapk8):
    s_exon_df = pd.read_csv(mapk8['s_exon_table'])
    graph = nx.read_gml(mapk8['splice_graph'])
    trx_df = subexons.ases.get_transcript_scores(s_exon_df, graph)
    path_table, ases_df = subexons.ases.conserved_ases(s_exon_df,
                                                       mapk8['splice_graph'])

    assert all(trx_df == path_table)

    assert 'IsHuman' not in trx_df.columns

    select = trx_df.Path == 'start/8_0/1_0/14_0/2_0/4_0/4_1/stop'
    assert all(trx_df.PathGeneNumber[select] == 1)
    assert all(trx_df.MinimumTranscriptWeightedConservation[select] ==
               0.03333333333333333)

    assert list(trx_df.PathGeneNumber) == sorted(trx_df.PathGeneNumber,
                                                 reverse=True)
    assert list(ases_df.AlternativePathGeneNumber) == sorted(
        ases_df.AlternativePathGeneNumber, reverse=True)

    data_path_table = pd.read_csv(mapk8['path_table'])
    data_ases_table = pd.read_csv(mapk8['ases_table'])
    assert sorted(path_table.columns) == sorted(data_path_table.columns)
    assert sorted(ases_df.columns) == sorted(data_ases_table.columns)
    assert path_table.size == data_path_table.size
    assert ases_df.shape[0] == data_ases_table.shape[0]
    for col in [
            'GeneID', 'TranscriptIDCluster', 'TranscriptLength', 'Path',
            'PathGeneNumber'
    ]:
        assert all(path_table[col].values == data_path_table[col].values)
    for col in [
            'CanonicalPath', 'AlternativePath', 'ASE',
            'CanonicalPathGeneNumber', 'CanonicalPathGenes',
            'AlternativePathGeneNumber', 'AlternativePathGenes'
    ]:
        assert all(ases_df[col].values == data_ases_table[col].values)
