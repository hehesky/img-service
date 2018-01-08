# Image Service Deployment Instructions

## 1.User UI
By default an EC2 instance loaded with User UI is running (tagged as "flask-dev"), with nginx serving HTTP requests and can be reach by the load balancer's public DNS address. 

In case that the flask-dev instance is not running, take the following steps:

- Start flask-dev instance
- Connect to flask-dev through ssh (use key-par "flask-dev.pem" and username "ec2-user")
- Start Nginx (as ec2-user)
    
        sudo service nginx start

- Start flask webapp
        
        nohup python ~/ece1779/run.py&

The flask-dev has its nginx configured and no need to change how nginx works.

## 2.Manage UI

By default an EC2 intance with Manage UI is running (tagged as "flask-manager"), with nginx serving HTTP requests.

Before accessing the manage UI, please take the following steps to configure Nginx on flask-manager:

- Start the instance if not running
- Connect to the instance with ssh (use key-pair flask-manager.pem)
- Edit Nginx config file
        
        sudo vim /etc/nginx/nginx.conf

- Change server_name to the instance's current public DNS address

        server_name <public DNS addr>;
- Restart Nginx

       sudo service nginx restart

       
Run the manager UI webapp as:

    sudo su apps
	cd ~/ece1779_manager
	workon myapp    
	python run.py&
        
Make sure the manager UI is bound to the same port as Nginx is reverse-proxying, otherwise the webapp may be unreachable outside of this instance

