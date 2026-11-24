from collections import Counter
import csv
from pathlib import Path

root = Path(__file__).resolve().parents[1]

def rows(path):
    with (root / path).open(encoding='utf-8', newline='') as file:
        return list(csv.DictReader(file))

flow = {row['etapa']: int(row['n']) for row in rows('resultados/fluxo_rsl.csv')}
assert flow['identificados'] - flow['remocao_periodo'] - flow['duplicatas'] == flow['triados']
assert flow['triados'] - flow['excluidos_triagem'] == flow['buscados']
assert flow['buscados'] - flow['nao_recuperados'] == flow['consultados']
assert flow['consultados'] - flow['excluidos_conteudo'] == flow['incluidos']
matrix = rows('metodo/matriz.csv')
assert len(matrix) == 900
assert len({row['id_estudo'] for row in matrix}) == flow['incluidos']
quality = Counter(row['id_estudo'] for row in matrix if row['julgamento_qualidade'])
assert len(quality) == 33 and set(quality.values()) == {10}, quality
print('Fluxo, matriz e julgamentos qualitativos conferidos.')
