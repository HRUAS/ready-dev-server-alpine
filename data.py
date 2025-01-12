import boto3
from prettytable import PrettyTable

def list_all_resources():
    # Initialize the table
    table = PrettyTable()
    table.field_names = [
        "Region",
        "NAT Gateways",
        "Elastic IPs",
        "Endpoints",
        "VPN Connections",
        "Transit Gateways",
        "EC2 Instances"
    ]

    # Get all regions
    ec2_client = boto3.client("ec2")
    regions = [region["RegionName"] for region in ec2_client.describe_regions()["Regions"]]

    for region in regions:
        print(f"Checking resources in region: {region}")

        # Initialize clients for the current region
        ec2 = boto3.client("ec2", region_name=region)
        ec2_resource = boto3.resource("ec2", region_name=region)

        # Initialize counts and details
        nat_gateways = "No NAT Gateways"
        elastic_ips = "No Elastic IPs"
        endpoints = "No Endpoints"
        vpn_connections = "No VPN Connections"
        transit_gateways = "No Transit Gateways"
        ec2_instances = "No EC2 Instances"

        # Get NAT Gateways
        try:
            nat_gateways_list = ec2.describe_nat_gateways()["NatGateways"]
            if nat_gateways_list:
                nat_gateways = f"{len(nat_gateways_list)} found"
        except Exception as e:
            nat_gateways = f"Error: {str(e)}"

        # Get Elastic IPs
        try:
            elastic_ips_list = ec2.describe_addresses()["Addresses"]
            if elastic_ips_list:
                elastic_ips = f"{len(elastic_ips_list)} found"
        except Exception as e:
            elastic_ips = f"Error: {str(e)}"

        # Get Endpoints
        try:
            endpoints_list = ec2.describe_vpc_endpoints()["VpcEndpoints"]
            if endpoints_list:
                endpoints = f"{len(endpoints_list)} found"
        except Exception as e:
            endpoints = f"Error: {str(e)}"

        # Get VPN Connections
        try:
            vpn_connections_list = ec2.describe_vpn_connections()["VpnConnections"]
            if vpn_connections_list:
                vpn_connections = f"{len(vpn_connections_list)} found"
        except Exception as e:
            vpn_connections = f"Error: {str(e)}"

        # Get Transit Gateways
        try:
            transit_gateways_list = ec2.describe_transit_gateways()["TransitGateways"]
            if transit_gateways_list:
                transit_gateways = f"{len(transit_gateways_list)} found"
        except Exception as e:
            transit_gateways = f"Error: {str(e)}"

        # Get EC2 Instances
        try:
            instances = ec2_resource.instances.all()
            instance_count = sum(1 for _ in instances)
            ec2_instances = f"{instance_count} found" if instance_count > 0 else "No EC2 Instances"
        except Exception as e:
            ec2_instances = f"Error: {str(e)}"

        # Add row to table
        table.add_row([region, nat_gateways, elastic_ips, endpoints, vpn_connections, transit_gateways, ec2_instances])

    # Print the table
    print(table)

if __name__ == "__main__":
    list_all_resources()
