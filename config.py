# Reference from Blackbird
# Usage: "import config" to use parameters "config.PARAMETER"

# Program parameters
DemoMode=True
Leg1='BTC'
Leg2='USD'
UseFullExposure=False
TestedExposure=25.00
MaxExposure=25000.00
MaxLength=5184000
DebugMaxIteration=3200000
Verbose=True
CACert='curl-ca-bundle.crt'

# Strategy parameters
Interval=3.0
SpreadEntry=0.0080
SpreadTarget=0.0050
PriceDeltaLimit=0.10
TrailingSpreadLim=0.0008
TrailingSpreadCount=1
OrderBookFactor=3.0
UseVolatility=False
VolatilityPeriod=600

# Email settings
SendEmail=False
SenderAddress=0
SenderUsername=0
SenderPassword=0
SmtpServerAddress=0
ReceiverAddress=0

# Database settings
DBFile='blackbird.db'

# Bitfinex
BitfinexApiKey=0
BitfinexSecretKey=0
BitfinexFees=0.0020
BitfinexEnable=True

# OkCoin
OkCoinApiKey=0
OkCoinSecretKey=0
OkCoinFees=0.0020
OkCoinEnable=True

# Bitstamp
BitstampClientId=0
BitstampApiKey=0
BitstampSecretKey=0
BitstampFees=0.0025
BitstampEnable=True

# Gemini
GeminiApiKey=0
GeminiSecretKey=0
GeminiFees=0.0025
GeminiEnable=True

# Kraken
KrakenApiKey=0
KrakenSecretKey=0
KrakenFees=0.0025
KrakenEnable=True

# ItBit
ItBitApiKey=0
ItBitSecretKey=0
ItBitFees=0.0020
ItBitEnable=True

# WEX
WEXApiKey=0
WEXSecretKey=0
WEXFees=0.0020
WEXEnable=False

# Poloniex
# Note: no BTC/USD on Poloniex
PoloniexApiKey=0
PoloniexSecretKey=0
PoloniexFees=0.0020
PoloniexEnable=True

# GDAX
GDAXApiKey=0
GDAXSecretKey=0
GDAXPhrase=0
GDAXFees=0.0025
GDAXEnable=True

# QuadrigaCX
QuadrigaApiKey=0
QuadrigaSecretKey=0
QuadrigaFees=0.005
QuadrigaClientId=0
QuadrigaEnable=True

# Exmo
ExmoApiKey=0
ExmoSecretKey=0
ExmoFees=0.002
ExmoEnable=True

# Cex.io
CexioClientId=0
CexioApiKey=0
CexioSecretKey=0
CexioFees=0.0025
CexioEnable=True

# Bittrex
BittrexApiKey=0
BittrexSecretKey=0
BittrexFees=0
BittrexEnable=True

# Binance
BinanceApiKey=0
BinanceSecretKey=0
BinanceFees=0
BinanceEnable=True
