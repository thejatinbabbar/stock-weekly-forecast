mkdir -p ~/.streamlit/

primColor="#F63366"
backColor="#FFFFFF"
secColor="#F0F2F6"
textColor="#262730"
font="sans serif"

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
[theme]\n\
primaryColor = "${primColor}"\n\
backgroundColor = "${backColor}"\n\
secondaryBackgroundColor = "${secColor}"\n\
textColor = "${textColor}"\n\
font = "${font}"\n\
\n\
" > ~/.streamlit/config.toml
