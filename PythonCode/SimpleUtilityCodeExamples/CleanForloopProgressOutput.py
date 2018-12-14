from IPython.display import clear_output
import numpy as np
import timeit

start = timeit.default_timer()
for i in range(0, 500):
    clear_output(wait= True)
    i += 1
    stop =timeit.default_timer()

    if ((i/500) * 100) < 5:
        expected_time = "Calculating..."
    else:
        time_perc = timeit.default_timer()
        expected_time =np.round(((time_perc - start) / (i/500))/60, 2)
    print("Progress:", np.round((i/500) * 100,2), "%")
    print("Current run time:", np.round((stop - start) /60, 2)," minutes")
    print("Expected run time;", expected_time, "minutes")