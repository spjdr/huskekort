<?php error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE); ?>
<?php include('lib/functions.php'); ?>
<html manifest="huskekort.manifest">
<head>
  <title>Huskekort</title>
  <base href="http://ny.spjdr.dk/huskekort/">
  <meta charset="utf-8">
  <meta name="description" content="Huskekort for spejdere. Alle de gode tips og tricks med pionering, madlavning, koder, signalering, iagttagelse og lejrliv lige ved hånden.">
  <meta name="apple-mobile-web-app-capable" content="yes"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
  <meta property="og:title" content="Huskekort for spejdere"/>
  <meta property="og:url" content="http://ny.spjdr.dk/huskekort/"/>
  <meta property="og:image" content="http://ny.spjdr.dk/huskekort/assets/img/huskekort-icon-big.png"/>
  <link rel="apple-touch-icon" href="assets/img/huskekort-icon.png" />
  <link rel="apple-touch-icon" sizes="57x57" href="assets/img/huskekort-icon-57x57.png" />
  <link rel="apple-touch-icon" sizes="72x72" href="assets/img/huskekort-icon-72x72.png" />
  <link rel="apple-touch-icon" sizes="76x76" href="assets/img/huskekort-icon-76x76.png" />
  <link rel="apple-touch-icon" sizes="114x114" href="assets/img/huskekort-icon-114x114.png" />
  <link rel="apple-touch-icon" sizes="120x120" href="assets/img/huskekort-icon-120x120.png" />
  <link rel="apple-touch-icon" sizes="144x144" href="assets/img/huskekort-icon-144x144.png" />
  <link rel="apple-touch-icon" sizes="152x152" href="assets/img/huskekort-icon-152x152.png" />
  <link rel="stylesheet" href="assets/css/screen.css" />
</head>
<body>
<div class="title">
  <h1>Huskekort</h1>
  <div class="tagline">fra <a href="http://spjdrpedia.dk">spjdrpedia.dk</a></div>
</div>

<div class="cards">

<?php $f = file_get_contents('kort/cards.json'); ?>
<?php $cards = json_decode($f,true); ?>

<?php $cards = array_msort($cards,array('emne'=>SORT_ASC,'titel'=>SORT_ASC)); ?>

<?php foreach($cards as $card): ?>
  <?php echo printcard($card['titel'],$card['name']); ?>
<?php endforeach; ?>
<div class="visualclear"></div>

<div class="all">
<h2>Alle kort</h2>
<?php echo printcard('Alle kort','alle','',false,false); ?>
<?php echo printcard('Alle kort','alleA7',false,'',false); ?>
<?php echo printcard('Alle kort','alleA8',false,false,''); ?>
</div>

<?php $f = file_get_contents('kort/meta.json'); ?>
<?php $meta = json_decode($f,true); ?>

<div class="visualclear"></div>
</div>
<div class="footer">
  <p>
  Indholdet er udgivet under 
  <a rel="nofollow" href="http://creativecommons.org/licenses/by-sa/3.0/deed.da">Creative Commons Navngivelse/Del på samme vilkår 3.0</a>
  <p>
  Alle huskekort må altså frit downloades, printes, bruges, ændres, genudgives eller på anden måde videreformidles på betingelse af at de genudgives under en tilsvarende licens og at <a href="credit.php">alle kunstnerne krediteres</a>.
  </p>
  <p>
    Sidst opdateret <?php echo $meta['updated'] ?>
  </p>
</div>

</body>
</html>
