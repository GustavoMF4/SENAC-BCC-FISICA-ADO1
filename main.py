# REQUISITOS:
# - Python 3.10+
# - NumPy
# - Matplotlib
#
# INSTALAÇÃO:
# No terminal do VS Code, execute:
#
#     python -m pip install numpy matplotlib
#
# EXECUÇÃO:
# Na pasta onde este arquivo está localizado, execute:
#
#     python projetil.py
#
# OU, no VS Code:
# Execute o arquivo projetil.py pelo botão "Run Python File".
#
# CONTROLES:
# - Velocidade inicial (m/s)
# - Ângulo de lançamento (graus)
# - Altura inicial (m)
# - Gravidade (m/s²)
#
# Os valores são atualizados automaticamente conforme os
# campos de entrada são alterados.
#
# O botão "LANÇAR" inicia a animação do projétil.
#

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.animation import FuncAnimation

x0 = 0
v0_atual = 50.0
theta_atual = 45.0
y0_atual = 0.0
g_atual = 9.81


#Função para calcular o tempo de voo, altura máxima e alcance horizontal do projétil
def calcular(v0, theta, y0, g):

    theta_rad = np.radians(theta)

    #Componentes da velocidade
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)

    #Tempo de voo
    t_voo = (
        vy + np.sqrt(vy**2 + 2 * g * y0)
    ) / g

    #Altura máxima
    y_max = y0 + (vy**2) / (2 * g)

    #Alcance horizontal
    R = x0 + vx * t_voo

    return t_voo, y_max, R

fig, ax = plt.subplots(figsize=(12, 8))

plt.subplots_adjust(
    left=0.08,
    right=0.95,
    top=0.90,
    bottom=0.35
)



#trajetoria incial
t_voo, y_max, R = calcular(
    v0_atual,
    theta_atual,
    y0_atual,
    g_atual
)

t = np.linspace(0, t_voo, 300)

theta_rad = np.radians(theta_atual)

x = (
    x0
    + v0_atual * np.cos(theta_rad) * t
)

y = (
    y0_atual
    + v0_atual * np.sin(theta_rad) * t
    - 0.5 * g_atual * t**2
)



#Desenha a trajetória 
linha, = ax.plot(
    x,
    y,
    linewidth=2,
    label="Trajetória"
)

#Projétil que estamos lançando
projetil, = ax.plot(
    [x0],
    [y0_atual],
    'o',
    markersize=10,
    label="Projétil"
)

#configurações do gráfico
ax.set_title(
    "Lançamento de Projétil",
    fontsize=16
)

ax.set_xlabel(
    "Distância horizontal (m)"
)

ax.set_ylabel(
    "Altura (m)"
)

ax.grid(True)

ax.legend()

ax.set_aspect(
    'equal',
    adjustable='box'
)


#esbição dos resultados do lançamento
texto_resultados = fig.text(
    0.75,
    0.22,
    "",
    fontsize=11
)


def atualizar_resultados():

    t_voo, y_max, R = calcular(
        v0_atual,
        theta_atual,
        y0_atual,
        g_atual
    )

    texto_resultados.set_text(
        f"RESULTADOS\n\n"
        f"Alcance horizontal: {R:.2f} m\n"
        f"Altura máxima: {y_max:.2f} m\n"
        f"Tempo de voo: {t_voo:.2f} s"
    )


atualizar_resultados()

#exibição dos campos de entrada para os parâmetros do lançamento

#Velocidade (m/s)
ax_v0 = plt.axes([
    0.18,
    0.25,
    0.20,
    0.045
])

campo_v0 = TextBox(
    ax_v0,
    "Velocidade (m/s): ",
    initial=str(v0_atual)
)


#Ângulo (θ)
ax_theta = plt.axes([
    0.18,
    0.19,
    0.20,
    0.045
])

campo_theta = TextBox(
    ax_theta,
    "Ângulo (°): ",
    initial=str(theta_atual)
)


#Altura
ax_y0 = plt.axes([
    0.18,
    0.13,
    0.20,
    0.045
])

campo_y0 = TextBox(
    ax_y0,
    "Altura inicial (m): ",
    initial=str(y0_atual)
)


#Gravidade (g)
ax_g = plt.axes([
    0.18,
    0.07,
    0.20,
    0.045
])

