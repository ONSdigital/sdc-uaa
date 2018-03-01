FROM tomcat:8.0.49-jre8

ENV UAA_CONFIG_PATH /uaa
ADD uaa.yml /uaa/uaa.yml

RUN rm -rf /usr/local/tomcat/webapps/ROOT
RUN rm -rf /usr/local/tomcat/webapps/host-manager
RUN rm -rf /usr/local/tomcat/webapps/manager
RUN rm -rf /usr/local/tomcat/webapps/examples
RUN rm -rf /usr/local/tomcat/webapps/docs

COPY target/lib/cloudfoundry-identity-uaa-4.10.0.war /usr/local/tomcat/webapps/ROOT.war

EXPOSE 8080


