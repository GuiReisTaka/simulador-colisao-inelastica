"""ADO-3 — Física: Práticas Extensivas (Prof. Ettore Baldini-Neto)
Colisão perfeitamente inelástica 1D (opção B) com animação interativa.

Grupo: Guilherme Reis Takahashi, Pedro Ulrich Ramos Heringer e Erick de Paula Moreira

Execução: python ADO3_Guilherme_Erick_Pedro.py
Bibliotecas: apenas matplotlib. Fórmulas fechadas, sem integração numérica; unidades do SI.
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button, Slider

# ====================== FÍSICA (fórmulas fechadas) ======================
def momento(m1, v1, m2, v2):
    """Momento linear total p = m1*v1 + m2*v2 (kg·m/s)."""
    return m1 * v1 + m2 * v2


def cinetica(m1, v1, m2, v2):
    """Energia cinética total K (J)."""
    return 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2


def massa_reduzida(m1, m2):
    """Massa reduzida mu = m1*m2/(m1+m2) (kg)."""
    return m1 * m2 / (m1 + m2)


def colisao_inelastica(m1, m2, v1, v2):
    """Velocidade final comum V dos blocos unidos (m/s)."""
    return momento(m1, v1, m2, v2) / (m1 + m2)


def delta_k(m1, m2, v1, v2):
    """Variação de energia cinética: -1/2 * mu * (v1 - v2)^2 (J)."""
    return -0.5 * massa_reduzida(m1, m2) * (v1 - v2) ** 2


def impulsos(m1, m2, v1, v2):
    """Impulsos J1 e J2 (N·s), pelo teorema impulso-momento."""
    V = colisao_inelastica(m1, m2, v1, v2)
    return m1 * (V - v1), m2 * (V - v2)


def forca_media(J, dt_ms):
    """Força média |J|/dt (N), com dt em milissegundos."""
    return abs(J) / (dt_ms / 1000.0)


def instante_colisao(x1_0, x2_0, larg1, larg2, v1, v2):
    """Instante tc (s) em que os blocos se tocam; None se v1 <= v2."""
    if v1 <= v2:
        return None
    folga = (x2_0 - x1_0) - (larg1 + larg2) / 2
    return max(folga, 0.0) / (v1 - v2)


def resolver(m1, m2, v1, v2, dt_ms):
    """Calcula todos os resultados da colisão em um dicionário."""
    V = colisao_inelastica(m1, m2, v1, v2)
    J1, J2 = impulsos(m1, m2, v1, v2)
    k_antes = cinetica(m1, v1, m2, v2)
    k_depois = cinetica(m1, V, m2, V)
    return {
        "V": V,
        "p_antes": momento(m1, v1, m2, v2),
        "p_depois": momento(m1, V, m2, V),
        "K_antes": k_antes,
        "K_depois": k_depois,
        "dK": delta_k(m1, m2, v1, v2),
        "J1": J1,
        "J2": J2,
        "F_med": forca_media(J1, dt_ms),
    }


# ====================== INTERFACE (matplotlib) ======================
X1_0, X2_0 = 2.0, 12.0   # posições iniciais dos centros (m)
SPAN = 30.0              # largura fixa da janela (m): mesma escala sempre
DT_FRAME = 0.05          # tempo simulado por quadro (s)
INTERVALO_MS = 50        # intervalo entre quadros (20 quadros/s)
T_POS = 3.0              # tempo simulado após a colisão (s)
T_SEM = 5.0              # duração quando não há colisão (s)
DURACAO_MAX = 8.0        # duração máxima da animação em tempo real (s)


# ---------- funções auxiliares (sem widgets) ----------

def largura(m):
    """Largura visual do bloco, crescente com a massa (m)."""
    return 0.8 * m ** 0.5


def altura(m):
    """Altura visual do bloco, crescente com a massa (m)."""
    return 0.3 * m ** 0.5


def posicoes(t, m1, m2, v1, v2):
    """Centros e velocidades dos blocos no instante t (MRU antes e depois)."""
    tc = instante_colisao(X1_0, X2_0, largura(m1), largura(m2), v1, v2)
    if tc is None or t < tc:
        return X1_0 + v1 * t, X2_0 + v2 * t, v1, v2
    V = colisao_inelastica(m1, m2, v1, v2)
    x1c = X1_0 + v1 * tc
    x2c = X2_0 + v2 * tc
    return x1c + V * (t - tc), x2c + V * (t - tc), V, V


def bordas(t, m1, m2, v1, v2):
    """Bordas esquerda/direita dos dois blocos no instante t."""
    x1, x2, _, _ = posicoes(t, m1, m2, v1, v2)
    return [x1 - largura(m1) / 2, x1 + largura(m1) / 2,
            x2 - largura(m2) / 2, x2 + largura(m2) / 2]


def janela_x(m1, m2, v1, v2):
    """Janela de largura fixa SPAN, centrada entre o início e o choque."""
    tc = instante_colisao(X1_0, X2_0, largura(m1), largura(m2), v1, v2)
    pontos = bordas(0.0, m1, m2, v1, v2)
    if tc is not None:
        com_choque = pontos + bordas(tc, m1, m2, v1, v2)
        if max(com_choque) - min(com_choque) <= SPAN - 2:   # se o choque cabe
            pontos = com_choque
    centro = (min(pontos) + max(pontos)) / 2
    return centro - SPAN / 2, centro + SPAN / 2


def tempo_final(m1, m2, v1, v2):
    """Instante (s) em que a simulação termina: tempo fixo após o choque,
    ou antes, se algum bloco chegar à borda da janela."""
    tc = instante_colisao(X1_0, X2_0, largura(m1), largura(m2), v1, v2)
    t_fim = T_SEM if tc is None else tc + T_POS
    lo, hi = janela_x(m1, m2, v1, v2)
    t = 0.0
    while t < t_fim:
        b = bordas(t, m1, m2, v1, v2)
        if min(b) < lo or max(b) > hi:
            return max(t, 0.1)
        t += 0.02
    return t_fim


def texto_painel(m1, m2, v1, v2, dt_ms):
    """Texto do painel de resultados."""
    if v1 <= v2:
        p = momento(m1, v1, m2, v2)
        k = cinetica(m1, v1, m2, v2)
        return (f"SEM COLISÃO (v1 ≤ v2)\n\n"
                f"v1 = {v1:.2f} m/s   v2 = {v2:.2f} m/s\n"
                f"p = {p:.2f} kg·m/s\nK = {k:.2f} J\n"
                f"J1 = J2 = 0\nF_med = 0")
    r = resolver(m1, m2, v1, v2, dt_ms)
    frac = 100 * abs(r["dK"]) / r["K_antes"] if r["K_antes"] > 0 else 0.0
    return (f"ANTES\n v1 = {v1:.2f} m/s   v2 = {v2:.2f} m/s\n\n"
            f"DEPOIS\n V = {r['V']:.2f} m/s (blocos unidos)\n\n"
            f"MOMENTO LINEAR\n p antes  = {r['p_antes']:.2f} kg·m/s\n"
            f" p depois = {r['p_depois']:.2f} kg·m/s\n\n"
            f"ENERGIA CINÉTICA\n K antes  = {r['K_antes']:.2f} J\n"
            f" K depois = {r['K_depois']:.2f} J\n"
            f" ΔK = {r['dK']:.2f} J ({frac:.1f} % dissipado)\n\n"
            f"IMPULSO E FORÇA MÉDIA\n J1 = {r['J1']:.2f} N·s   J2 = {r['J2']:.2f} N·s\n"
            f" F_med = {r['F_med']:.2f} N (Δt = {dt_ms:.0f} ms)")


def valores_barras(m1, m2, v1, v2, dt_ms):
    """(p_antes, p_depois, K_antes, K_depois); sem colisão, nada muda."""
    if v1 <= v2:
        p = momento(m1, v1, m2, v2)
        k = cinetica(m1, v1, m2, v2)
        return p, p, k, k
    r = resolver(m1, m2, v1, v2, dt_ms)
    return r["p_antes"], r["p_depois"], r["K_antes"], r["K_depois"]


def ajustar_ylim(ax, valores):
    """Ajusta o eixo y do gráfico de barras (inclui o zero)."""
    lo = min(valores + [0.0])
    hi = max(valores + [0.0])
    margem = 0.15 * (hi - lo) or 1.0
    ax.set_ylim(lo - margem if lo < 0 else 0, hi + margem)


# ---------- interface ----------

def main():
    fig = plt.figure(figsize=(12, 8))
    estado = {"t": 0.0, "t_fim": 1.0, "passo": DT_FRAME,
              "pausado": False, "timer_parado": False}

    # Área da animação
    ax_sim = fig.add_axes([0.05, 0.62, 0.58, 0.33])
    ax_sim.set_xlim(0, SPAN)
    ax_sim.set_ylim(0, 4)
    ax_sim.set_yticks([])
    ax_sim.set_xlabel("x (m)")
    ax_sim.set_title("Bloco 1 (azul)  →  Bloco 2 (laranja)")
    ax_sim.axhline(0, color="k")
    ret1 = Rectangle((0, 0), 1, 1, color="tab:blue")
    ret2 = Rectangle((0, 0), 1, 1, color="tab:orange")
    ax_sim.add_patch(ret1)
    ax_sim.add_patch(ret2)
    txt_tempo = ax_sim.text(0.02, 0.88, "", transform=ax_sim.transAxes)
    txt_aviso = ax_sim.text(0.5, 0.6, "", transform=ax_sim.transAxes,
                            ha="center", color="red", fontsize=13)

    # Painel de resultados
    ax_txt = fig.add_axes([0.66, 0.30, 0.32, 0.65])
    ax_txt.axis("off")
    txt_painel = ax_txt.text(0, 1, "", va="top", family="monospace", fontsize=9,
                             transform=ax_txt.transAxes)

    # Gráficos de barras
    ax_p = fig.add_axes([0.07, 0.30, 0.25, 0.22])
    ax_k = fig.add_axes([0.38, 0.30, 0.25, 0.22])
    barras_p = ax_p.bar(["antes", "depois"], [0, 0], color=["tab:gray", "tab:green"])
    barras_k = ax_k.bar(["antes", "depois"], [0, 0], color=["tab:gray", "tab:red"])
    ax_p.set_title("Momento total p (kg·m/s)", fontsize=10)
    ax_k.set_title("Energia cinética total K (J)", fontsize=10)
    ax_p.axhline(0, color="k", lw=0.8)
    ax_k.axhline(0, color="k", lw=0.8)

    # Sliders
    def criar_slider(y, nome, vmin, vmax, valor, passo):
        ax = fig.add_axes([0.12, y, 0.40, 0.025])
        return Slider(ax, nome, vmin, vmax, valinit=valor, valstep=passo)

    sl_m1 = criar_slider(0.20, "m1 (kg)", 0.5, 10, 2.0, 0.1)
    sl_m2 = criar_slider(0.16, "m2 (kg)", 0.5, 10, 3.0, 0.1)
    sl_v1 = criar_slider(0.12, "v1 (m/s)", -10, 10, 5.0, 0.1)
    sl_v2 = criar_slider(0.08, "v2 (m/s)", -10, 10, 0.0, 0.1)
    sl_dt = criar_slider(0.04, "Δt (ms)", 1, 100, 10, 1)

    # Botões
    btn_pausa = Button(fig.add_axes([0.68, 0.12, 0.12, 0.06]), "Pausar")
    btn_reinicia = Button(fig.add_axes([0.83, 0.12, 0.12, 0.06]), "Reiniciar")

    def parametros():
        return sl_m1.val, sl_m2.val, sl_v1.val, sl_v2.val, sl_dt.val

    # Liga/desliga o timer da animação (timer parado = zero CPU)
    def parar_timer():
        if not estado["timer_parado"]:
            anim.event_source.stop()
            estado["timer_parado"] = True

    def ligar_timer():
        if estado["timer_parado"]:
            anim.event_source.start()
            estado["timer_parado"] = False

    def desenhar(t):
        m1, m2, v1, v2, _ = parametros()
        x1, x2, u1, u2 = posicoes(t, m1, m2, v1, v2)
        ret1.set_xy((x1 - largura(m1) / 2, 0))
        ret1.set_width(largura(m1))
        ret1.set_height(altura(m1))
        ret2.set_xy((x2 - largura(m2) / 2, 0))
        ret2.set_width(largura(m2))
        ret2.set_height(altura(m2))
        txt_tempo.set_text(f"t = {t:.2f} s   v1 = {u1:.2f} m/s   v2 = {u2:.2f} m/s")

    def atualizar_resultados():
        m1, m2, v1, v2, dt = parametros()
        txt_painel.set_text(texto_painel(m1, m2, v1, v2, dt))
        txt_aviso.set_text("Sem colisão: v1 ≤ v2" if v1 <= v2 else "")
        pa, pd, ka, kd = valores_barras(m1, m2, v1, v2, dt)
        for barra, h in zip(barras_p, (pa, pd)):
            barra.set_height(h)
        for barra, h in zip(barras_k, (ka, kd)):
            barra.set_height(h)
        ajustar_ylim(ax_p, [pa, pd])
        ajustar_ylim(ax_k, [ka, kd])

    def reiniciar(_=None):
        m1, m2, v1, v2, dt = parametros()
        estado["t"] = 0.0
        estado["pausado"] = False
        estado["t_fim"] = tempo_final(m1, m2, v1, v2)
        # Se a colisão demorar muito, acelera o relógio da simulação
        estado["passo"] = DT_FRAME * max(1.0, estado["t_fim"] / DURACAO_MAX)
        lo, hi = janela_x(m1, m2, v1, v2)
        ax_sim.set_xlim(lo, hi)
        btn_pausa.label.set_text("Pausar")
        atualizar_resultados()
        desenhar(0.0)
        ligar_timer()
        fig.canvas.draw_idle()

    def alternar_pausa(_):
        estado["pausado"] = not estado["pausado"]
        if estado["pausado"]:
            btn_pausa.label.set_text("Continuar")
            parar_timer()
        else:
            btn_pausa.label.set_text("Pausar")
            ligar_timer()
        fig.canvas.draw_idle()

    def quadro(_):
        estado["t"] = min(estado["t"] + estado["passo"], estado["t_fim"])
        desenhar(estado["t"])
        if estado["t"] >= estado["t_fim"]:
            parar_timer()   # fim da simulação: para de redesenhar

    for sl in (sl_m1, sl_m2, sl_v1, sl_v2, sl_dt):
        sl.on_changed(reiniciar)
    btn_pausa.on_clicked(alternar_pausa)
    btn_reinicia.on_clicked(reiniciar)

    anim = FuncAnimation(fig, quadro, interval=INTERVALO_MS, cache_frame_data=False)
    reiniciar()
    plt.show()


if __name__ == "__main__":
    main()
