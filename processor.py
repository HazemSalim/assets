class EnergyProcessor:
    def __init__(self, data_accessor):
        self.data_accessor = data_accessor

    def calculate_reduced_energy_demand(self, asset_id):
        try:
            # Get asset information
            asset = self.data_accessor.get_asset(asset_id)
            if not asset:
                return None

            # Initialize energy demand dictionary and total energy demand
            energy_demand = {energy_type["name"]: 0 for energy_type in self.data_accessor.data.get("energy_type", [])}
            total_energy_demand = 0

            # Get asset-specific energy demand and energy output
            asset_energy_demand = self.data_accessor.get_asset_energy_demand(asset_id)
            energy_output = self.data_accessor.get_asset_energy_output(asset_id)

            # Calculate reduced energy demand for each energy type
            for demand in asset_energy_demand:
                energy_type_name = self.data_accessor.get_energy_type_name(demand.get("energy_type"))
                energy_system_name = self.data_accessor.get_energy_system_name(next((system.get("energy_system") for system in self.data_accessor.data.get("asset_energy_system", []) if system.get("asset") == asset_id and system.get("energy_type") == demand.get("energy_type")), None))
                
                # Skip if energy type or energy system name is not found
                if energy_type_name is None or energy_system_name is None:
                    continue

                # Calculate demand value considering energy output
                demand_value = max(0, demand.get("energy_demand", 0) - energy_output if energy_system_name == "electricity" else demand.get("energy_demand", 0))
                # Update energy demand dictionary and total energy demand
                energy_demand[energy_type_name] += demand_value
                total_energy_demand += demand_value

            # Calculate energy output reduction percentage
            energy_output_reduction = (1 - (total_energy_demand / sum(demand.get("energy_demand", 0) for demand in asset_energy_demand))) * 100 if total_energy_demand > 0 else 0

            # Return calculated results
            return {
                "name": asset.get("name", ""),
                "energy_types": energy_demand,
                "total_energy_demand": total_energy_demand,
                "energy_output_reduction": energy_output_reduction
            }
        except Exception as e:
            # Handle any unexpected errors
            print(f"Error processing energy demand for asset {asset_id}: {e}")
            return None
