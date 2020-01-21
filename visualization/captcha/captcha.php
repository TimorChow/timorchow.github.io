<?php
include('captcha-gen.php');
session_start();
$captcha = new captcha();
$_SESSION['captcha_keystring'] = $captcha->getKeyString();