CONFIG="config.ini"

if ! [ -f "$CONFIG" ]; then
    python3 generateConfig.py
    echo "A configutation file has been generated in this folder."
    echo "Please take a moment to fill it out."
    echo "Otherwise the message will not be sent properly and/or may contain irrelivant information."
    exit 0
else
    python3 weatherSender.py
fi

