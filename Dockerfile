FROM tomcat:8.0.49-jre8

ENV UAA_CONFIG_PATH /uaa
ADD tomcat/uaa-tomcat.yml /uaa/uaa.yml

COPY tomcat/tomcat-users.xml /usr/local/tomcat/conf
COPY tomcat/setenv.sh /usr/local/tomcat/bin

COPY target/lib/cloudfoundry-identity-uaa-4.8.3.war .
RUN unzip -d /usr/local/tomcat/webapps/cloudfoundry-identity-uaa-4.8.3 cloudfoundry-identity-uaa-4.8.3.war
RUN rm cloudfoundry-identity-uaa-4.8.3.war

COPY tomcat/saml-idp.xml /usr/local/tomcat/webapps/cloudfoundry-identity-uaa-4.8.3/WEB-INF/spring/

EXPOSE 8080

