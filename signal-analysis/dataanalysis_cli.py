

import matplotlib.pyplot as plt

def plot_amplitudes(fft_result: dict) -> None:
    """
    Plot the amplitude spectrum from an RFFT result.

    Args:
        fft_result: Dictionary returned by calculate_rfft(), containing
                    'frequencies' and 'amplitudes' arrays
    """
    frequencies = fft_result["frequencies"]
    amplitudes = fft_result["amplitudes"]

    plt.figure(figsize=(10, 5))
    plt.stem(frequencies, amplitudes, basefmt=" ")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Amplitude Spectrum")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()