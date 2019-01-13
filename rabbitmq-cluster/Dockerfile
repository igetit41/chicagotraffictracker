#rabbitmq
FROM rabbitmq:3.7.8-management
ENV rabbitServer_mqadmin mqadmin
ENV rabbitServer_mqadminpassword mqadminpassword

#Add init.sh file
ADD init.sh /init.sh

#Define default command
RUN ["chmod", "+x", "/init.sh"]
CMD ["/init.sh"]