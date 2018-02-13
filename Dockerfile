FROM tomcat:8.0.49-jre8

COPY tomcat/tomcat-users.xml /usr/local/tomcat/conf
COPY tomcat/setenv.sh /usr/local/tomcat/bin

COPY target/lib/cloudfoundry-identity-uaa-4.8.3.war .
RUN unzip -d /usr/local/tomcat/webapps/cloudfoundry-identity-uaa-4.8.3 cloudfoundry-identity-uaa-4.8.3.war
RUN rm cloudfoundry-identity-uaa-4.8.3.war

COPY tomcat/uaa.yml /usr/local/tomcat/uaa.yml
COPY tomcat/saml-idp.xml /usr/local/tomcat/webapps/cloudfoundry-identity-uaa-4.8.3/WEB-INF/spring/

EXPOSE 8080

