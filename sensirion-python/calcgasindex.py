

#Define Global variables
GasIndexAlgorithm_ALGORITHM_TYPE_VOC = int(0)
GasIndexAlgorithm_ALGORITHM_TYPE_NOX = int(1)
GasIndexAlgorithm_DEFAULT_SAMPLING_INTERVAL = float(1)  #in secondsds
GasIndexAlgorithm_INITIAL_BLACKOUT = float(45)
GasIndexAlgorithm_INDEX_GAIN = float(230)
GasIndexAlgorithm_SRAW_STD_INITIAL = float(50)
GasIndexAlgorithm_SRAW_STD_BONUS_VOC = float(220)
GasIndexAlgorithm_SRAW_STD_NOX = float(2000)
GasIndexAlgorithm_TAU_MEAN_HOURS = float(12)
GasIndexAlgorithm_TAU_VARIANCE_HOURS = float(12)
GasIndexAlgorithm_TAU_INITIAL_MEAN_VOC = float(20)
GasIndexAlgorithm_TAU_INITIAL_MEAN_NOX = float(1200)
GasIndexAlgorithm_INIT_DURATION_MEAN_VOC = float((3600 * 0.75))
GasIndexAlgorithm_INIT_DURATION_MEAN_NOX = float((3600 * 4.75))
GasIndexAlgorithm_INIT_TRANSITION_MEAN = float(0.01)
GasIndexAlgorithm_TAU_INITIAL_VARIANCE = float(2500)
GasIndexAlgorithm_INIT_DURATION_VARIANCE_VOC = float((3600 * 1.45))
GasIndexAlgorithm_INIT_DURATION_VARIANCE_NOX = float((3600 * 5.70))
GasIndexAlgorithm_INIT_TRANSITION_VARIANCE = float(0.01)
GasIndexAlgorithm_GATING_THRESHOLD_VOC = float(340)
GasIndexAlgorithm_GATING_THRESHOLD_NOX = float(30)
GasIndexAlgorithm_GATING_THRESHOLD_INITIAL = float(510)
GasIndexAlgorithm_GATING_THRESHOLD_TRANSITION = float(0.09)
GasIndexAlgorithm_GATING_VOC_MAX_DURATION_MINUTES = float((60 * 3))
GasIndexAlgorithm_GATING_NOX_MAX_DURATION_MINUTES = float((60 * 12))
GasIndexAlgorithm_GATING_MAX_RATIO = float(0.3)
GasIndexAlgorithm_SIGMOID_L = float(500)
GasIndexAlgorithm_SIGMOID_K_VOC = float(-0.0065)
GasIndexAlgorithm_SIGMOID_X0_VOC = float(213)
GasIndexAlgorithm_SIGMOID_K_NOX = float(-0.0101)
GasIndexAlgorithm_SIGMOID_X0_NOX = float(614)
GasIndexAlgorithm_VOC_INDEX_OFFSET_DEFAULT = float(100)
GasIndexAlgorithm_NOX_INDEX_OFFSET_DEFAULT = float(1)
GasIndexAlgorithm_LP_TAU_FAST = float(20.0)
GasIndexAlgorithm_LP_TAU_SLOW = float(500.0)
GasIndexAlgorithm_LP_ALPHA = float(-0.2)
GasIndexAlgorithm_VOC_SRAW_MINIMUM = float(20000)
GasIndexAlgorithm_NOX_SRAW_MINIMUM = float(10000)
GasIndexAlgorithm_PERSISTENCE_UPTIME_GAMMA = float((3 * 3600))
GasIndexAlgorithm_TUNING_INDEX_OFFSET_MIN = float(1)
GasIndexAlgorithm_TUNING_INDEX_OFFSET_MAX = float(250)
GasIndexAlgorithm_TUNING_LEARNING_TIME_OFFSET_HOURS_MIN = float(1)
GasIndexAlgorithm_TUNING_LEARNING_TIME_OFFSET_HOURS_MAX = float(1000)
GasIndexAlgorithm_TUNING_LEARNING_TIME_GAIN_HOURS_MIN = float(1)
GasIndexAlgorithm_TUNING_LEARNING_TIME_GAIN_HOURS_MAX = float(1000)
GasIndexAlgorithm_TUNING_GATING_MAX_DURATION_MINUTES_MIN = float(0)
GasIndexAlgorithm_TUNING_GATING_MAX_DURATION_MINUTES_MAX = float(3000)
GasIndexAlgorithm_TUNING_STD_INITIAL_MIN = float(10)
GasIndexAlgorithm_TUNING_STD_INITIAL_MAX = float(5000)
GasIndexAlgorithm_TUNING_GAIN_FACTOR_MIN = float(1)
GasIndexAlgorithm_TUNING_GAIN_FACTOR_MAX = float(1000)
GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING = float(64)
GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING  = float(8)
GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX = float(32767)


