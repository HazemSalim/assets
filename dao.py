import json

class DataAccessor:
    def __init__(self, filename):
        try:
            # Load JSON data from the file
            with open(filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            # Handle file not found error
            print(f"Error: File '{filename}' not found.")
            self.data = {}  

    def get_asset(self, asset_id):
        try:
            # Search for asset with the given ID
            for asset in self.data["asset"]:
                if asset["id"] == asset_id:
                    return asset   
            return None   
        except KeyError:
            # Handle missing or incorrect data structure in JSON file
            print("Error: Missing or incorrect data structure in JSON file.")
            return None

    def get_asset_energy_demand(self, asset_id):
        try:
            # Retrieve energy demand data for the given asset ID
            return [asset for asset in self.data.get("asset_energy_demand", []) if asset.get("asset") == asset_id]
        except KeyError:
            # Handle missing or incorrect data structure in JSON file
            print("Error: Missing or incorrect data structure in JSON file.")
            return []

    def get_asset_energy_output(self, asset_id):
        try:
            # Retrieve energy output for the given asset ID
            return next((asset["energy_output"] for asset in self.data.get("asset_energy_output", []) if asset.get("asset") == asset_id), 0)
        except (StopIteration, KeyError):
            # Handle missing or incorrect data structure in JSON file
            print("Error: Missing or incorrect data structure in JSON file.")
            return 0

    def get_energy_system_name(self, energy_system_id):
        try:
            # Retrieve energy system name for the given ID
            return next((system["name"] for system in self.data.get("energy_system", []) if system.get("id") == energy_system_id), None)
        except StopIteration:
            # Handle energy system not found
            print("Error: Energy system not found.")
            return None
        except KeyError:
            # Handle missing or incorrect data structure in JSON file
            print("Error: Missing or incorrect data structure in JSON file.")
            return None

    def get_energy_type_name(self, energy_type_id):
        try:
            # Retrieve energy type name for the given ID
            return next((energy["name"] for energy in self.data.get("energy_type", []) if energy.get("id") == energy_type_id), None)
        except StopIteration:
            # Handle energy type not found
            print("Error: Energy type not found.")
            return None
        except KeyError:
            # Handle missing or incorrect data structure in JSON file
            print("Error: Missing or incorrect data structure in JSON file.")
            return None
