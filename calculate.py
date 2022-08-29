import extract_temperature

def cal_value(filename: str):
    temperature_np = extract_temperature.extract_temperature(filename)
    mouse_list = list()
    for i in range(temperature_np.shape[0]):
        for j in range(temperature_np.shape[1]):
            if (temperature_np[i][j] >= 29 and temperature_np[i][j] <= 40):
                mouse_list.append(temperature_np[i][j])
    avg_value = 0
    max_value = 0
    min_value = 0
    if (len(mouse_list) != 0):
        avg_value = sum(mouse_list)/len(mouse_list)
        max_value = max(mouse_list)
        min_value = min(mouse_list)
    return avg_value, max_value, min_value