class GasIndexAlgorithmParams:

    def __init__(self):
        pass

    def __str__(self):
        pass


def GasIndexAlgorithm_init_with_sampling_interval(params: GasIndexAlgorithmParams,
        algorithm_type : int,  sampling_interval: float):
    params.mAlgorithm_Type = algorithm_type
    params.mSamplingInterval = sampling_interval
    if algorithm_type == GasIndexAlgorithm_ALGORITHM_TYPE_NOX:
        params.mIndex_Offset = GasIndexAlgorithm_NOX_INDEX_OFFSET_DEFAULT
        params.mSraw_Minimum = GasIndexAlgorithm_NOX_SRAW_MINIMUM
        params.mGating_Max_Duration_Minutes = GasIndexAlgorithm_GATING_NOX_MAX_DURATION_MINUTES
        params.mInit_Duration_Mean = GasIndexAlgorithm_INIT_DURATION_MEAN_NOX
        params.mInit_Duration_Variance = GasIndexAlgorithm_INIT_DURATION_VARIANCE_NOX
        params.mGating_Threshold = GasIndexAlgorithm_GATING_THRESHOLD_NOX
    else:
        params.mIndex_Offset = GasIndexAlgorithm_VOC_INDEX_OFFSET_DEFAULT
        params.mSraw_Minimum = GasIndexAlgorithm_VOC_SRAW_MINIMUM
        params.mGating_Max_Duration_Minutes = GasIndexAlgorithm_GATING_VOC_MAX_DURATION_MINUTES
        params.mInit_Duration_Mean = GasIndexAlgorithm_INIT_DURATION_MEAN_VOC
        params.mInit_Duration_Variance = GasIndexAlgorithm_INIT_DURATION_VARIANCE_VOC
        params.mGating_Threshold = GasIndexAlgorithm_GATING_THRESHOLD_VOC
    params.mIndex_Gain = GasIndexAlgorithm_INDEX_GAIN
    params.mTau_Mean_Hours = GasIndexAlgorithm_TAU_MEAN_HOURS
    params.mTau_Variance_Hours = GasIndexAlgorithm_TAU_VARIANCE_HOURS
    params.mSraw_Std_Initial = GasIndexAlgorithm_SRAW_STD_INITIAL
    GasIndexAlgorithm_reset(params)


def GasIndexAlgorithm_init(params: GasIndexAlgorithmParams, algorithm_type: int):
    GasIndexAlgorithm_init_with_sampling_interval(params, algorithm_type, GasIndexAlgorithm_DEFAULT_SAMPLING_INTERVAL)


def GasIndexAlgorithm_reset(params: GasIndexAlgorithmParams):
    params.mUptime = float(0)
    params.mSraw = float(0)
    params.mGas_Index = 0
    GasIndexAlgorithm__init_instances(params)


def GasIndexAlgorithm__init_instances(params: GasIndexAlgorithmParams):
    GasIndexAlgorithm__mean_variance_estimator__set_parameters(params)
    GasIndexAlgorithm__mox_model__set_parameters(
        params, GasIndexAlgorithm__mean_variance_estimator__get_std(params),
        GasIndexAlgorithm__mean_variance_estimator__get_mean(params));
    if (params.mAlgorithm_Type == GasIndexAlgorithm_ALGORITHM_TYPE_NOX):
            GasIndexAlgorithm__sigmoid_scaled__set_parameters(params, GasIndexAlgorithm_SIGMOID_X0_NOX,
                GasIndexAlgorithm_SIGMOID_K_NOX,
                GasIndexAlgorithm_NOX_INDEX_OFFSET_DEFAULT)
    else:
        GasIndexAlgorithm__sigmoid_scaled__set_parameters(
            params, GasIndexAlgorithm_SIGMOID_X0_VOC,
            GasIndexAlgorithm_SIGMOID_K_VOC,
            GasIndexAlgorithm_VOC_INDEX_OFFSET_DEFAULT)
    GasIndexAlgorithm__adaptive_lowpass__set_parameters(params)

