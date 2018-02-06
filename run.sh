#!/bin/bash


[ -n "$UAA_CONFIG_URL" ] && curl -Lo /uaa/uaa.yml $UAA_CONFIG_URL

($CATALINA_HOME/bin/catalina.sh run) & JAVAPID=$!
trap "kill $JAVAPID; wait $JAVAPID" SIGINT SIGTERM
wait $JAVAPID