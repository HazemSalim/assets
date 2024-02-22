from fastapi import FastAPI, HTTPException
from dao import DataAccessor
from processor import EnergyProcessor

app = FastAPI()

# Initialize DataAccessor and EnergyProcessor instances
data_accessor = DataAccessor("json_database.json")
energy_processor = EnergyProcessor(data_accessor)

@app.get("/")
def home():
    return "Server is running"


@app.get("/energy_demand/{asset_id}")
async def get_energy_demand(asset_id: int):
    # Call EnergyProcessor method to calculate reduced energy demand
    result = energy_processor.calculate_reduced_energy_demand(asset_id)
    if result is not None:
        return result   
    else:
        # If result is None, raise an HTTPException with status code 404 "Asset not found"
        raise HTTPException(status_code=404, detail="Asset not found")