'''
void GasIndexAlgorithm_get_sampling_interval(
    const GasIndexAlgorithmParams* params, float* sampling_interval) {
    *sampling_interval = params->mSamplingInterval;
}

void GasIndexAlgorithm_get_states(const GasIndexAlgorithmParams* params,
                                  float* state0, float* state1) {
    *state0 = GasIndexAlgorithm__mean_variance_estimator__get_mean(params);
    *state1 = GasIndexAlgorithm__mean_variance_estimator__get_std(params);
    return;
}
'''

def GasIndexAlgorithm_set_states(params: GasIndexAlgorithmParams, state0: float, state1: float):
    GasIndexAlgorithm__mean_variance_estimator__set_states(
        params, state0, state1, GasIndexAlgorithm_PERSISTENCE_UPTIME_GAMMA)
    GasIndexAlgorithm__mox_model__set_parameters(
        params, GasIndexAlgorithm__mean_variance_estimator__get_std(params),
        GasIndexAlgorithm__mean_variance_estimator__get_mean(params))
    params.mSraw = state0;


def GasIndexAlgorithm_set_tuning_parameters(params: GasIndexAlgorithmParams, index_offset: int,
        learning_time_offset_hours: int, learning_time_gain_hours: int,
        gating_max_duration_minutes: int, std_initial: int, gain_factor: int):

    params.mIndex_Offset = float(index_offset)
    params.mTau_Mean_Hours = float(learning_time_offset_hours)
    params.mTau_Variance_Hours = float(learning_time_gain_hours)
    params.mGating_Max_Duration_Minutes = float(gating_max_duration_minutes)
    params.mSraw_Std_Initial = float(std_initial)
    params.mIndex_Gain = float(gain_factor)
    GasIndexAlgorithm__init_instances(params)


'''
void GasIndexAlgorithm_get_tuning_parameters(
    const GasIndexAlgorithmParams* params, int32_t* index_offset,
    int32_t* learning_time_offset_hours, int32_t* learning_time_gain_hours,
    int32_t* gating_max_duration_minutes, int32_t* std_initial,
    int32_t* gain_factor) {

    *index_offset = ((int32_t)(params->mIndex_Offset));
    *learning_time_offset_hours = ((int32_t)(params->mTau_Mean_Hours));
    *learning_time_gain_hours = ((int32_t)(params->mTau_Variance_Hours));
    *gating_max_duration_minutes =
        ((int32_t)(params->mGating_Max_Duration_Minutes));
    *std_initial = ((int32_t)(params->mSraw_Std_Initial));
    *gain_factor = ((int32_t)(params->mIndex_Gain));
    return;
}
'''

def GasIndexAlgorithm_process(params: GasIndexAlgorithmParams, sraw: int) -> int:
    #according to the original c code: value is returned via pointer int32_t* gas_index 
    
    if params.mUptime <= GasIndexAlgorithm_INITIAL_BLACKOUT:
        params.mUptime = params.mUptime + params.mSamplingInterval
    else:
        if (sraw > 0) and (sraw < 65000): 
            if (sraw < (params.mSraw_Minimum + 1)):
                sraw = (params.mSraw_Minimum + 1)
            elif (sraw > (params.mSraw_Minimum + 32767)): 
                sraw = (params.mSraw_Minimum + 32767)
            
            params.mSraw = float(sraw - params.mSraw_Minimum)
        
        if ((params.mAlgorithm_Type ==
              GasIndexAlgorithm_ALGORITHM_TYPE_VOC) or
             GasIndexAlgorithm__mean_variance_estimator__is_initialized(params)):
            params.mGas_Index = GasIndexAlgorithm__mox_model__process(params, params.mSraw)
            params.mGas_Index = GasIndexAlgorithm__sigmoid_scaled__process(params, params.mGas_Index);
        else:
            params.mGas_Index = params.mIndex_Offset
        
        params.mGas_Index = GasIndexAlgorithm__adaptive_lowpass__process(params, params.mGas_Index)
        if (params.mGas_Index < 0.5): 
            params.mGas_Index = 0.5
        
        if (params.mSraw > 0.0):
            GasIndexAlgorithm__mean_variance_estimator__process(params,params.mSraw)
            GasIndexAlgorithm__mox_model__set_parameters(params,
            GasIndexAlgorithm__mean_variance_estimator__get_std(params),
                GasIndexAlgorithm__mean_variance_estimator__get_mean(params))
          
    gas_index = int(params.mGas_Index + 0.5)
    return gas_index

    
