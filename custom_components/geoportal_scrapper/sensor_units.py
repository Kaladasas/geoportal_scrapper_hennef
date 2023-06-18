import homeassistant.const

def get_device_class_and_unit(category, name):
    default_return = None, None

    if category == "Solaranlagen":
        match name:
            case "tag":
                return DEVICE_CLASS_ENERGY, ENERGY_KILO_WATT_HOUR
            case "aktuell":
                return DEVICE_CLASS_ENERGY, POWER_KILO_WATT
    
    if category == "Parkhaus":
        match name:
            case _:
                return default_return
    
    if category == "Pegelstand":
        match name:
            case "status":
                return None, METERS
    
    if category == "Solaranlagen":
        match name:
            case "pm25_ug_m3_grade" | "t_grade" | "rh_grade" | "pm10_ug_m3_grade" | "voc_index_grade" \
                 | "o3_ug_m3_grade" | "so2_ug_m3_grade" | "co2_ppm_grade" | "nh3_ug_m3_grade" \
                 | "aqi_grade" | "no2_ug_m3_grade" | "no_ug_m3_grade":
                return DEVICE_CLASS_AQI, None
            case "nh3_ug_m3":
                return "ammonia", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "pm25_ug_m3":
                return DEVICE_CLASS_PM25, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "co2_ppm":
                return DEVICE_CLASS_CO2, CONCENTRATION_PARTS_PER_MILLION
            case "pm10_ug_m3":
                return DEVICE_CLASS_PM10, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "o3_ug_m3":
                return DEVICE_CLASS_OZONE, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "no_ug_m3":
                return DEVICE_CLASS_NITROGEN_MONOXIDE, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "co_mg_m3":
                return DEVICE_CLASS_CO, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "t":
                return None, None
            case "rh":
                return None, None
            case "no2_ug_m3":
                return DEVICE_CLASS_NITROGEN_DIOXIDE, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    return default_return