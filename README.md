# query_ntp_status
A python to query local NTP status (via ntpq -p) and return it as JSON

NTP can need quite a bit of setup and monitoring to ensure that your time is synchronised to within the desired level, especially for computer vision applications that may need image timestamps accurate to within a few milliseconds (if you need this to be within a few hundred or tens microseconds then you may need something like PPS instead!).  The first port of call to get NTP status is to manually run:

<pre>
ntpq -p
<pre/>

Which returns various status values.

This python script shells out to ntpq, parses the putput and then returns it as a JSON string, this is handy if your code or application want's to automatically monitor and report NTP status. 
