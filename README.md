# DiceFamilyBot

Asistente de apuestas de la plataforma de TELEGRAM. El juego consiste en adivinar el próximo número a salir. El jugador realiza una apuesta y si gana recibe una recompensa asociada a ésta. Al finalizar cada ronda se dan los ganadores y se entregan las ganancias correspondientes y se reinician las apuestas. Los resultados se dan a conocer en cada hora en punto.

# Modos de juego

- **Dice:** consiste en adivinar el número que va a salir en la próxima ronda.
- **Tall and Bass:** consiste en adivinar si el numero será _Tall_ (4, 5, 6) o _Bass_ (1, 2, 3)
- **DBomb:** consiste en adivinar si un número no va a salir en la siguiente ronda.

# Dependencias

- aiohttp
- aioredis
- pyTelegramBotApi

# Iniciar

Para iniciar el bot solo hay que correr el siguiente comando:

``` script
make
```