campo_g = TextBox(
    ax_g,
    "Gravidade (m/s²): ",
    initial=str(g_atual)
)


mensagem = fig.text(
    0.50,
    0.03,
    "",
    ha="center",
    fontsize=10
)


def atualizar(event):

    global v0_atual
    global theta_atual
    global y0_atual
    global g_atual

    #tentativa de converter os valores dos campos de entrada para float
    try:

        v0 = float(
            campo_v0.text.replace(",", ".")
        )

        theta = float(
            campo_theta.text.replace(",", ".")
        )

        y0 = float(
            campo_y0.text.replace(",", ".")
        )

        g = float(
            campo_g.text.replace(",", ".")
        )

    except ValueError:

        mensagem.set_text(
            "ERRO: digite apenas valores numéricos."
        )

        fig.canvas.draw_idle()

        return


  
    #Validação dos valores de entrada do usuario.

    #velocidade (m/s)
    if v0 <= 0:

        mensagem.set_text(
            "ERRO: a velocidade deve ser maior que 0 m/s."
        )

        fig.canvas.draw_idle()

        return

    #ângulo (θ)
    if theta <= 0 or theta >= 90:

        mensagem.set_text(
            "ERRO: o ângulo deve estar entre 0° e 90°."
        )

        fig.canvas.draw_idle()

        return


    #altura inicial (y0)
    if y0 < 0:

        mensagem.set_text(
            "ERRO: a altura inicial não pode ser negativa."
        )

        fig.canvas.draw_idle()

        return


    #gravidade (g)
    if g <= 0:

        mensagem.set_text(
            "ERRO: a gravidade deve ser maior que 0."
        )

        fig.canvas.draw_idle()

        return


    v0_atual = v0
    theta_atual = theta
    y0_atual = y0
    g_atual = g


    
#realiza os cálculos da física com os valores atualizados
    t_voo, y_max, R = calcular(
        v0_atual,
        theta_atual,
        y0_atual,
        g_atual
    )

    t = np.linspace(
        0,
        t_voo,
        300
    )

    theta_rad = np.radians(
        theta_atual
    )

    x = (
        x0
        + v0_atual
        * np.cos(theta_rad)
        * t
    )

    y = (
        y0_atual
        + v0_atual
        * np.sin(theta_rad)
        * t
        - 0.5
        * g_atual
        * t**2
    )


    linha.set_data(
        x,
        y
    )

    projetil.set_data(
        [x0],
        [y0_atual]
    )


    #Ajusta os limites do gráfico
    ax.set_xlim(
        0,
        max(10, R * 1.1)
    )

    ax.set_ylim(
        0,
        max(10, y_max * 1.1)
    )

    atualizar_resultados()


    
    #limpeza de mensagens de erro
    mensagem.set_text(
        "Valores atualizados com sucesso!"
    )


    fig.canvas.draw_idle()


campo_v0.on_text_change(atualizar)
campo_theta.on_text_change(atualizar)
campo_y0.on_text_change(atualizar)
campo_g.on_text_change(atualizar)



#botão de lançamento do projétil
ax_lancar = plt.axes([
    0.45,
    0.06,
    0.16,
    0.06
])

botao_lancar = Button(
    ax_lancar,
    "LANÇAR"
)


#animação do lançamento do projétil
animacao = None


def lancar(event):

    global animacao

    #Valores atualmente válidos
    v0 = v0_atual
    theta = theta_atual
    y0 = y0_atual
    g = g_atual

    theta_rad = np.radians(
        theta
    )

    # cauculo do tempo de voo
    t_voo, y_max, R = calcular(
        v0,
        theta,
        y0,
        g
    )

    tempos = np.linspace(
        0,
        t_voo,
        100
    )


   
    #movimentação do projetil durante a animação
    def mover(i):

        t = tempos[i]

        x = (
            x0
            + v0
            * np.cos(theta_rad)
            * t
        )

        y = (
            y0
            + v0
            * np.sin(theta_rad)
            * t
            - 0.5
            * g
            * t**2
        )

        projetil.set_data(
            [x],
            [y]
        )

        return projetil,


    animacao = FuncAnimation(
        fig,
        mover,
        frames=len(tempos),
        interval=30,
        blit=True,
        repeat=False
    )

    fig.canvas.draw_idle()


botao_lancar.on_clicked(
    lancar
)

plt.show()
