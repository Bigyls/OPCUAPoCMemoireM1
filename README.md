# OPCUAPoCMemoireM1
Poc OPC UA pour le mémoire technique

## Installation

```shell
git clone https://github.com/Bigyls/OPCUAPoCMemoireM1.git
cd OPCUAPoCMemoireM1
```

```shell
sudo apt install python3-tk
sudo apt-get install python3-pil python3-pil.imagetk
```

```shell
cd GUIScenario02
pip install -r requirements.txt
```

## Scénario 01

### PoC exploitation

#### Server

```shell
python3 Scenario01/Exploitation/server.py 
```

#### Client

```shell
python3 Scenario01/Exploitation/client.py -i 127.0.0.1
```

### PoC mitigation

#### Server

```shell
python3 Scenario01/Mitigation/server.py 
```

#### Client

```shell
python3 Scenario01/Mitigation/client.py -i 127.0.0.1
```

## Scénario 02

### PoC exploitation

```shell
python3 GUIScenario02/main.py -m exploitation
```

Il est possible de connecter au serveur OPC UA avec `uaexpert` (https://www.unified-automation.com/downloads/opc-ua-clients.html).

### PoC mitigation

```shell
python3 GUIScenario02/main.py -m mitigation
```

Il est possible de connecter au serveur OPC UA avec `uaexpert`.



