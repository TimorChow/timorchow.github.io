<?php
require_once(dirname(__FILE__).'/captcha-config.php');
class captcha{
 function captcha(){
 require(dirname(__FILE__).'/captcha-config.php');
				$this->keystring='';
				for($i=0;$i<$length;$i++)
					$this->keystring.=$use_symbols{mt_rand(0,$use_symbols_len-1)};
			$im=imagecreatefromgif(dirname(__FILE__)."/back.gif");
			$width = imagesx($im);
			$height = imagesy($im);
			$rc=mt_rand(120,140);
			$font_color = imagecolorresolve($im, $rc, $rc,$rc);
			$px =$margin_left;
   			For($i=0;$i<$length;$i++){
									imagettftext($im,$font_size,0,$px, $margin_top,$font_color,dirname(__FILE__)."/CARTOON8.TTF",$this->keystring[$i]);
   									$px+=$font_width+mt_rand($rand_bsimb_min,$rand_bsimb_max); 
								}
		
		$h_y=mt_rand(0,$height);
		$h_y1=mt_rand(0,$height);
		imageline($im,mt_rand(0,20),$h_y,mt_rand($width-20,$width),$h_y1,$font_color);
		imageline($im,mt_rand(0,20),$h_y,mt_rand($width-20,$width),$h_y1,$font_color);
		$h_y=mt_rand(0,$height);
		$h_y1=mt_rand(0,$height);
		imageline($im,mt_rand(0,20),$h_y,mt_rand($width-20,$width),$h_y1,$font_color);
		imageline($im,mt_rand(0,20),$h_y,mt_rand($width-20,$width),$h_y1,$font_color);
		image_make_pomexi($im,50,80);
		
		$rand=mt_rand(0,1);
		if ($rand)$rand=-1; else $rand=1;
		wave_region($im,0,0,$width,$height,$rand*mt_rand($amplitude_min,$amplitude_max),mt_rand(30,40));
		header('Expires: Sat, 17 May 2008 05:00:00 GMT'); 
		header('Cache-Control: no-store, no-cache, must-revalidate'); 
		header('Cache-Control: post-check=0, pre-check=0', FALSE); 
		header('Pragma: no-cache');
		if(function_exists("imagejpeg")){
			header("Content-Type: image/jpeg");
			imagejpeg($im, null, $jpeg_quality);
		}else if(function_exists("imagegif")){
			header("Content-Type: image/gif");
			imagegif($im);
		}else if(function_exists("imagepng")){
			header("Content-Type: image/x-png");
			imagepng($im);
		}
 }
 	function getKeyString(){
		return $this->keystring;
	}
}

function wave_region($img, $x, $y, $width, $height,$amplitude = 4.5,$period = 30){
        $mult = 2;
        $img2 = imagecreatetruecolor($width * $mult, $height * $mult);
        imagecopyresampled ($img2,$img,0,0,$x,$y,$width * $mult,$height * $mult,$width, $height);
        for ($i = 0;$i < ($width * $mult);$i += 2)
           imagecopy($img2,$img2,$x + $i - 2,$y + sin($i / $period) * $amplitude,$x + $i,$y, 2,($height * $mult));
        imagecopyresampled($img,$img2,$x,$y,0,0,$width, $height,$width * $mult,$height * $mult);
        imagedestroy($img2);
 }

function image_make_pomexi(&$im,$size,$colch){
   $max_x=imagesx($im);
   $max_y=imagesy($im);
   for ($i=0;$i<=$colch;$i++){
   $size=mt_rand(10,$size);
				$px1=mt_rand(0,$max_x);
				$py1=mt_rand(0,$max_y);
				$col=imagecolorresolve($im, 255, 255, 255); 
				$pk1=mt_rand(-1,1);
				$pk2=mt_rand(-1,1);
    			imageline($im,$px1,$py1,$px1+$size*$pk1,$py1+$size*$pk2,$col);
			}	
}