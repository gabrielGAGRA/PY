import numpy as np
import sounddevice as sd


def play_buzzer_full(freq, duration, fs=44100):
    """Buzzer tocando 100% do tempo (volume máximo)."""
    t = np.arange(int(fs * duration)) / fs
    wave = 0.3 * np.sign(np.sin(2 * np.pi * freq * t))
    print(f"Buzzer a {freq}Hz — 100% do tempo (volume cheio)")
    sd.play(wave, fs)
    sd.wait()


def play_buzzer_pwm(freq, duration, duty_cycle, switch_hz, fs=44100):
    """
    Alterna entre tocar e silêncio para simular controle de volume via PWM.

    - freq: frequência da nota (onda quadrada)
    - duration: duração total em segundos
    - duty_cycle: fração do tempo ligado (0.0 a 1.0). Ex: 0.5 = 50% do tempo tocando
    - switch_hz: quantas vezes por segundo liga/desliga (frequência do PWM)
    """
    t = np.arange(int(fs * duration)) / fs
    # Gera a onda quadrada completa
    square_wave = 0.3 * np.sign(np.sin(2 * np.pi * freq * t))

    # Cria a envoltória PWM: liga por duty_cycle% de cada período, desliga o resto
    samples_per_period = int(fs / switch_hz)
    samples_on = int(samples_per_period * duty_cycle)

    envelope = np.zeros(len(t))
    for i in range(0, len(t), samples_per_period):
        end_on = min(i + samples_on, len(t))
        envelope[i:end_on] = 1.0

    output_wave = square_wave * envelope

    print(
        f"Buzzer a {freq}Hz — duty cycle {duty_cycle*100:.0f}% "
        f"(PWM a {switch_hz}Hz)"
    )
    sd.play(output_wave, fs)
    sd.wait()


if __name__ == "__main__":
    fs = 44100
    freq = 2000  # 2kHz — frequência típica de ressonância de buzzers piezo

    print("=== Controle de Volume por PWM (liga/desliga) ===\n")

    # 4. Comparação de duty cycles com PWM rápido
    print("\n--- 4. Escala de 'volumes' via duty cycle (PWM a 500Hz) ---")
    for duty in [1.0, 0.75, 0.5, 0.25, 0.10]:
        play_buzzer_pwm(freq, 1.5, duty, 500, fs)
