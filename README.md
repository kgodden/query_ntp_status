# query_ntp_status
A python script to query local NTP status (via ntpq -p) and return the fields as a JSON string.

NTP can need quite a bit of setup and monitoring to ensure that your time is synchronised to within the desired level, especially for computer vision applications that may need image timestamps accurate to within a few milliseconds (if you need this to be within a few hundred or tens microseconds then you may need something like PPS instead!).  The first port of call to get NTP status is to manually run:

<pre>
ntpq -p
</pre>

Which returns various status values, like this:

<pre>
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
+bray.walcz.net  140.203.204.77   2 u   44   64  377   10.453   -3.605   0.337
*185.121.25.166  85.199.214.99    2 u   54   64  377   19.904   -4.803   0.500
</pre>

This python script shells out to ntpq, parses the putput and then returns it as a JSON string, this is handy if your code or application wants to automatically monitor and report NTP status. It will try to the the data for the current time source (the line that starts with * ), if that fails it returns data for the first line it finds (assuming that this will become the promary source when synchronised).

More info can be found [here](https://www.ridgesolutions.ie/index.php/2015/04/29/python-script-to-query-ntp-status-and-return-it-as-json/).

Usage:
------

<pre>
./query_ntp_status.py

{"query_result": "ok", "data": {"remote": "bray.walcz.net", "refid": "140.203.204.77", "st": "2", "t": "u", "when": "14", "poll": "64", "reach": "377", "delay": "10.601", "offset": "-3.535", "jitter": "0.447"}}
</pre>
