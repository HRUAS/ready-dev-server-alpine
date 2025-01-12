#!/usr/bin/python3
import boto3
from prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

def get_resources_for_region(region):
    # Initialize clients for the current region
    ec2 = boto3.client("ec2", region_name=region)
    ec2_resource = boto3.resource("ec2", region_name=region)

    # Initialize counts and details
    resources = {
        "region": region,
        "nat_gateways": "No NAT Gateways",
        "elastic_ips": "No Elastic IPs",
        "endpoints": "No Endpoints",
        "vpn_connections": "No VPN Connections",
        "transit_gateways": "No Transit Gateways",
        "ec2_instances": "No EC2 Instances"
    }

    # Get NAT Gateways
    try:
        nat_gateways_list = ec2.describe_nat_gateways()["NatGateways"]
        if nat_gateways_list:
            resources["nat_gateways"] = f"{len(nat_gateways_list)} found"
    except Exception as e:
        resources["nat_gateways"] = f"Error: {str(e)}"

    # Get Elastic IPs
    try:
        elastic_ips_list = ec2.describe_addresses()["Addresses"]
        if elastic_ips_list:
            resources["elastic_ips"] = f"{len(elastic_ips_list)} found"
    except Exception as e:
        resources["elastic_ips"] = f"Error: {str(e)}"

    # Get Endpoints
    try:
        endpoints_list = ec2.describe_vpc_endpoints()["VpcEndpoints"]
        if endpoints_list:
            resources["endpoints"] = f"{len(endpoints_list)} found"
    except Exception as e:
        resources["endpoints"] = f"Error: {str(e)}"

    # Get VPN Connections
    try:
        vpn_connections_list = ec2.describe_vpn_connections()["VpnConnections"]
        if vpn_connections_list:
            resources["vpn_connections"] = f"{len(vpn_connections_list)} found"
    except Exception as e:
        resources["vpn_connections"] = f"Error: {str(e)}"

    # Get Transit Gateways
    try:
        transit_gateways_list = ec2.describe_transit_gateways()["TransitGateways"]
        if transit_gateways_list:
            resources["transit_gateways"] = f"{len(transit_gateways_list)} found"
    except Exception as e:
        resources["transit_gateways"] = f"Error: {str(e)}"

    # Get EC2 Instances
    try:
        instances = ec2_resource.instances.all()
        instance_count = sum(1 for _ in instances)
        resources["ec2_instances"] = f"{instance_count} found" if instance_count > 0 else "No EC2 Instances"
    except Exception as e:
        resources["ec2_instances"] = f"Error: {str(e)}"

    return resources

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
    total_regions = len(regions)
    completed_regions = 0

    # Use ThreadPoolExecutor to handle multithreading
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_resources_for_region, region): region for region in regions}

        for future in as_completed(futures):
            region = futures[future]
            try:
                resources = future.result()
                # Add row to table
                table.add_row([resources["region"], resources["nat_gateways"], resources["elastic_ips"],
                               resources["endpoints"], resources["vpn_connections"], resources["transit_gateways"],
                               resources["ec2_instances"]])

                # Update progress
                completed_regions += 1
                progress = (completed_regions / total_regions) * 100
                sys.stdout.write(f"\rProgress: {completed_regions}/{total_regions} regions completed ({progress:.2f}%)")
                sys.stdout.flush()

            except Exception as e:
                print(f"\nError processing region {region}: {str(e)}")

    # Print the table
    print("\n")
    print(table)

if __name__ == "__main__":
    list_all_resources()
