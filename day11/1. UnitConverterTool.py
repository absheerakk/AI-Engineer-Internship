def convert(expression):
    parts = expression.lower().split()

    if len(parts) != 4 or parts[2] != "to":
        return f"No conversion found for: {expression}"
    
    try:
        value = float(parts[0])
    except ValueError:
        return f"No conversion found for: {expression}"
    
    from_unit = parts[1]
    to_unit = parts[3]

    if from_unit == "km" and to_unit == "miles":
        return f"{value:g} km = {value * 0.621371:.3f} miles"

    elif from_unit == "miles" and to_unit == "km":
        return f"{value:g} miles = {value / 0.621371:.3f} km"

    elif from_unit == "kg" and to_unit == "lbs":
        return f"{value:g} kg = {value * 2.20462:.3f} lbs"

    elif from_unit == "lbs" and to_unit == "kg":
        return f"{value:g} lbs = {value / 2.20462:.3f} kg"

    elif from_unit == "celsius" and to_unit == "fahrenheit":
        fahrenheit = (value * 9 / 5) + 32
        return f"{value:g} Celsius = {fahrenheit:.1f} Fahrenheit"

    elif from_unit == "fahrenheit" and to_unit == "celsius":
        celsius = (value - 32) * 5 / 9
        return f"{value:g} Fahrenheit = {celsius:.1f} Celsius"

    return f"No conversion found for: {expression}"

print(convert("5 km to miles"))
print(convert("100 celsius to fahrenheit"))
print(convert("70 kg to lbs"))
print(convert("10 parsecs to lightyears"))