def GasIndexAlgorithm__mean_variance_estimator__set_parameters(params: GasIndexAlgorithmParams):

    params.m_Mean_Variance_Estimator___Initialized = False
    params.m_Mean_Variance_Estimator___Mean = 0.0
    params.m_Mean_Variance_Estimator___Sraw_Offset = 0.0
    params.m_Mean_Variance_Estimator___Std = params.mSraw_Std_Initial
    params.m_Mean_Variance_Estimator___Gamma_Mean = (((GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING *
           GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING) *
          (params.mSamplingInterval / 3600.0)) /
         (params.mTau_Mean_Hours + (params.mSamplingInterval / 3600.0)));
    params.m_Mean_Variance_Estimator___Gamma_Variance = ((GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
          (params.mSamplingInterval / 3600.0)) /
         (params.mTau_Variance_Hours + (params.mSamplingInterval / 3600.0)))
    if (params.mAlgorithm_Type == GasIndexAlgorithm_ALGORITHM_TYPE_NOX): 
        params.m_Mean_Variance_Estimator___Gamma_Initial_Mean = (((GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING *
               GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING) *
              params.mSamplingInterval) /
             (GasIndexAlgorithm_TAU_INITIAL_MEAN_NOX +
              params.mSamplingInterval))
    else: 
        params.m_Mean_Variance_Estimator___Gamma_Initial_Mean = (((GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING *
               GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING) *
              params.mSamplingInterval) /
             (GasIndexAlgorithm_TAU_INITIAL_MEAN_VOC +
              params.mSamplingInterval))
    
    params.m_Mean_Variance_Estimator___Gamma_Initial_Variance = ((GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
          params.mSamplingInterval) /
         (GasIndexAlgorithm_TAU_INITIAL_VARIANCE + params.mSamplingInterval))
    params.m_Mean_Variance_Estimator__Gamma_Mean = 0.0;
    params.m_Mean_Variance_Estimator__Gamma_Variance = 0.0;
    params.m_Mean_Variance_Estimator___Uptime_Gamma = 0.0;
    params.m_Mean_Variance_Estimator___Uptime_Gating = 0.0;
    params.m_Mean_Variance_Estimator___Gating_Duration_Minutes = 0.0;


def GasIndexAlgorithm__mean_variance_estimator__set_states(params: GasIndexAlgorithmParams, 
        mean: float, std: float,  uptime_gamma: float):

    params._Mean_Variance_Estimator___Mean = mean
    params.m_Mean_Variance_Estimator___Std = std
    params.m_Mean_Variance_Estimator___Uptime_Gamma = uptime_gamma
    params.m_Mean_Variance_Estimator___Initialized = true



def GasIndexAlgorithm__mean_variance_estimator__get_std(params: GasIndexAlgorithmParams)-> float:
    return params.m_Mean_Variance_Estimator___Std

def GasIndexAlgorithm__mean_variance_estimator__get_mean(params: GasIndexAlgorithmParams)-> float:
    return (params.m_Mean_Variance_Estimator___Mean +
            params.m_Mean_Variance_Estimator___Sraw_Offset)

def GasIndexAlgorithm__mean_variance_estimator__is_initialized(params: GasIndexAlgorithmParams) -> bool: 
    return params.m_Mean_Variance_Estimator___Initialized


