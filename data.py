import boto3

def list_all_resources():
    # Get a list of all regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    
    for region in regions:
        print(f"\nChecking resources in region: {region}")
        
        # Create clients for each service in the specific region
        ec2 = boto3.client('ec2', region_name=region)
        ec2_resource = boto3.resource('ec2', region_name=region)
        vpn_client = boto3.client('ec2', region_name=region)
        
        # a) List NAT Gateways
        print("\nNAT Gateways:")
        try:
            nat_gateways = ec2.describe_nat_gateways()['NatGateways']
            if nat_gateways:
                for ngw in nat_gateways:
                    print(f"  - NAT Gateway ID: {ngw['NatGatewayId']}")
            else:
                print("  No NAT Gateways found.")
        except Exception as e:
            print(f"  Error listing NAT Gateways: {e}")
        
        # b) List Elastic IPs
        print("\nElastic IPs:")
        try:
            elastic_ips = ec2.describe_addresses()['Addresses']
            if elastic_ips:
                for eip in elastic_ips:
                    print(f"  - Public IP: {eip['PublicIp']}, Allocation ID: {eip.get('AllocationId')}")
            else:
                print("  No Elastic IPs found.")
        except Exception as e:
            print(f"  Error listing Elastic IPs: {e}")
        
        # c) List Endpoints
        print("\nEndpoints:")
        try:
            endpoints = ec2.describe_vpc_endpoints()['VpcEndpoints']
            if endpoints:
                for endpoint in endpoints:
                    print(f"  - Endpoint ID: {endpoint['VpcEndpointId']}, Service Name: {endpoint['ServiceName']}")
            else:
                print("  No Endpoints found.")
        except Exception as e:
            print(f"  Error listing Endpoints: {e}")
        
        # d) List Site-to-Site VPN connections
        print("\nSite-to-Site VPN Connections:")
        try:
            vpn_connections = vpn_client.describe_vpn_connections()['VpnConnections']
            if vpn_connections:
                for vpn in vpn_connections:
                    print(f"  - VPN Connection ID: {vpn['VpnConnectionId']}")
            else:
                print("  No Site-to-Site VPN connections found.")
        except Exception as e:
            print(f"  Error listing VPN Connections: {e}")
        
        # e) List Transit Gateways
        print("\nTransit Gateways:")
        try:
            transit_gateways = ec2.describe_transit_gateways()['TransitGateways']
            if transit_gateways:
                for tg in transit_gateways:
                    print(f"  - Transit Gateway ID: {tg['TransitGatewayId']}")
            else:
                print("  No Transit Gateways found.")
        except Exception as e:
            print(f"  Error listing Transit Gateways: {e}")
        
        # f) List EC2 instances
        print("\nEC2 Instances:")
        try:
            instances = ec2_resource.instances.all()
            instance_count = 0
            for instance in instances:
                print(f"  - Instance ID: {instance.id}, State: {instance.state['Name']}")
                instance_count += 1
            if instance_count == 0:
                print("  No EC2 instances found.")
        except Exception as e:
            print(f"  Error listing EC2 instances: {e}")

if __name__ == "__main__":
    list_all_resources()
