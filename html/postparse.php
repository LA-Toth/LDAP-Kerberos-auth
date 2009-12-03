#!/usr/bin/php
<?php

$fdate = fopen("date.tex", "r");
$date = fread($fdate, 4096);
fclose($fdate);
#$date = str_replace("\\", '',str_replace('{', '', preg_replace('/(date|})/', '', $date)));
$date = preg_replace("/.*date{([^}]*).*/ms", '\1', $date);


$fh = fopen("html/main/main.html", "r");
if (!$fh) die ('nincs meg a file');
$buffer = '';
$buffer  = fread($fh, 4096);
print preg_replace( '%</head[^>]*>.*<body[^>]*>[^<]*<small.*ALT="\$[^"]*copyright\$"></span>.*(2005-2007)%mxs', '
<style type="text/css">
.center { text-align: center }
</style>
</head>
<body>
<h1 class="center">LDAP és Kerberos alapú rendszer megvalósítása</h1>
<p class="center LARGE">Tóth László Attila</p>
<p class="center">' . $date . '</p>
<small>\1', $buffer);
while (!feof($fh)) {
    print fread($fh, 4096);
}
fclose ($fh);
