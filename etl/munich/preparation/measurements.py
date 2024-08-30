def merge_measurements(height, width, length) -> str | None:
    '''This function merges the height, width and length into a single string'''
    measures = [height, width, length]
    measures = [m for m in measures if m is not None]

    if len(measures) == 0:
        return None

    measurements = " x ".join([str(m) for m in measures])
    return measurements
