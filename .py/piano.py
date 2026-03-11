import numpy as np
import sounddevice as sd


def play_buzzer_style(freq, duration, fs=44100):
    t = np.arange(int(fs * duration)) / fs
    # Onda quadrada: simula o comportamento Liga/Desliga de um buzzer digital
    wave = 0.3 * np.sign(np.sin(2 * np.pi * freq * t))
    print(f"Buzzer simulado a {freq}Hz...")
    sd.play(wave, fs)
    sd.wait()


def play_buzzer_alternation(freq_a, freq_b, duration, switch_hz, fs=44100):
    # switch_hz define quantas vezes por segundo trocamos entre as notas
    t = np.arange(int(fs * duration)) / fs
    output_wave = np.zeros(len(t))

    samples_per_switch = int(fs / switch_hz)

    for i in range(0, len(t), samples_per_switch):
        end = min(i + samples_per_switch, len(t))
        # Alterna entre freq_a e freq_b
        current_freq = freq_a if (i // samples_per_switch) % 2 == 0 else freq_b

        # Gera onda quadrada para este segmento
        segment_t = t[i:end]
        output_wave[i:end] = 0.3 * np.sign(np.sin(2 * np.pi * current_freq * segment_t))

    print(
        f"Alternância tipo Buzzer: {freq_a}Hz e {freq_b}Hz a {switch_hz} alternâncias/seg..."
    )
    sd.play(output_wave, fs)
    sd.wait()


if __name__ == "__main__":
    fs = 44100
    # Notas agudas (faixa de ressonância do buzzer)
    nota_do = 523.00  # Dó (C7) - bem agudo
    nota_si = 449.0  # Si (B7) - limite de agudez comum

    print("--- 1. Simulando Buzzer (Onda Quadrada) ---")
    play_buzzer_style(nota_do, 1.5, fs)

    print("\n--- 3. Alternância no limite auditivo (2000 vezes por segundo) ---")
    # Aqui o som vira um timbre complexo (você não distingue as notas)
    play_buzzer_alternation(nota_do, nota_si, 3, 2000, fs)

    print("\n---(20000 vezes por segundo) ---")
    # Aqui o som vira um timbre complexo (você não distingue as notas)
    play_buzzer_alternation(nota_do, nota_si, 3, 20000, fs)

    print("\n---(40000 vezes por segundo) ---")
    # Aqui o som vira um timbre complexo (você não distingue as notas)
    play_buzzer_alternation(nota_do, nota_si, 3, 40000, fs)
