import mysettings

def ht_in_percent(percentage) :  # Pass the % value
    return (mysettings.HEIGHT / 100) * percentage

def width_percent(percentage):
    return (mysettings.WIDTH/100) * percentage