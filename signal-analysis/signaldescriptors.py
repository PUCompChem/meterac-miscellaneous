import numpy as np
import math
import matplotlib.pyplot as plt


allowed_descriptor_types = ["number", "list", "text"]


class Descriptor:
    def __init__(self, name: str, typestr:str = "number", info: str = None):
        self.name = name
        self.typestr = typestr
        self.info = info

descriptor_list = [
    Descriptor("numpoints"),
    Descriptor("mean"),
    Descriptor("rms"),
    Descriptor("stdev"),
    Descriptor("min"),
    Descriptor("max"),
    Descriptor("span"),
    Descriptor("entropy"),
    ]

class DescriptorValue:
    def __init__(self, floatValue: float = None, listValue: list[float] = None, textValue: str = None,
                  errorMsg: str = None, info: str = None):
        self.floatValue = floatValue
        self.listValue = listValue
        self.textValue = textValue
        self.errorMsg = errorMsg
        self.info = info

class CalcSignalDescriptors:
    def __init__(self, signal: list[float], 
                 descriptors: list[str] = None, 
                 sample_rate: float = 10,
                 entropy_bin_delta: float = 1000): 
        self.signal = signal
        self.sample_rate =  sample_rate    #signal sample rate in  Hz (how many measurements per second)
        self.entropy_bin_delta = entropy_bin_delta
        if descriptors != None:
            #TODO
            self.descriptors = None
        else:                
            self.descriptors = descriptor_list  #by default entire descriptor list is used
        
    def calculate(self) -> dict[str, DescriptorValue]:
        dvalues = {}
        if self.descriptors == None:
            return dvalues
        for d in self.descriptors:
            dv = self.calculateDescriptor(d.name)
            dvalues[d.name] = dv
        return dvalues
    
    def calculateDescriptor(self, name: str) -> DescriptorValue:       
        if name == "numpoints":
            return self.calculateNumOfPoints()
        if name == "mean":
            return self.calculateMean()
        if name == "rms":
            return self.calculateRMS()
        if name == "stdev":
            return self.calculateStDev()
        if name == "min":
            return self.calculateMin()
        if name == "max":
            return self.calculateMax()
        if name == "span":
            return self.calculateSpan()
        if name == "entropy":
            #assuming the signal is between -32000 and +32000,
            # bin_delta ~1000 (default value) gives around 60 levels for entropy calculation
            return self.calculateEntropy(self.entropy_bin_delta)  
        return DescriptorValue(errorMsg = "Descriptor '" + name + "' is not supported")
        
    def calculateNumOfPoints(self) -> DescriptorValue:
        val = len (self.signal)
        return DescriptorValue(floatValue = val)
    
    def calculateMean(self) -> DescriptorValue:
        val = np.mean(self.signal)
        return DescriptorValue(floatValue = val)

    def calculateRMS(self) -> DescriptorValue:
        arr = np.array(self.signal)
        val = np.sqrt(np.mean(arr**2))
        return DescriptorValue(floatValue = val)
    
    def calculateStDev(self) -> DescriptorValue:
        #arr = np.array(self.signal)
        val = np.std(self.signal)
        return DescriptorValue(floatValue = val)
    
    def calculateMin(self) -> DescriptorValue:  
        val = np.min(self.signal)
        return DescriptorValue(floatValue = val)
    
    def calculateMax(self) -> DescriptorValue:
        val = np.max(self.signal)
        return DescriptorValue(floatValue = val)
    
    def calculateSpan(self) -> DescriptorValue:
        val = np.max(self.signal) - np.min(self.signal)
        return DescriptorValue(floatValue = val)
    
    def calculateEntropy(self, bin_delta:float) -> DescriptorValue:
        arr = np.array(self.signal)
        val = calc_entropy_based_on_even_bins(arr, bin_delta)
        return DescriptorValue(floatValue = val)

def calc_entropy_based_on_even_bins(data: np.ndarray, bin_delta:float) -> float:
    #print("### data =  ", data)
    min = np.min(data)
    max = np.max(data)
    num_bins = math.ceil((max-min)/bin_delta)
    if num_bins < 1:
       num_bins = 1
    hist, bins = np.histogram(data, bins=num_bins)
    p = hist/len(data)
    entropy = 0.0
    for x in p:
        if x > 0: # some bins might be 0
            entropy = entropy - x*math.log(x,2)
    #print("bins: ", bins)
    #print("hist: ", hist)
    #print("sum p:", np.sum(p))
    #print("len(data):", len(data))
    return entropy


def calculate_rfft(signal: list[float], sample_rate: float = 1.0) -> dict:
    """
    Calculate the real FFT (optimized for real-valued signals, returns only positive frequencies).

    Args:
        signal: List of float numbers representing the signal
        sample_rate: Sampling rate in Hz (default: 1.0)

    Returns:
        Dictionary containing:
            - 'frequencies': Array of positive frequency values (Hz)
            - 'amplitudes': Array of amplitude values
            - 'phases': Array of phase values (radians)
            - 'fft_complex': Raw complex FFT output (positive frequencies only)
    """
    signal_array = np.array(signal)
    n = len(signal_array)

    fft_complex = np.fft.rfft(signal_array)
    frequencies = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    amplitudes = np.abs(fft_complex) / n
    amplitudes[1:-1] *= 2  # Double non-DC, non-Nyquist components
    phases = np.angle(fft_complex)

    
    return {
        "frequencies": frequencies,
        "amplitudes": amplitudes,
        "phases": phases,
        "fft_complex": fft_complex,
    }


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