<?php

function printcard($title, $name, $single = '', $eight = '_A7', $sixteen = '_A8') {

  $folder = 'kort/'.$name.'/';

  $output = '<h2>'.$title.'</h2>';
  $output .= '<img src="'.$folder.$name.'.png" />';
  $output .= '<div class="download">Download ';
  if ($single !== false) {
  	$output .=   '<a class="single" title="enkeltside" href="'.$folder.$name.$single.'.pdf" /></a>';
  }
  if ($eight !== false) {
  	$output .=   '<a class="eight" title="A7" href="'.$folder.$name.$eight.'.pdf" /></a>';
  }
  if ($sixteen !== false) {
  	$output .=   '<a class="sixteen" title="A8" href="'.$folder.$name.$sixteen.'.pdf" /></a>';
  }
  $output .= '</div>';

  $output = '<div class="card"><div class="wrapper">'.$output.'</div></div>';

  return $output;
}

// jimpoz at jimpoz dot com
// http://dk1.php.net/array_multisort
function array_msort($array, $cols)
{
    $colarr = array();
    foreach ($cols as $col => $order) {
        $colarr[$col] = array();
        foreach ($array as $k => $row) { $colarr[$col]['_'.$k] = strtolower($row[$col]); }
    }
    $eval = 'array_multisort(';
    foreach ($cols as $col => $order) {
        $eval .= '$colarr[\''.$col.'\'],'.$order.',';
    }
    $eval = substr($eval,0,-1).');';
    eval($eval);
    $ret = array();
    foreach ($colarr as $col => $arr) {
        foreach ($arr as $k => $v) {
            $k = substr($k,1);
            if (!isset($ret[$k])) $ret[$k] = $array[$k];
            $ret[$k][$col] = $array[$k][$col];
        }
    }
    return $ret;

}
