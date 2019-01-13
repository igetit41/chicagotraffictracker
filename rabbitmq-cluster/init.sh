#This code will set the initial management account
( sleep 20 && \
rabbitmqctl delete_user guest 2>/dev/null && \
rabbitmqctl add_user $rabbitServer_mqadmin $rabbitServer_mqadminpassword && \
rabbitmqctl set_user_tags $rabbitServer_mqadmin administrator && \
rabbitmqctl set_permissions -p / $rabbitServer_mqadmin  ".*" ".*" ".*" && \
echo "*** User '$rabbitServer_mqadmin' with password '$rabbitServer_mqadminpassword' completed. ***" && \
echo "*** Log in the WebUI at port 15672 (example: http:/localhost:15672) ***") &

rabbitmq-server $@