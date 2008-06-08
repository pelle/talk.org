#!/bin/sh
# Original author Lindsey Simon

cat static/stylesheets/style.css > /tmp/talk_compiled.css.tmp;
java -jar tools/yuicompressor-2.3.4.jar \
     --type css /tmp/talk_compiled.css.tmp \
     -o static/stylesheets/talk_compiled.css;
echo "MINIFIED CSS! (static/stylesheets/talk_compiled.css)";
head static/stylesheets/talk_compiled.css;
echo "-------------------------------"

#cat static/javascripts/jquery.blockUI.js \
cat  static/javascripts/talk.js > /tmp/talk_compiled.js.tmp
java -jar tools/yuicompressor-2.3.4.jar \
     --type js /tmp/talk_compiled.js.tmp \
     -o static/javascripts/talk_compiled.js;
echo "MINIFIED JS! (static/javascripts/talk_compiled.js)";
head static/javascripts/talk_compiled.js;
echo "-------------------------------"

echo "Deploying to App Engine servers...";
appcfg.py update .
echo "DONE!"
echo "";

