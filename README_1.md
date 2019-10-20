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

# Parte I - Comparação da taxa de bits por codificação

![](https://github.com/diogo0001/line-coding-script/blob/master/images/bitsRate.png)

As codificaçõs Polar-Quaternário-NRZ e 2B1Q apresentam uma maior taxa de transmissão devido ao fato de transmitirem mais níveis de amplitude, e podem transmitir 2 bits por nível de amplitude.

### Formas de pulso por codificação

![](https://github.com/diogo0001/line-coding-script/blob/master/images/Unipolar%20RZ.png)

![](https://github.com/diogo0001/line-coding-script/blob/master/images/Unipolar%20NRZ.png)

![](https://github.com/diogo0001/line-coding-script/blob/master/images/NRZ%20Space.png)

![](https://github.com/diogo0001/line-coding-script/blob/master/images/Manchester.png)

![](https://github.com/diogo0001/line-coding-script/blob/master/images/HDB3.png)

![](https://github.com/diogo0001/line-coding-script/blob/master/images/Bipolar%20RZ.png)

![](https://github.com/diogo0001/line-coding-script/blob/master/images/Bipolar%20NRZ.png)

![](https://github.com/diogo0001/line-coding-script/blob/master/images/Polar%20Quatern%20NRZ.png)

![](https://github.com/diogo0001/line-coding-script/blob/master/images/2B1Q.png)