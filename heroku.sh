#!/bin/sh
wget https://github.com/v2fly/v2ray-core/releases/latest/download/v2ray-linux-64.zip
unzip v2ray-linux-64.zip
chmod +x v2ray v2ctl
cat > config.json << EOF
{
    "inbounds": [
        {
            "port": $PORT,
            "protocol": "vless",
            "settings": {
	        "decryption": "none",
                "clients": [
                    {
                        "id": "75d1df6e-caeb-4880-8f11-058c1cb436fe"
                    }
                ]
            },
            "streamSettings": {
                "network": "ws"
            }
        }
    ],
    "outbounds": [
        {
            "protocol": "freedom"
        }
    ]
}
EOF
./v2ray -config config.json