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


# Parte I -  Comparação da taxa de bits por codificação

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

# Parte - II Aplicando ruído e atenuação

Nesta etapa, será aplicado ruído e atenuação ao sinal para verificar a taxa de erro de bits na decodificação. 
Será feita a aquisição para recuperação do sinal a partir dos limiares, serão utilizadas as codificações bipolares
NRZ e Manchester, onde o limiar de decisão é 0.

Será aplicado um filtro passa baixa para a redução do ruído e a verificação do limiar da mesma forma.

Os resultados foram salvos nos arquivos:

  - [Results_mean.json](https://github.com/diogo0001/line-coding-script/blob/master/Results_mean.json): 
Com as médias calculadas para 10 interações de diferentes vetores de 16000 bits, variando o SNR de 1 a 45 em cada interação.   
  - [Results.json](https://github.com/diogo0001/line-coding-script/blob/master/Results.json):
  Os resultados brutos adquiridos das interações
  
Também foi feita a verificação dos bits de uma mensagem, variando o SNR de 1 a 15, os resultados estão no arquivo
[Msg_errors.json](https://github.com/diogo0001/line-coding-script/blob/master/Msg_errors.json)


### Teste com codificação Manchester com ruído e SNR = 45

![](https://github.com/diogo0001/line-coding-script/blob/master/images_noise/Manchester_noise.png)

Teste com codificação Manchester com atenuação e ruído  

![](https://github.com/diogo0001/line-coding-script/blob/master/images_noise/Manchester_at_noise.png)

### Com SNR de 6 db e atenuação utilizando a distribuição de Rayleigh:

![](https://github.com/diogo0001/line-coding-script/blob/master/images_noise/BipolarNRZ_6db_snr_noise.png)

Este é o SNR utilizado para calibrar a taxa de bits para a média de 200 erros em um stream de 16000 bits.

### Gráficos da probabilidade de erro x SNR para as codificações com ruído

![](https://github.com/diogo0001/line-coding-script/blob/master/images_noise/SRNxPb%20BipolarNRZ_noise%20.png)

![](https://github.com/diogo0001/line-coding-script/blob/master/images_noise/SRNxPb%20Manchester_noise.png)

Pode-se verificar que houveram erros de transmissão com um SNR inferior à 15 dB, conforme o SNR aumenta
menor é a taxa de erros.

### Gráficos da probabilidade de erro x SNR para as codificações com filtragem

O filtro aplicado é o mostrado a seguir:

![Filtro]()

Os parâmetrod do filtro são:

 Cutoff = 160 Hz
 
 fs = 8000 Hz
 
 Ordem = 6
 
 Os gráficos a seguir mostram que não houveram erros de bits na transmissão:
 
 ![](https://github.com/diogo0001/line-coding-script/blob/master/images_noise/SRNxPb%20BipolarNRZ_filtered%20.png)
 
 ![](https://github.com/diogo0001/line-coding-script/blob/master/images_noise/SRNxPb%20Manchester_filtered%20.png)



