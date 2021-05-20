#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json
RTL_433_ARGUMENTS="$(bashio::config 'rtl_433_arguments')"

/discovery_proxy.py&

echo /usr/local/bin/rtl_433 $RTL_433_ARGUMENTS
/usr/local/bin/rtl_433 $RTL_433_ARGUMENTS
