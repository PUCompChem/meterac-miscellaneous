import numpy as np
import math
import os.path
from datetime import datetime, timezone

metrics_info = ["Single line metrics for a frequency interval {f1,f2,...,fk}",
                "  with signal points/intensities {S(f1),S(f2),...,S(fk)}:",
                "  -----------------------------------------------",
                "  mean - the mean intensity for the frequency interval: mean{S(fi)|i=1,2,...,k}  [dB].",
                "  span - the dynamic span for the frequency interval: max{S(fi)} - min{S(fi)}  [dB]",
                "  entr - the entropy of the frequency interval, based on bins of 0.5 dB",
                "",
                "Group metrics for a set of m lines {S(f1,j),S(f2,j),...,S(fk,j) | j = 1,2,...,m}:",
                "  for each i: delta(fi) = max{S(fi,j) | j=1,...,m} - min{S(fi,j) | j=1,...,m}",
                "  for each j: RMS(j) = sqrt(sum{S(fi,j)^2 | i=1,...,k}})",
                "  -----------------------------------------------",
                "  d_max - maximal delta = max{delta(fi)| i=1,...,k}}",
                "  d_rms - RMS over all deltas = sqrt(sum{delta(fi)^2 | i=1,...,k}})",
                "  s_rms_min - minimal RMS signal = min{RMS(j) | j = 1,...,m}",
                "  s_rms_max - maximal RMS signal = max{RMS(j) | j = 1,...,m}",
                "  s_rms_span - rms_max - rms_min}",
                "  s_rms_span - the entropy of the group of signal rms, based on bins of 0.1 dB"
                ]

class MetricsFlags:
    def __init__(self):
        self.calc_mean = False
        self.calc_span = False
        self.calc_entr = False
        self.calc_d_max = False
        self.calc_d_rms = False
        self.calc_s_rms_min = False
        self.calc_s_rms_max = False
        self.calc_s_rms_span = False
        self.calc_s_rms_entr = False
        self.errors =[]
    
    def set_all_single_line_metrics(self, flag: bool):
        self.calc_mean = flag
        self.calc_span = flag
        self.calc_entr = flag

    def set_all_group_metrics(self, flag: bool):
        self.calc_d_max = flag
        self.calc_d_rms = flag
        self.calc_s_rms_min = flag
        self.calc_s_rms_max = flag
        self.calc_s_rms_span = flag
        self.calc_s_rms_entr = flag
  
    def set_all_flags(self, flag: bool):
        self.set_all_group_metrics(flag)
        self.set_all_single_line_metrics(flag)

    def has_single_line_metrics(self) -> bool:
        if self.calc_mean or self.calc_span or self.calc_entr:
            return True
        return False

    def has_group_metrics(self) -> bool:
        if self.calc_d_max or self.calc_d_rms or \
           self.calc_s_rms_min or self.calc_s_rms_max or \
            self.calc_s_rms_span or self.calc_s_rms_entr:
               return True
        return False    

def get_all_metrics_flags() -> MetricsFlags:
    mi = MetricsFlags()
    mi.set_all_flags(True)
    return mi

def extract_metrics_flags_from_string(s: str, splitter: str = "," ) -> MetricsFlags:
    mi = MetricsFlags()
    tokens = s.split(splitter)   
    for tok in tokens:
        t = tok.strip()
        if t != '':
            if t.lower() == "all":
                mi.set_all_flags(True)
            elif t.lower() == "sl":
                mi.set_all_single_line_metrics(True)
            elif t.lower() == "grp":
                mi.set_all_group_metrics(True)
            elif t.lower() == "mean" or t.lower() == "mean-on":
                mi.calc_mean = True
            elif t.lower() == "mean-off":
                mi.calc_mean = False
            elif t.lower() == "span" or t.lower() == "span-on":
                mi.calc_span = True
            elif t.lower() == "span-off":
                mi.calc_span = False       
            else:
                mi.errors.append("Incorrect metrics: " + t)    
    return mi

class Metrics:
    def __init__(self):
        self.designations = [] #list[str]
        self.values = [] #list[float]
        self.time_begin = 0
        self.time_end = 0
        self.single_line_metrics = True

