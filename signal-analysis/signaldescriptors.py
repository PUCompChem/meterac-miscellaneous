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
    Descriptor("band_rms_energy")    
    ]

default_frequency_band_list = [
    [0,1],
    [1,2],
    [2,3],
    [3,4],
    [4,5]
]

class DescriptorValue:
    def __init__(self, floatValue: float = None, listValue: list[float] = None, textValue: str = None,
                  errorMsg: str = None, info: str = None):
        self.floatValue = floatValue
        self.listValue = listValue
        self.textValue = textValue
        self.errorMsg = errorMsg
        self.info = info
    
    def value_to_string(self) -> str:
        val = ""
        if self.floatValue != None:
            val = f"{self.floatValue:.2f}"
        if self.textValue != None:
            val = self.textValue
        if self.listValue != None:
            n = len(self.listValue)
            for i in range(n):
                val += f"{self.listValue[i]:.2f}"
                if i < n-1:
                    val +=" "
        return val

class CalcSignalDescriptors:
    def __init__(self, signal: list[float], 
                 descriptors: list[str] = None, 
                 sample_rate: float = 10,
                 entropy_bin_delta: float = 1000,
                 frequency_bands: list[list[float]] = None):        
        self.signal = signal
        self.sample_rate =  sample_rate    #signal sample rate in  Hz (how many measurements per second)
        self.entropy_bin_delta = entropy_bin_delta
        if descriptors != None:
            #TODO
            self.descriptors = None
        else:                
            self.descriptors = descriptor_list  #by default entire descriptor list is used
        self.fft_result = None
        if frequency_bands == None:
            self.frequency_bands = default_frequency_band_list
        else:
            self.frequency_bands = frequency_bands

    def calculate(self) -> dict[str, DescriptorValue]:
        dvalues = {}
        if self.descriptors == None:
            return dvalues
        for d in self.descriptors:
            if d.name == "band_rms_energy":
                for b in self.frequency_bands:                    
                    dv = self.calculateBandRMSEnergy(b[0], b[1])
                    dvalues[dv.info] = dv   #dv.info is used for descriptor name
            else:
                dv = self.calculateDescriptor(d.name)
                dvalues[d.name] = dv
        return dvalues
    
    def calculateDescriptor(self, name: str, params:list[float] = None) -> DescriptorValue:       
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

    def get_fft_result(self) -> dict:
        if self.fft_result == None:
            self.fft_result = calculate_rfft(self.signal, 10)
        return self.fft_result

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
    
    def calculateBandRMSEnergy(self, f1:float, f2:float) -> DescriptorValue:        
        fft_res = self.get_fft_result()
        f1_ = f1 if f1 > 0 else 0.001  #correction for 0 Hz
        f2_ = f2 if f2 < fft_res["frequencies"][-1] else (fft_res["frequencies"][-1]-0.001)  #correction for last frequency
        val = rms_energy_in_band(fft_res, f1_, f2_)
        dv_info = "rms_en_"+ str(f1) + "_" + str(f2) + "Hz"
        return DescriptorValue(floatValue = val, info = dv_info)

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



def rms_energy_in_band(fft_result: dict, f1: float, f2: float) -> float:
    """
    Calculate the RMS amplitude within a specified frequency band [f1, f2].
    Args:
        fft_result: Dictionary returned by calculate_rfft(), containing
                    'frequencies' and 'amplitudes' arrays
        f1: Lower bound of the frequency band (Hz)
        f2: Upper bound of the frequency band (Hz)

    Returns:
        RMS amplitude within the specified frequency band
        or None in case of incorrect frequency band
    """
    
    if f1 < 0 or f2 < 0:
        return None

    frequencies = fft_result["frequencies"]
    amplitudes = fft_result["amplitudes"]

    max_frequency = frequencies[-1]  #last element
    
    if f1 > max_frequency or f2 > max_frequency:
        return None

    mask = (frequencies >= f1) & (frequencies <= f2)
    band_amplitudes = amplitudes[mask]

    # Loop version — works but slow
    #band_amplitudes = []
    #for i in range(len(frequencies)):
    #    if f1 <= frequencies[i] <= f2:
    #        band_amplitudes.append(amplitudes[i])

    if len(band_amplitudes) == 0:
        return None

    return np.sqrt(np.mean(band_amplitudes ** 2))



def find_peaks(fft_result: dict, threshold: float = 0.1, min_distance: int = None) -> dict:
    """
    Find peaks in the FFT amplitude spectrum using threshold and minimum distance logic.

    Args:
        fft_result:     Dictionary returned by calculate_rfft()
        threshold:      Minimum amplitude to consider as a peak, expressed as a
                        fraction of the maximum amplitude (default: 0.1 = 10%)
        min_distance:   Minimum number of bins between two peaks;
                        if min_distance is not specified,  min_distance = 5% of length

    Returns:
        Dictionary containing:
            - 'frequencies': Array of peak frequencies (Hz)
            - 'amplitudes':  Array of peak amplitudes
            - 'indices':     Array of peak indices in the original array
    """
    frequencies = fft_result["frequencies"]
    amplitudes  = fft_result["amplitudes"]

    if threshold < 0 or threshold > 1:
        raise ValueError("Threshold must be between 0 and 1")
        
    # default min_distance: 5% of spectrum length
    if min_distance is None:
        min_distance = max(1, len(amplitudes) // 20)

    if min_distance < 1:
        min_distance = 1

    # Step 1: apply threshold — ignore bins below threshold * max amplitude
    abs_threshold = threshold * np.max(amplitudes)
    above_threshold = amplitudes >= abs_threshold  #numpy masking

    # Step 2: find local maxima — a bin is a peak if it is greater than its neighbors
    is_local_max = np.zeros(len(amplitudes), dtype=bool)
    for i in range(1, len(amplitudes) - 1):
        if amplitudes[i] > amplitudes[i - 1] and amplitudes[i] > amplitudes[i + 1]:
            is_local_max[i] = True

    # Step 3: combine both conditions
    peak_mask = above_threshold & is_local_max
    peak_indices = np.where(peak_mask)[0]   #taking element 0 since np.where return tuple

    # Step 4: enforce minimum distance between peaks — if two peaks are too
    # close, keep only the stronger one
    if min_distance > 1 and len(peak_indices) > 1:
        filtered_indices = [peak_indices[0]]     # add first peak
        for idx in peak_indices[1:]:  # iterate remaining peaks
            if idx - filtered_indices[-1] >= min_distance:    # check whether peack is far enough?
                filtered_indices.append(idx)  # add new peak 
            elif amplitudes[idx] > amplitudes[filtered_indices[-1]]:  # peak is closer, but is it stronger?
                filtered_indices[-1] = idx   # replace previous peak with the new one
        peak_indices = np.array(filtered_indices)

    return {
        "frequencies": frequencies[peak_indices],
        "amplitudes":  amplitudes[peak_indices],
        "indices":     peak_indices
    }