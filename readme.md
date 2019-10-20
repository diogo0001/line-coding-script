# Script para testes de codificações de linha

## Autor: Diogo Tavares

## Github: https://github.com/diogo0001/line-coding-script

## Dependências

- Python 3
- numpy
- matplotlib
- scipy

Executar o arquivo lineCodeScript.py.

### Parte I

Primeiramente, será feito a implementação das funções e os gráficos das codificações UnipolarRZ, UnipolarNRZ,
BipolarRZ, BipolarNRZ, PolarQuaternárioNRZ, NRZ-S, Manchester, 2BQ1,HDB3. Será comparada a taxa de transmissão
de bits em de cada uma.

### Parte III

Posteriormente, será adicionado ruído ao sinal (variando o SNR de 1 a 45) e atenuação, para simular um ambiente real.
Será feita a decodificação do sinal, diretamente e utilizando um filtro PB, comparando o sinal obtido com o enviado,
e detectando a taxa de erro de cada transmissão. As codificações para esta comaração serão as que não passam por zero e
possuem 2 amplitudes, a BipolarNRZ e Manchester.
