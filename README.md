# Simulador de colisão perfeitamente inelástica

Simulador interativo em Python (matplotlib) de uma colisão frontal unidimensional entre dois blocos que ficam unidos após o choque. Mostra a animação do movimento e, em tempo real, o que acontece com o momento linear, a energia cinética, os impulsos e a força média.

Trabalho **ADO-3 — Colisões, Impulso e Conservação do Momento Linear**, da disciplina *Física: Práticas Extensivas* (Prof. Ettore Baldini-Neto). Opção B: colisão perfeitamente inelástica.

## Como executar

Requisitos: Python 3 e matplotlib.

```bash
pip install matplotlib
python ADO3_Guilherme_Erick_Pedro.py
```

## O que o programa faz

- **Animação** dos dois blocos em MRU antes e depois do choque, com tamanho visual dependente da massa. O instante da colisão é calculado em fórmula fechada, sem integração numérica.
- **Painel de resultados** com velocidades antes e depois, momento linear, energia cinética (antes, depois e variação), impulsos J1 e J2 e força média.
- **Gráficos de barras** comparando o momento total e a energia cinética total antes e depois.
- **Caso sem colisão** (v1 ≤ v2): mostra um aviso na tela, sem erro de execução.

### Controles

| Controle | Função |
|---|---|
| Sliders m1, m2 | Massas dos blocos (kg) |
| Sliders v1, v2 | Velocidades iniciais (m/s) |
| Slider Δt | Duração do contato (ms) |
| Pausar / Continuar | Congela e retoma a animação |
| Reiniciar | Recomeça a simulação |

Ao mudar qualquer slider, a simulação reinicia com os novos valores.

## Física utilizada

Fórmulas fechadas, em unidades do SI:

- Velocidade final dos blocos unidos: `V = (m1·v1 + m2·v2) / (m1 + m2)`
- Variação de energia cinética: `ΔK = −½·μ·(v1 − v2)²`, com `μ = m1·m2 / (m1 + m2)`
- Impulsos: `J1 = m1·(V − v1)` e `J2 = m2·(V − v2)`, com `J1 = −J2`
- Força média: `F_med = |J| / Δt`

Situação padrão (m1 = 2,0 kg, m2 = 3,0 kg, v1 = 5,0 m/s, v2 = 0, Δt = 10 ms): `V = 2,0 m/s`, `ΔK = −15 J` (60 % da energia dissipada), `J1 = −6 N·s`, `J2 = +6 N·s` e `F_med = 600 N`.

## Testes

```bash
python teste_fisica.py
```

Verifica as fórmulas na situação padrão, o efeito de Δt sobre a força média, o caso de momento total nulo e o caso sem colisão.

## Estrutura

- `ADO3_Guilherme_Erick_Pedro.py`: programa completo (física e interface)
- `teste_fisica.py`: testes das fórmulas
- Relatório em PDF com as respostas de Q1 a Q5

## Autores

- Guilherme Reis Takahashi
- Pedro Ulrich Ramos Heringer
- Erick de Paula Moreira
