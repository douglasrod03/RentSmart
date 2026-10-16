# RentSmart - Sistema de Orçamento de Locação

Este é um projeto acadêmico desenvolvido para a disciplina de **Algorithmic Thinking & Introduction to Object-Oriented Programming** da **UniFECAF**. 

O **RentSmart** é uma aplicação desktop desenvolvida em Python para automatizar os orçamentos de locação da imobiliária fictícia *R.M Imóveis*. O sistema calcula os valores mensais de aluguel aplicando regras de negócio específicas para Apartamentos, Casas e Estúdios, além de gerar uma projeção financeira de 12 meses em formato CSV.

## Funcionalidades

* **Cálculo Dinâmico:** Aplica automaticamente adicionais de quartos e garagem, além de descontos por ausência de crianças.
* **Taxa Contratual Separada:** Calcula e exibe o parcelamento da taxa de contrato (R$ 2.000,00) de forma independente do valor do aluguel.
* **Interface Gráfica (GUI):** Interface intuitiva construída com a biblioteca nativa `tkinter`, com validação de dados em tempo real.
* **Exportação de Dados:** Gera um ficheiro `.csv` (`projecao_12_meses.csv`) com a previsão de custos mês a mês para o cliente.

## Tecnologias Utilizadas

* **Python 3**
* **Programação Orientada a Objetos (POO):** Uso de Herança, Polimorfismo e Encapsulamento.
* **Tkinter:** Para a interface gráfica de utilizador.
* **CSV:** Para manipulação e exportação da folha de cálculo.

## Como Executar o Projeto

1. Certifique-se de ter o **Python 3** instalado no seu computador.
2. Clone este repositório ou transfira os ficheiros para a sua máquina.
3. Abra o terminal na pasta do projeto.
4. Execute o seguinte comando:

```bash
python rentsmart_gui.py
