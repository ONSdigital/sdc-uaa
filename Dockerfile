FROM java:8
MAINTAINER ONS

ENV UAA_CONFIG_PATH /uaa
ENV CATALINA_HOME /tomcat

ADD run.sh /tmp/
ADD uaa.yml /uaa/uaa.yml
RUN chmod +x /tmp/run.sh

RUN wget -q http://mirror.ox.ac.uk/sites/rsync.apache.org/tomcat/tomcat-8/v8.5.27/bin/apache-tomcat-8.5.27.tar.gz
RUN wget -qO- https://www.apache.org/dist/tomcat/tomcat-8/v8.5.27/bin/apache-tomcat-8.5.27.tar.gz.md5 | md5sum -c -

RUN tar zxf apache-tomcat-8.5.27.tar.gz
RUN rm apache-tomcat-8.5.27.tar.gz


RUN mkdir /tomcat
RUN mv apache-tomcat-8.5.27/* /tomcat
RUN rm -rf /tomcat/webapps/*

RUN wget --no-check-certificate http://central.maven.org/maven2/org/cloudfoundry/identity/cloudfoundry-identity-uaa/2.7.1/cloudfoundry-identity-uaa-2.7.1.war
RUN mv cloudfoundry-identity-uaa-2.7.1.war  /tomcat/webapps/ROOT.war

EXPOSE 8080

CMD ["/tmp/run.sh"]