# 🚀 Data Logger IoT - Monitoramento Ambiental

Este projeto implementa um **dispositivo de registro de dados (data logger)** voltado para o **monitoramento de condições ambientais** em espaços controlados, como salas, estufas ou ambientes sensíveis. O sistema realiza o monitoramento de **temperatura**, **umidade relativa do ar** e **luminosidade** em tempo real, e utiliza o conceito de **Internet das Coisas (IoT)** para coletar, armazenar e transmitir os dados.

## Características Principais

- **Sensores de Temperatura e Umidade**: DHT-11
- **Sensor de Luminosidade**: LDR (Light Dependent Resistor)
- **Microcontrolador**: ESP32 Doit DEVKIT V1
- **Plataforma de Backend**: FIWARE Descomplicado
- **Armazenamento**: MongoDB via STH-Comet
- **Relógio de Tempo Real**: Timestamp gerado pelo Orion Context Broker
- **Interface de Usuário**: Dashboard em Python
- **LED Azul**: Indicador visual, acionado quando os valores de temperatura, umidade ou luminosidade saem da faixa predefinida.

## 🛠️ Especificações Técnicas

- **Microcontrolador**: ESP32 Doit DEVKIT V1
  - Chip ESP32, com conectividade Wi-Fi e Bluetooth.
  - Usado para ler os sensores e enviar os dados ao servidor via Wi-Fi.

- **Sensores**:
  - **DHT-11**: Sensor de temperatura e umidade, com faixa de temperatura de 0 a 50°C e umidade de 20% a 90%.
  - **LDR**: Sensor de luminosidade para medir a intensidade da luz ambiente.

- **Backend e Armazenamento**:
  - **FIWARE Descomplicado**: Plataforma para integração de dispositivos IoT.
  - **STH-Comet**: Armazenamento de dados no MongoDB via Serviço de Histórico (STH).
  
- **Interface de Usuário**:
  - **Dashboard em Python**: Interface gráfica para monitoramento em tempo real dos dados.
  
- **Relógio de Tempo Real**:
  - O timestamp dos dados coletados é gerado pelo **Orion Context Broker**.

## Gatilhos e Níveis de Alerta

O sistema está configurado para acionar um **LED Azul** no ESP32 quando os valores dos sensores saírem dos seguintes limites predefinidos:

- **Temperatura**: 15°C < t < 25°C
- **Luminosidade**: 0 < l < 30%
- **Umidade**: 30% < u < 50%

Caso algum valor medido ultrapasse os limites estabelecidos, o LED Azul será acionado, sinalizando que os parâmetros ambientais estão fora da faixa ideal.

## Lista de Materiais

- **ESP32 Doit DEVKIT V1**: Microcontrolador com Wi-Fi e Bluetooth.
- **DHT-11**: Sensor de temperatura e umidade.
- **LDR**: Sensor de luminosidade.
- **Resistor de 10kΩ**: Para o sensor LDR.
- **Protoboard**: Para prototipagem.
- **Jumpers**: Para conectar os componentes.
- **LED Azul**: Indicador visual.
- **Resistores**: Para configurar o LED e os sensores.

## ⚡ Diagrama Elétrico:

![Diagrama Elétrico]()

## Fluxo de Funcionamento

1. **Leitura dos Sensores**:
   - O **DHT-11** lê os valores de temperatura e umidade.
   - O **LDR** lê os valores de luminosidade no ambiente.
   
2. **Processamento no ESP32**:
   - O ESP32 coleta os dados dos sensores periodicamente e processa os valores.

3. **Envio para o Backend**:
   - Os dados são enviados via Wi-Fi para a plataforma **FIWARE Descomplicado**.
   - Os dados são armazenados no banco de dados **MongoDB** via **STH-Comet**.

4. **Monitoramento e Notificação**:
   - O **Orion Context Broker** gera timestamps para cada dado coletado.
   - A **dashboard em Python** permite visualizar os dados em tempo real.
   - Se algum valor de temperatura, umidade ou luminosidade ultrapassar os limites estabelecidos, o **LED Azul** será acionado como um alerta visual.

## Como Configurar

### 1. Conectar os Sensores ao ESP32

- Conecte o **DHT-11** ao pino 4 do ESP32 (pino de dados).
- Conecte o **LDR** ao pino analógico do ESP32 (pino A0, por exemplo).
- Conecte o **LED Azul** ao pino digital do ESP32 (pino D2, por exemplo).

### 2. Configuração do Backend

- Crie uma instância do **FIWARE Descomplicado** para gerenciar os dados.
- Configure o backend para armazenar os dados no banco de dados **MongoDB**, utilizando **STH-Comet**.
- Configure o **Orion Context Broker** para gerar os timestamps dos dados coletados.

### 3. Configuração da Interface de Usuário

- Instale e configure a **dashboard em Python**. Ela se conectará ao backend para exibir os dados de forma gráfica em tempo real.
  
### 4. Rodar o Sistema

- Após conectar o hardware e configurar o backend, o dispositivo começará a coletar dados dos sensores. O LED Azul será acionado sempre que algum parâmetro estiver fora da faixa ideal, e os dados serão enviados e exibidos em tempo real na dashboard.

---

## 🤝 Integrantes do Projeto:

- Enzo Brito Alves de Oliveira - RA: 082220040;
- Erikson Vieira Queiroz - RA: 082220021;
- Guilherme Alves Barbosa - RA: 082220014;
- Heitor Santos Ferreira - RA: 081230042;
- Tainara do Nascimento Casimiro - RA: 082220011;
- William Santim - RA: 082220033

## 🎥 Vídeo Demonstrativo:

- Link: 
