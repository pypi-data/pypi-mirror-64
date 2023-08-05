import typing

# The data gives the value for co2 emitted in case of petrol and diesel in gm/litre
co2_gasoline = 2347.698
co2_diesel = 2689.273

# defining the function for evaluating the co2 emitted
def co2Emitted(carType : str,mileage : float,distance : float) -> float:
    if carType == 'gasoline' or carType == 'petrol':
        co2_emission = (co2_gasoline*distance)/mileage
    elif carType == 'diesel':
        co2_emission = (co2_diesel*distance)/mileage
    return co2_emission