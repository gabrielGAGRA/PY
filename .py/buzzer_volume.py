import numpy as np
import sounddevice as sd


def play_buzzer_full(freq, duration, fs=44100):
    """Buzzer tocando 100% do tempo (volume máximo)."""
    t = np.arange(int(fs * duration)) / fs
    wave = 0.3 * np.sign(np.sin(2 * np.pi * freq * t))
    print(f"Buzzer a {freq}Hz — 100% do tempo (volume cheio)")
    sd.play(wave, fs)
    sd.wait()


def play_buzzer_pwm_native(freq, duration, duty_cycle, fs=44100):
    """
    Simula volume no buzzer modulando a largura do pulso da própria nota
    (em vez de ligar/desligar usando uma segunda frequência PWM externa).

    Quando distorcemos a largura do pulso da onda fundamental (ex: de 50% para 10%),
    a nota percebida continua a mesma, mas a energia total na frequência
    fundamental cai, criando uma percepção muito clara de redução de volume
    em circuitos digitais e buzzers, sem distorção fantasma.
    """
    t = np.arange(int(fs * duration)) / fs

    # Cria uma rampa para cada ciclo da frequência (fase 0 a 1)
    phase = (t * freq) % 1.0

    # Sinal passa a ser ALTO apenas na fração `duty_cycle` de cada ciclo da própria nota!
    # - duty_cycle = 0.5 (onda quadrada padrão = volume máximo = +energia na fundamental)
    # - duty_cycle = 0.1 (pulsos bem curtos = volume baixo)
    wave = np.where(phase < duty_cycle, 0.3, -0.3)

    print(
        f"Buzzer a {freq:.0f}Hz — Duty Nativo {duty_cycle*100:.0f}% (Volume Reduzido)"
    )
    sd.play(wave, fs)
    sd.wait()


if __name__ == "__main__":
    fs = 44100

    # Notas musicais na faixa aguda (oitava 6 — boa para buzzers)
    notas = {
        "Dó": 2093.00,  # C7
        "Ré": 2349.32,  # D7
        "Mi": 2637.02,  # E7
        "Fá": 2793.83,  # F7
        "Sol": 3135.96,  # G7
        "Lá": 3520.00,  # A7
        "Si": 3951.07,  # B7
    }

    print("=== Controle de Volume: PWM na própria Onda da Nota ===\n")

    # 1. Escala a 100% de volume (Onda Quadrada 50% Duty Cycle)
    print("--- 1. Escala musical (Volume Máximo - Duty 50%) ---")
    for nome, freq in notas.items():
        print(f"  {nome} ({freq:.0f}Hz)")
        play_buzzer_pwm_native(freq, 0.5, 0.5, fs)

    # 2. Mesma escala a ~30% de volume percebido (PWM Duty 10%)
    print("\n--- 2. Escala musical (Volume Menor - Duty 10%) ---")
    for nome, freq in notas.items():
        print(f"  {nome} ({freq:.0f}Hz)")
        play_buzzer_pwm_native(freq, 0.5, 0.1, fs)

    # 3. Mesma escala bem baixa (PWM Duty 2%)
    print("\n--- 3. Escala musical (Volume Baixinho - Duty 2%) ---")
    for nome, freq in notas.items():
        print(f"  {nome} ({freq:.0f}Hz)")
        play_buzzer_pwm_native(freq, 0.5, 0.02, fs)
