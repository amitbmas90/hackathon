import boto3
import json
changebatch={
        "Comment": "Automatic DNS update",
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": "gohack.free",
                    "Type": "A",
                    "Region": "ap-southeast-1",
                    "TTL": 300,
                    "ResourceRecords": [
                        {
                            "Value": "52.221.255.43"
                        }
                    ]
                }
            }
        ]
}
changebatch2={
                'Comment': 'comment',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': 'gohack.free.',
                            'Type': 'A',
                            'TTL': 300,
                            #'Region': 'ap-southeast-1',
                            'ResourceRecords': [
                                {
                                    'Value': '54.169.230.239'
                                },
                                ],
                            }
                    },
                    ]
                }

class Update():


   def update(self,ip):
         self.session=boto3.session.Session(profile_name='default', region_name="ap-southeast-1")
         #session=boto3.session.Session(profile_name='default', region_name="ap-southeast-1")
         #ec2_client = session.client('route53')
         self.ec2_client =self.session.client('route53')
         response = self.ec2_client.change_resource_record_sets(
         HostedZoneId='Z25CEXSDPLKK7B',
         ChangeBatch={
                'Comment': 'comment',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': 'gohack.free.',
                            'Type': 'A',
                            'TTL': 300,
                            #'Region': 'ap-southeast-1',
                            'ResourceRecords': [
                                {
                                    'Value': ip
                                },
                                ],
                            }
                    },
                    ]
                })

if __name__=="__main__":
    updater = Update()
    updater.update()
