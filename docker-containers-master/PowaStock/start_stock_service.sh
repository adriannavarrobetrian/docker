#!/bin/bash

export STOCK_DB_SUBPROTOCOL="mysql"
export STOCK_DB_SUBNAME="//localhost:3306/stock"
export STOCK_DB_USER="root"
export STOCK_DB_PASSWORD="#hermesdb"

java -jar target/powa-stock-service-0.1.0-SNAPSHOT-standalone.jar
