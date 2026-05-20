# Crazy World — Platformer em Python

Jogo de plataforma 2D feito com Pygame. A jogadora é **Yasmin**, que deve atravessar três fases cheias de plataformas móveis e inimigos robóticos para chegar ao portal de saída.

## Como jogar

```
pip install -r requirements.txt
python main.py
```

## Controles

| Tecla | Ação |
|-------|------|
| ← → | Mover |
| Espaço | Pular (duplo pulo no ar) |
| Shift | Dash |
| Clique esquerdo | Ataque corpo a corpo |
| Clique direito | Atirar projétil (requer power-up) |

## Fases

| Fase | Dificuldade | Plataformas |
|------|-------------|-------------|
| 1 | Fácil | Baixas, lentas |
| 2 | Médio | Médias, mais velozes |
| 3 | Difícil | Altas, velozes |

## Inimigos

- **Drone** — inimigo leve, 1 HP, dá 100 pontos
- **HeavyBot** — inimigo pesado, 2 HP, muda de sprite ao levar dano, dá 200 pontos

## Power-up

Colete o **WeaponPowerup** (caixa amarela `?`) para habilitar o disparo de projéteis por tempo limitado.

## Dependências

```
pygame
```
