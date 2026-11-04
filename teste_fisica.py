"""Testes das fórmulas da ADO-3 (rodar: python teste_fisica.py)."""
from ADO3_Guilherme_Erick_Pedro import resolver, instante_colisao


def perto(a, b):
    return abs(a - b) < 1e-9


# Situação padrão da opção B
r = resolver(2.0, 3.0, 5.0, 0.0, 10)
assert perto(r["V"], 2.0)
assert perto(r["p_antes"], 10.0) and perto(r["p_depois"], 10.0)
assert perto(r["K_antes"], 25.0) and perto(r["K_depois"], 10.0)
assert perto(r["dK"], -15.0)
assert perto(r["K_depois"] - r["K_antes"], r["dK"])   # confere com a fórmula do mu
assert perto(r["J1"], -6.0) and perto(r["J2"], 6.0)   # J1 = -J2
assert perto(r["F_med"], 600.0)                       # dt = 10 ms

# dt dez vezes maior -> força média dez vezes menor
assert perto(resolver(2.0, 3.0, 5.0, 0.0, 100)["F_med"], 60.0)

# Q5: sentidos opostos com p = 0 -> V = 0 e toda a energia dissipada
r = resolver(2.0, 3.0, 3.0, -2.0, 10)
assert perto(r["p_antes"], 0.0) and perto(r["V"], 0.0)
assert perto(r["K_depois"], 0.0) and perto(r["dK"], -r["K_antes"])

# Sem colisão
assert instante_colisao(0.0, 5.0, 1.0, 1.0, 2.0, 3.0) is None

print("Todos os testes passaram.")
