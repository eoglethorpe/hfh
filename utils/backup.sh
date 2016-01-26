zip -r /home/ec2-user/code/backup /home/ec2-user/code/omk/public/*
aws s3 cp /home/ec2-user/code/backup.zip s3://hfh-proj/public-backups/$(date +%y)/$(date +%m)/$(date +%d)/
rm /home/ec2-user/code/backup.zip
