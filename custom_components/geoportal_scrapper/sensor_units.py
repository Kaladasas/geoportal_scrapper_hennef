import homeassistant.const as ha_const

def get_device_class_and_unit(category, name):
    """This function will return the classes and unit of measurements of our sensors"""
    default_return = None, None

    if category == "Solaranlagen":
        match name:
            case "tag":
                return ha_const.DEVICE_CLASS_ENERGY, ha_const.UnitOfEnergy.KILO_WATT_HOUR
            case "aktuell":
                return ha_const.DEVICE_CLASS_ENERGY, ha_const.UnitOfEnergy.KILO_WATT_HOUR
    
    if category == "Parkhaus":
        match name:
            case _:
                return default_return
    
    if category == "Pegelstand":
        match name:
            case "status":
                return ha_const.LENGTH, ha_const.UnitOfLength.METERS
    
    if category == "Breeze":
        match name:
            case "pm25_ug_m3_grade" | "t_grade" | "rh_grade" | "pm10_ug_m3_grade" | "voc_index_grade" \
                 | "o3_ug_m3_grade" | "so2_ug_m3_grade" | "co2_ppm_grade" | "nh3_ug_m3_grade" \
                 | "aqi_grade" | "no2_ug_m3_grade" | "no_ug_m3_grade":
                return ha_const.DEVICE_CLASS_AQI, None
            case "nh3_ug_m3":
                return "ammonia", ha_const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "pm25_ug_m3":
                return ha_const.DEVICE_CLASS_PM25, ha_const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "co2_ppm":
                return ha_const.DEVICE_CLASS_CO2, ha_const.CONCENTRATION_PARTS_PER_MILLION
            case "pm10_ug_m3":
                return ha_const.DEVICE_CLASS_PM10, ha_const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "o3_ug_m3":
                return ha_const.DEVICE_CLASS_OZONE, ha_const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "no_ug_m3":
                return ha_const.DEVICE_CLASS_NITROGEN_MONOXIDE, ha_const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
            case "co_mg_m3":
                return ha_const.DEVICE_CLASS_CO, ha_const.CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER
            case "t":
                return None, None
            case "rh":
                return None, None
            case "no2_ug_m3":
                return ha_const.DEVICE_CLASS_NITROGEN_DIOXIDE, ha_const.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    return default_return