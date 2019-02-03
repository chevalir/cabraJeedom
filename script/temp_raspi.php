<?php
    $temp = shell_exec("cat /sys/class/thermal/thermal_zone0/temp");
    $temp = $temp / 1000;
    $temp = round($temp,1);
	$temp = $temp - 19;
    echo $temp;
?>
