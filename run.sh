#!/usr/bin/with-contenv bashio

declare host
declare password
declare port
declare username
declare config_path
declare rtl_433_arguments

config_path=/data/options.json

if bashio::services.available "mqtt"; then
    host=$(bashio::services "mqtt" "host")
    password=$(bashio::services "mqtt" "password")
    port=$(bashio::services "mqtt" "port")
    username=$(bashio::services "mqtt" "username")
else
    bashio::log.info "mqtt is not available"
    exit 1
fi

#rtl_433_arguments=$("$rtl_433_arguments") "$(bashio::config 'rtl_433_arguments')"
rtl_433_arguments="-F mqtt://$host:$port,user=$username,pass=$password"

/discovery_proxy.py&

echo /usr/local/bin/rtl_433 $rtl_433_arguments
/usr/local/bin/rtl_433 $rtl_433_arguments