class SpectralData:
    def __init__(self):        
        self.frequencies = None #list[float]
        self.data_matrix = []
        self.sweep_start = []  #stored as string
        self.sweep_stop = []   #stored as string
        self.utc_start = []
        self.utc_stop = []
        self.frequency_unit = "MHz"
        self.frequency_factor = 1.0e-6
        self.errors = []
        self.min_spectrum = None   #np NDArray
        self.max_spectrum = None   #np NDArray
        self.average_spectrum = None  #np NDArray
        self.delta_spectrum = None  #np NDArray
        self.frequency_intervals = None
            
    def check_matrix_dimensions(self):
        min_len = len(self.data_matrix[0])
        max_len = len(self.data_matrix[0])
        min_row = 1 #1-based indexed
        max_row = 1 #1-based indexed
        for i in range(len(self.data_matrix)):            
            n =  len(self.data_matrix[i]) 
            #print((i+1), " --> ", n)
            if min_len > n:
                min_len = n
                min_row = i+1
            if max_len < n:
                max_len = n
                max_row = i+1
        print("frequencies len: ", len(self.frequencies))
        print("data_matrix len: ", len(self.data_matrix))
        print("data_matrix min row len: ", min_len, " at row: ", min_row)
        print("data_matrix max row len: ", max_len, " at row: ", max_row)
        print("sweep_start len: ", len(self.sweep_start))
        print("sweep_stop len: ", len(self.sweep_stop))

    def get_x_ticks_with_step(self, xIndexStep: int) -> list[int]:
        return range(0,len(self.frequencies), xIndexStep)

    def get_x_ticks_labels(self, x_indices: list[int]) -> list[str]:
        labels = []
        for i in x_indices:
            labels.append(str(self.frequencies[i]*self.frequency_factor) 
                          + " " + self.frequency_unit)
        return labels
    
    def get_y_ticks_with_step(self, yIndexStep: int) -> list[int]:
        return range(0, len(self.sweep_stop), yIndexStep)
    
    def get_y_ticks_labels(self, y_indices: list[int]) -> list[str]:
        labels = []
        for i in y_indices:
            labels.append(str(self.sweep_stop[i]))
        return labels
    
    def print_errors(self):
        for err in self.errors:
            print(err)
    
    def calc_basic_spectrum_statistics(self):
        z = np.array(self.data_matrix, dtype='float32')
        self.average_spectrum = np.mean(z, axis=0)
        self.min_spectrum = np.min(z, axis=0)
        self.max_spectrum = np.max(z, axis=0)
        self.delta_spectrum =  self.max_spectrum - self.min_spectrum  

    def get_even_frequency_intervals(self, numIntervals: int):
        self.frequency_intervals = get_even_slice_intervals(len(self.frequencies), numIntervals)
    
    def calc_metrics_for_single_line(self, line_num: int, metr_flags: MetricsFlags) -> Metrics:
        #Get single line as a np array
        z1 = np.array(self.data_matrix[line_num], dtype='float32')
         
        metr = Metrics()
        metr.time_begin = self.utc_start[line_num]
        metr.time_end = self.utc_stop[line_num]
        n = len(self.frequency_intervals)

        # Interval mean
        if metr_flags.calc_mean:
            for i in range(n):
                i_begin, i_end = self.frequency_intervals[i]
                z1_i = z1[i_begin:i_end]
                i_mean = np.mean(z1_i)
                metr.values.append(i_mean)
                metr.designations.append("mean_" + str(i+1))

        # Interval span
        if metr_flags.calc_span:
            for i in range(n):
                i_begin, i_end = self.frequency_intervals[i]
                z1_i = z1[i_begin:i_end]
                i_min = np.min(z1_i)
                i_max = np.max(z1_i)
                i_span = i_max - i_min
                metr.values.append(i_span)
                metr.designations.append("span_" + str(i+1))
        
        # Interval entropy
        if metr_flags.calc_entr:
            for i in range(n):
                i_begin, i_end = self.frequency_intervals[i]
                z1_i = z1[i_begin:i_end]
                i_entr = calc_entropy_based_on_even_bins(z1_i, 1.0) #bin_delta 0.5dB
                metr.values.append(i_entr)
                metr.designations.append("entr_" + str(i+1))
        return metr

    def calc_metrics_for_group_of_lines(self, start_line: int, end_line: int, metr_flags: MetricsFlags) -> Metrics:
        #Getting group lines in a np array
        z = np.array(self.data_matrix[start_line:end_line], dtype='float32')
        #z_mean = np.mean(z, axis=0)
        z_min = np.min(z, axis=0)
        z_max = np.max(z, axis=0)
        z_delta = z_max - z_min        
        #print("min: ", z_min[:a])
        #print("max: ", z_max[:a])
        #print("delta: ", z_delta[:a])

        metr = Metrics()
        metr.single_line_metrics = False
        n = len(self.frequency_intervals)
        metr.time_begin = self.utc_start[start_line]
        metr.time_end = self.utc_stop[end_line-1]
        
        # Interval delta max
        if metr_flags.calc_d_max:
            for i in range(n):
                i_begin, i_end = self.frequency_intervals[i]            
                #print("interval indices: ", i_begin, i_end)
                d = z_delta[i_begin:i_end]
                max_d = np.max(d)
                metr.values.append(max_d)
                metr.designations.append("d_max_" + str(i+1))
        
        # Interval delta RMS
        if metr_flags.calc_d_rms:
            for i in range(n):
                i_begin, i_end = self.frequency_intervals[i]
                d = z_delta[i_begin:i_end]
                rms_d = np.sqrt(np.mean(d**2))
                metr.values.append(rms_d)
                metr.designations.append("d_rms_" + str(i+1))
        
        # RMS singanl statistics
        s_rms_min_values = []
        s_rms_min_designations = []
        s_rms_max_values = []
        s_rms_max_designations = []
        s_rms_span_values = []
        s_rms_span_designations = []
        s_rms_entr_values = []
        s_rms_entr_designations = []
        for i in range(n):
            i_begin, i_end = self.frequency_intervals[i]
            # Get interval columns
            z1 = z[...,i_begin:i_end]
            #RMS per rows
            z1_2 = z1**2
            ms =  np.mean(z1_2, axis=1)  #an array with means for each row
            rms = ms**0.5
            #print("rms: ", rms)
            rms_min = np.min(rms)
            rms_max = np.max(rms)
            rms_span = rms_max - rms_min
            rms_entr = calc_entropy_based_on_even_bins(rms, 0.1) #bin_delta 0.1dB
            s_rms_min_values.append(rms_min)
            s_rms_min_designations.append("s_rms_min_" + str(i+1))
            s_rms_max_values.append(rms_max)
            s_rms_max_designations.append("s_rms_max_" + str(i+1))
            s_rms_span_values.append(rms_span)
            s_rms_span_designations.append("s_rms_span_" + str(i+1))
            s_rms_entr_values.append(rms_entr)
            s_rms_entr_designations.append("s_rms_entr_" + str(i+1))
        
        if metr_flags.calc_s_rms_min:
            metr.values.extend(s_rms_min_values)
            metr.designations.extend(s_rms_min_designations)
        
        if metr_flags.calc_s_rms_max:
            metr.values.extend(s_rms_max_values)
            metr.designations.extend(s_rms_max_designations)
        
        if metr_flags.calc_s_rms_span:
            metr.values.extend(s_rms_span_values)
            metr.designations.extend(s_rms_span_designations)
        
        if metr_flags.calc_s_rms_entr:
            metr.values.extend(s_rms_entr_values)
            metr.designations.extend(s_rms_entr_designations)
                
        return metr
    
    def calc_metrics_by_groups(self, group_size: int, metr_flags: MetricsFlags) -> list[Metrics]:
        num_lines = n = len(self.data_matrix)
        cur_line = 0
        metr_arr = []
        while cur_line < num_lines:
            end_line = cur_line + group_size
            if end_line > num_lines:
                end_line = num_lines
            if end_line - cur_line < group_size/2:
                break #if the last group of lines is not "full enough" it is omitted
            metr = self.calc_metrics_for_group_of_lines(cur_line, end_line, metr_flags)
            metr_arr.append(metr)
            cur_line = cur_line + group_size
        return metr_arr    

    def calc_metrics_for_entire_data_matrix(self, metr_flags: MetricsFlags) -> Metrics:
        return self.calc_metrics_for_group_of_lines(0, len(self.data_matrix) -1, metr_flags)


class SpectraProcessConfig:
    def __init__(self):
        #self.tasks_string = None
        self.group_time_step = 600 #in seconds
        self.group_num_of_lines = 10
        self.num_of_frequency_intervals = 6
        self.append_to_output = True
        self.input = None
        self.output = None
        self.output_number_format = "{:0.2f}"
        self.parse_errors = []


def get_timestamp(time_string: str, dt_format: str) -> int:
    dt = datetime.strptime(time_string, dt_format).replace(tzinfo=timezone.utc)
    return dt.timestamp()
    

def get_even_slice_intervals(num_objects: int, num_intervals: int) -> list[object]:
    #generates interval in slicing manner (last index to be excluded)
    intervals = []
    n = num_objects
    delta = n / num_intervals
    prevEndValue = 0
    for i in range(num_intervals):
        interval = []
        interval.append(prevEndValue)
        endValue = math.floor((i+1) * delta)
        if endValue > n:
            endValue = n
        interval.append(endValue)
        prevEndValue = endValue
        intervals.append(interval)

    return intervals

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





