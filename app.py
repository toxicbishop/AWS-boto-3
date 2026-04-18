from flask import Flask, render_template, request, redirect, url_for, flash
import boto3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flashing messages

def get_ec2_client():
    return boto3.client('ec2', region_name='us-east-1')

@app.route('/')
def index():
    client = get_ec2_client()
    instances = []
    try:
        response = client.describe_instances()
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                name = "Unnamed"
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break
                
                instances.append({
                    'id': instance['InstanceId'],
                    'name': name,
                    'ip': instance.get('PublicIpAddress', instance.get('PrivateIpAddress', 'N/A')),
                    'state': instance['State']['Name'],
                    'type': instance['InstanceType']
                })
        error = None
    except Exception as e:
        instances = []
        error = str(e)
    
    return render_template('test.html', instances=instances, error=error)

@app.route('/action/<action>/<instance_id>')
def instance_action(action, instance_id):
    client = get_ec2_client()
    try:
        if action == 'start':
            client.start_instances(InstanceIds=[instance_id])
            flash(f"Successfully started instance {instance_id}", "success")
        elif action == 'stop':
            client.stop_instances(InstanceIds=[instance_id])
            flash(f"Successfully stopped instance {instance_id}", "info")
        elif action == 'reboot':
            client.reboot_instances(InstanceIds=[instance_id])
            flash(f"Successfully rebooted instance {instance_id}", "warning")
    except Exception as e:
        flash(f"Error {action}ing instance {instance_id}: {str(e)}", "danger")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        print("Starting in HTTPS mode...")
        app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
    else:
        print("Starting in HTTP mode (Run 'make certs' to enable HTTPS)...")
        app.run(debug=True)
