import streamlit as st
import openai
import re
import json
import time
import base64
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

load_dotenv()

# --- TEMPLATES & SCHEMA ---
# These templates can be edited to change branding, colors, and layout.
# Use standard HTML and inline CSS. Placeholders like {title} will be replaced.

EMAIL1_TEMPLATE = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
<!--[if gte mso 9]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width">
<!--[if !mso]><!-->
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<!--<![endif]-->
<title></title>
<!--[if !mso]><!-->
<!--<![endif]-->
<style type="text/css">
body {
margin: 0;
padding: 0;
}

table,
td,
tr {
vertical-align: top;
border-collapse: collapse;
}

* {
line-height: inherit;
}

a[x-apple-data-detectors=true] {
color: inherit !important;
text-decoration: none !important;
}
</style>
<style type="text/css" id="media-query">
 @media (max-width: 660px) {

.block-grid,
.col {
min-width: 320px !important;
max-width: 100% !important;
display: block !important;
}

.block-grid {
width: 100% !important;
}

.col {
width: 100% !important;
}

.col_cont {
margin: 0 auto;
}

img.fullwidth,
img.fullwidthOnMobile {
width: 100% !important;
}

.no-stack .col {
min-width: 0 !important;
display: table-cell !important;
}

.no-stack.two-up .col {
width: 50% !important;
}

.no-stack .col.num2 {
width: 16.6% !important;
}

.no-stack .col.num3 {
width: 25% !important;
}

.no-stack .col.num4 {
width: 33% !important;
}

.no-stack .col.num5 {
width: 41.6% !important;
}

.no-stack .col.num6 {
width: 50% !important;
}

.no-stack .col.num7 {
width: 58.3% !important;
}

.no-stack .col.num8 {
width: 66.6% !important;
}

.no-stack .col.num9 {
width: 75% !important;
}

.no-stack .col.num10 {
width: 83.3% !important;
}

.video-block {
max-width: none !important;
}

.mobile_hide {
min-height: 0px;
max-height: 0px;
max-width: 0px;
display: none;
overflow: hidden;
font-size: 0px;
}

.desktop_hide {
display: block !important;
max-height: none !important;
}
}
</style>
<style type="text/css" id="menu-media-query">
 @media (max-width: 660px) {
.menu-checkbox[type="checkbox"]~.menu-links {
display: none !important;
padding: 5px 0;
}

.menu-checkbox[type="checkbox"]~.menu-links span.sep {
display: none;
}

.menu-checkbox[type="checkbox"]:checked~.menu-links,
.menu-checkbox[type="checkbox"]~.menu-trigger {
display: block !important;
max-width: none !important;
max-height: none !important;
font-size: inherit !important;
}

.menu-checkbox[type="checkbox"]~.menu-links>a,
.menu-checkbox[type="checkbox"]~.menu-links>span.label {
display: block !important;
text-align: center;
}

.menu-checkbox[type="checkbox"]:checked~.menu-trigger .menu-close {
display: block !important;
}

.menu-checkbox[type="checkbox"]:checked~.menu-trigger .menu-open {
display: none !important;
}

#menuw19hjn~div label {
border-radius: 50% !important;
}

#menuw19hjn:checked~.menu-links {
background-color: #3fb9bc !important;
}

#menuw19hjn:checked~.menu-links a {
color: #ffffff !important;
}

#menuw19hjn:checked~.menu-links span {
color: #ffffff !important;
}
}
</style>
</head>

<body class="clean-body" style="margin: 0; padding: 0; -webkit-text-size-adjust: 100%; background-color: #f6f8f8;">
<!--[if IE]><div class="ie-browser"><![endif]-->
<table bgcolor="#f6f8f8" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="table-layout: fixed; vertical-align: top; min-width: 320px; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f6f8f8; width: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top;" valign="top" class="">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color:#f6f8f8"><![endif]-->
<div style="background-color:transparent;">
<div class="block-grid two-up no-stack" style="min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="320" style="background-color:transparent;width:320px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:5px;"><![endif]-->
<div class="col num6" style="display: table-cell; vertical-align: top; max-width: 320px; min-width: 318px; width: 320px;">
<div class="col_cont" style="width:100% !important;">
<!--[if (!mso)&(!IE)]>
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;"><!--<![endif]-->
<div align="left" class="img-container left fixedwidth" style="padding-right: 0px;padding-left: 0px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="left"><![endif]-->
<div style="font-size:1px;line-height:25px"><br>
<br>
<a href="http://www.pasona.com/" style="background-color: transparent; outline: none;" tabindex="-1" target="_blank"><img alt="Pasona" border="0" class="left fixedwidth" height="34" src="https://www2.pasona.com/l/519571/2021-11-15/gbqhvn/519571/1637023162DnRtOeCf/PNA_logo_clear_back.png" style="text-decoration-line: none; width: 187px; max-width: 100%; display: block; height: 34px; border-width: 0px;" title="Pasona" width="187"></a></div>

<div style="font-size:1px;line-height:15px">&nbsp;</div>

<!--[if mso]></td></tr></table><![endif]--></div>

<!--[if (!mso)&(!IE)]></div>
<!--<![endif]--></div>
</div>

<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td><td align="center" width="320" style="background-color:transparent;width:320px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:5px;"><![endif]-->

<div class="col num6" style="display: table-cell; vertical-align: top; max-width: 320px; min-width: 318px; width: 320px;">
<div class="col_cont" style="width:100% !important;">
<!--[if (!mso)&(!IE)]>
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;"><!--<![endif]-->
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td align="right" style="word-break: break-word; vertical-align: top; padding-top: 15px; padding-bottom: 5px; padding-left: 0px; padding-right: 0px; text-align: right; font-size: 0px;" valign="top" class=""><!--[if !mso><input class="menu-checkbox" id="menuw19hjn" style="display:none !important;max-height:0;visibility:hidden;" type="checkbox"> <!--<![endif]-->
<div class="menu-trigger" style="display:none;max-height:0px;max-width:0px;font-size:0px;overflow:hidden;"><label class="menu-label" for="menuw19hjn" style="height:36px;width:36px;display:inline-block;cursor:pointer;mso-hide:all;user-select:none;align:right;text-align:center;color:#ffffff;text-decoration:none;background-color:#3fb9bc;"><span class="menu-open" style="mso-hide:all;font-size:26px;line-height:36px;">☰</span><span class="menu-close" style="display:none;mso-hide:all;font-size:26px;line-height:36px;">✕</span></label></div>

<div class="menu-links">
<!--[if mso]>
<table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center">
<tr>
<td style="padding-top:20px;padding-right:20px;padding-bottom:15px;padding-left:20px">
<![endif]--><br>
<a href="https://form.run/ @pnaweb--UcEAWPHvAFBxyTpxf61l?utm_source=mail&amp;utm_medium=PNAnewsletter"><img align="right" alt="" border="0" height="75" src="https://www2.pasona.com/l/519571/2024-04-02/kb7phy/519571/1712093663Hbkuu8JI/CTA_Button.jpg" style="width: 300px; float: right; height: 75px; border-width: 0px; border-style: solid;" width="300"></a>
 <!--[if mso]></td></tr></table><![endif]--></div>
</td>
</tr>
</tbody>
</table>
<br>

<!--[if (!mso)&(!IE)]></div>
<!--<![endif]--></div>
</div>

<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]--></div>
</div>
</div>

<div style="background-color:#fff;">
<div class="block-grid " style="min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#fff;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="640" style="background-color:transparent;width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
<div class="col_cont" style="width:100% !important;">
<!--[if (!mso)&(!IE)]>
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;"><!--<![endif]-->
<div align="center" class="img-container center autowidth" style="padding-right: 16px;padding-left: 16px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 16px;padding-left: 16px;" align="center"><![endif]-->
<div align="center" class="img-container center autowidth" style="padding-right:16px; padding-left:16px">
<div align="center" class="img-container center autowidth" style="text-align:-webkit-center; padding-right:16px; padding-left:16px">
<p><span style="font-size:medium"><span style="line-height:inherit"><span style="color:#000000"><span style="font-family:&quot;Times New Roman&quot;"><span style="font-style:normal"><span style="font-variant-ligatures:normal"><span style="font-weight:400"><span style="white-space:normal"><span style="background-color:#ffffff"><span style="text-decoration-thickness:initial"><span style="text-decoration-style:initial"><span style="text-decoration-color:initial"><span style="line-height:inherit"><span style="font-size:20px"><span style="line-height:inherit"><strong style="line-height:inherit"><span style="line-height:inherit"><span style="font-family:Arial, Helvetica, sans-serif"><span lang="JA" style="line-height:inherit"><span style="line-height:21.4px">​​​​</span></span></span></span></strong></span></span><br style="line-height:inherit">
<a href="https://www.pasona.com/seminar/visa_111925/"><img alt="" border="0" height="315" src="https://www2.pasona.com/l/519571/2025-10-23/kcr1tr/519571/1761263724GrYzWrJK/B_For_November_2025.png" style="width: 600px; height: 315px; border-width: 0px; border-style: solid;" width="600"></a><br>
<br>
<span style="font-size:14px"><span style="line-height:inherit"><span style="line-height:inherit"><span style="font-family:Arial, Helvetica, sans-serif"><span style="line-height:14.98px"><span lang="JA" style="line-height:inherit"><span style="line-height:14.98px">​​​​​</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span><a href="https://www.pasona.com/seminar/visa_111925/"><span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><img alt="" border="0" height="50" src="https://www2.pasona.com/l/519571/2024-02-27/kb617z/519571/1709085445ZEUWJECB/output_onlinepngtools__1_.png" style="width: 200px; height: 50px; border-width: 0px; border-style: solid;" width="200"></span></span></a></p>

<p style="text-align:justify; margin-bottom:11px"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:medium"><span style="line-height:inherit"><span style="color:#000000"><span style="font-style:normal"><span style="font-variant-ligatures:normal"><span style="font-weight:400"><span style="white-space:normal"><span style="background-color:#ffffff"><span style="text-decoration-thickness:initial"><span style="text-decoration-style:initial"><span style="text-decoration-color:initial"><span style="line-height:inherit"><span style="font-size:14px"><span style="line-height:inherit">第二次トランプ政権の発足以降、移民受入れ制限の公約のもと、さまざまな大統領令が打ち出され、米国移民法のあらゆる側面で厳格化が加速しています。その影響は、日系企業が活用する各種ビザにも及び、採用や駐在員派遣に関するルールが次々と変更されるなど、米国で事業を行うすべての企業において、これまで以上に柔軟かつ迅速な対応と、的確なリスクマネジメントが求められています。<br>
&nbsp;<br>
本ウェビナーでは、移民法専門弁護士をお招きし、実際に企業から寄せられる「よくある質問 Top 5」をもとに、最新の政策動向とその実務的な対応策を解説します。</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></p>

<hr>
<p align="center"><span style="font-size:20px;"><strong><span style="font-family:Arial,Helvetica,sans-serif;">【概要】<br>
<span style="color:#000000;">第二次トランプ政権下で加速する<br>
移民政策の厳格化・在米日系企業への影響</span><br>
<span style="color:#aa2128;">～よくある質問Top 5から考える、<br>
厳格化を乗り切るための実践的ヒント～</span></span></strong></span></p>
</div>

<div style="padding-top:10px; padding-right:16px; padding-bottom:15px; padding-left:16px">
<div class="txtTinyMce-wrapper">
<table border="1" cellpadding="1" cellspacing="1" class="pd-table" style="width: 564px;">
<tbody>
<tr>
<td style="width: 103px; text-align: center;">
<p><br>
<br>
​​​​​<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><strong>日　時</strong></span></span><br>
&nbsp;</p>
</td>
<td style="width: 447px;">
<p><br>
<br>
<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">&nbsp; &nbsp;日程： 2025年11月19日（水）<br>
&nbsp; &nbsp;時間：13:00-14:00 PT/ 15:00-16:00 CT/16:00-17:00 ET</span></span><br>
&nbsp;</p>
</td>
</tr>
<tr>
<td style="width: 103px; text-align: center;">
<p><br>
<br>
<br>
<br>
​​​​​​<br>
<span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;"><strong>場　所</strong></span></span></p>
</td>
<td style="width: 447px;">
<p style="margin-bottom: 11px;"><span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="color:#000000;"><span style="line-height:107%"><span lang="JA"><span style="line-height:107%">​​</span></span></span></span><br>
<br>
&nbsp;</span></span>&nbsp; &nbsp;<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">オンラインウェビナー（ツール：ZOOM）</span></span><span style="background-color: transparent;">​​​​​</span></p>

<ul>
<li><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;">イベントご参加用のURLは、ご登録いただいた方に、<br>
開催日1営業日前にお送りいたします。</span></span></li>
<li><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;">Zoomのアプリをインストール（無料）のうえ、ご参加<br>
されることを推奨しておりますが必須ではございません。</span></span></li>
</ul>

<div style="margin-bottom: 11px;"><span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="color:#000000;"><span style="line-height:107%"><span lang="JA"><span style="line-height:107%">​​​​</span></span></span></span></span></span></div>
</td>
</tr>
<tr>
<td style="width: 103px; text-align: center;">
<p><br>
<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><strong>​​​</strong></span></span><br>
<span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;"><strong>登 壇 者</strong></span></span></p>
</td>
<td style="width: 447px;"><br>
<br>
<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">&nbsp; &nbsp;<strong>岸波　宏和氏 / Hirokazu Kishinami</strong><br>
&nbsp; &nbsp;増田・舟井・アイファート・ミッチェル法律事務所 / 弁護士</span></span><br>
<br>
&nbsp;</td>
</tr>
<tr>
<td style="width: 103px;">
<p>​​​​​<br>
<br>
<br>
<span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;"><span style="background-color: transparent; text-align: center;">&nbsp; &nbsp; &nbsp; &nbsp;</span><strong style="background-color: transparent; font-size: 14px; font-family: Arial, Helvetica, sans-serif; text-align: center;">詳</strong><strong>　</strong><strong style="background-color: transparent; font-size: 14px; font-family: Arial, Helvetica, sans-serif; text-align: center;">細<br>
&nbsp; &nbsp;&nbsp;お申し込み</strong></span></span></p>
</td>
<td style="width: 447px;">
<p style="text-align: center;"><br>
<a href="https://www.pasona.com/seminar/visa_111925/"><span style="color:#e74c3c;"><span style="font-size:22px;"><strong>詳細・お申し込みページ</strong></span></span></a><br>
<br>
<span style="font-size:16px;">​​​​​​<strong>【ウェビナー登録締切日】<br>
米国時間11月17日（月）18:00　PST<br>
&nbsp;</strong><span style="font-family:Arial,Helvetica,sans-serif;"><span style="margin-left:8px;"><span style="background-color:transparent;"><a href="mailto:infonews @pasona.com" style="color:blue;text-decoration:underline;">​​​​​</a></span></span></span></span></p>
</td>
</tr>
</tbody>
</table>
&nbsp;

<div style="text-align:-webkit-center; padding:10px 16px 15px">
<div class="txtTinyMce-wrapper">
<div style="margin-bottom:11px; text-align:center"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;"><span style="margin-left:8px;"><span style="background-color:transparent;"><strong>お問い合わせ<br>
Pasona N A, Inc.&nbsp;<a href="mailto:infonews @pasona.com?subject=%E3%80%90%E3%82%A6%E3%82%A7%E3%83%93%E3%83%8A%E3%83%BC%E3%80%91%E3%81%8A%E5%95%8F%E3%81%84%E5%90%88%E3%82%8F%E3%81%9B">infonews @pasona.com</a></strong></span></span></span></span></div>
</div>
</div>
</div>
</div>

<div style="color:#555555;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;line-height:1.8;padding-top:10px;padding-right:16px;padding-bottom:15px;padding-left:16px;">
<div class="txtTinyMce-wrapper" style="font-size: 12px; line-height: 1.8; color: #555555; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; mso-line-height-alt: 22px;">
<p style="margin: 0px; line-height: 1.8; word-break: break-word; font-size: 13px; text-align: center;">
<!--[if mso]></center></v:textbox></v:roundrect></td></tr></table><![endif]--></p>
</div>
</div>

<div style="text-align: center;">
<!--[if (!mso)&(!IE)]></div>
</div>

<div style="text-align: center;"><!--<![endif]--></div>
</div>
</div>

<div style="text-align: center;">
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]--></div>
</div>
</div>
</div>

<div style="background-color:transparent;">
<div class="block-grid " style="min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
<div class="col_cont" style="width:100% !important;">
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" height="5" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid transparent; height: 5px; width: 100%;" valign="top" width="100%">
<tbody style="text-align: center;">
</tbody>
</table>
</td>
</tr>
</tbody>
</table>

<div class="img-container center autowidth" style="padding-right: 0px; padding-left: 0px; text-align: center;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="center"><![endif]--><a href="https://form.run/ @pnaweb--UcEAWPHvAFBxyTpxf61l?utm_source=mail&amp;utm_medium=PNAnewsletter"><img alt="" border="0" height="160" src="https://storage.pardot.com/519571/1709082473KSrkeukw/_____________________.png" style="height: 160px; width: 640px; border-width: 0px; border-style: solid;" width="640"></a></div>
&nbsp;

<div class="img-container center autowidth" style="padding-right: 0px; padding-left: 0px; text-align: center;">
<!--[if mso]></td></tr></table><![endif]--></div>

<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" height="5" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid transparent; height: 5px; width: 100%;" valign="top" width="100%">
<tbody style="text-align: center;">
</tbody>
</table>
</td>
</tr>
</tbody>
</table>

<div style="text-align: center;">
<!--[if (!mso)&(!IE)]></div>
</div>

<div style="text-align: center;"><!--<![endif]--></div>
</div>
</div>

<div style="text-align: center;">
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]--></div>
</div>
</div>
</div>

<div style="background-color:transparent;">
<div class="block-grid " style="min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<div style="text-align: center;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="640" style="background-color:transparent;width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:30px;"><![endif]--></div>

<div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
<div class="col_cont" style="width:100% !important;">
<div style="text-align: center;">
<!--[if (!mso)&(!IE)]></div>

<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:30px; padding-right: 0px; padding-left: 0px;">
<div style="text-align: center;"><!--<![endif]--></div>

<table cellpadding="0" cellspacing="0" class="social_icons" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top" class="">
<div style="text-align: center;">
<div style="text-align: left;">
<table align="center" class="Table" style="width:6.25in; border-collapse:collapse" width="600">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top">
<table class="Table" style="border-collapse:collapse; border:none">
<tbody>
<tr>
<td style="border-bottom:1px solid #b6bbbe; padding:30px 30px 30px 30px; border-top:1px solid #b6bbbe; border-right:1px solid #b6bbbe; border-left:1px solid #b6bbbe" valign="top">
<table align="center" class="Table" style="width:100.0%; border-collapse:collapse" width="100%">
<tbody>
<tr>
<td style="width:122px; padding:0in 0in 0in 0in" valign="top">
<table class="Table" style="width:122px; border-collapse:collapse" width="122">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top" class="">
<p><span style="font-size:12pt"><span style="font-family:Aptos,sans-serif"><span style="font-family:&quot;Helvetica&quot;,sans-serif"><span style="color:#4b525d"><span style="text-decoration:none"><span style="text-underline:none"><img alt="Litmus" class="light-img" height="38" id="_x0000_i1025" src="https://www2.pasona.com/l/519571/2022-05-09/j7b7v8/519571/1652138760j4CezAKY/Logo_2_nobk.png" style="width: 150px; height: 38px;" width="150"></span></span></span></span></span></span><br>
&nbsp;</p>
</td>
</tr>
</tbody>
</table>
</td>
<td style="width:30px; padding:0in 0in 0in 0in" valign="top" class="">&nbsp;</td>
<td style="width:416px; padding:0in 0in 0in 0in" valign="top">
<table class="Table" role="presentation" style="width:416px; border-collapse:collapse" width="416">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top" class="">
<p align="right" style="margin-bottom:5px; text-align:right"><span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-family:Aptos,sans-serif"><span style="font-size:10.5pt"><span style="font-family:&quot;Helvetica&quot;,sans-serif"><span style="color:#4b525d">&nbsp;340 Madison Avenue, Suite 12-B, New York, NY 10173&nbsp;&nbsp;</span></span></span></span></span></span><br>
<span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-family:Aptos,sans-serif"><span style="font-size:10.5pt"><span style="font-family:&quot;Helvetica&quot;,sans-serif"><span style="color:#4b525d">&nbsp;<a href="{{Unsubscribe}}"><span style="color:#4b525d">Unsubscribe</span></a>&nbsp; &nbsp;|&nbsp; &nbsp;<a href="{{View_Online}}"><span style="color:#4b525d">View&nbsp;online</span></a>&nbsp; &nbsp;|&nbsp; &nbsp;<a href="https://www.pasona.com/en/privacy/"><span style="color:#4b525d">Privacy Policy</span></a>&nbsp;&nbsp;</span></span></span></span></span></span></p>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr>
<td style="width:122px; padding:0in 0in 0in 0in" valign="top">
<table class="Table" style="width:122px; border-collapse:collapse" width="122">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top">
<table class="Table" style="width:122px; border-collapse:collapse" width="122">
<tbody>
<tr>
<td style="word-break: break-word; vertical-align: top; padding-bottom: 0; padding-right: 7.5px; padding-left: 7.5px;" valign="top" class=""><br>
<a href="https://www.facebook.com/pasona.usa" target="_blank"><img alt="Facebook" height="32" src="https://d2fi4ri5dhpqd1.cloudfront.net/public/resources/social-networks-icon-sets/circle-color/facebook @2x.png" style="text-decoration-line: none; height: auto; border: 0px; display: block;" title="Facebook" width="32"></a></td>
<td style="word-break: break-word; vertical-align: top; padding-bottom: 0; padding-right: 7.5px; padding-left: 7.5px;" valign="top" class="">
<div>&nbsp;</div>
<a href="https://www.linkedin.com/company/pasona-na-inc/" target="_blank"><img alt="LinkedIn" height="32" src="https://d2fi4ri5dhpqd1.cloudfront.net/public/resources/social-networks-icon-sets/circle-color/linkedin @2x.png" style="text-decoration-line: none; height: auto; border: 0px; display: block;" title="LinkedIn" width="32"></a></td>
<td style="word-break: break-word; vertical-align: top; padding-bottom: 0; padding-right: 7.5px; padding-left: 7.5px;" valign="top" class="">
<div>&nbsp;</div>
<a href="https://youtu.be/a0ezUQFQyTk" target="_blank"><img alt="YouTube" height="32" src="https://d2fi4ri5dhpqd1.cloudfront.net/public/resources/social-networks-icon-sets/circle-color/youtube @2x.png" style="text-decoration-line: none; height: auto; border: 0px; display: block;" title="YouTube" width="32"></a></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
<td style="width:30px; padding:0in 0in 0in 0in" valign="top" class="">&nbsp;</td>
<td style="width:416px; padding:0in 0in 0in 0in" valign="top">
<table class="Table" role="presentation" style="width:416px; border-collapse:collapse" width="416">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top" class="">
<p align="right" style="margin-bottom:5px; text-align:right"><br>
<span style="font-family:Trebuchet MS,Helvetica,sans-serif;"><strong><span style="color:#aa2128;"><span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-size:10.5pt">© 2025&nbsp;Pasona N A, Inc. </span></span></span></span><span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-size:10.5pt">All rights&nbsp;reserved.</span></span></span><span style="color:#aa2128;"><span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-size:10.5pt">&nbsp;</span></span></span></span></strong></span></p>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
​​​​​​</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</div>

<div style="text-align: right;">&nbsp;</div>

<div><span style="font-size:10px;"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="color:#bdc3c7;">【免責事項】<br>
​本メールに記載されている情報の正確性については万全を期しておりますが、ご利用者が当情報を用いて行う一切の行為について、何らの責任を負うものではありません。本情報に起因してご利用者に生じた損害については、責任を負いかねますのでご了承ください。</span></span></span><br>
<span style="font-size:11px;"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="color:#bdc3c7;">This message may contain information that is legally privileged or confidential. If you received this transmission in error, regardless of whether you are a named recipient, please kindly notify the sender by reply e-mail and delete the message and any attachments. &nbsp;Any opinions expressed in this message may not reflect views of the company.</span></span></span></div>
</div>
</td>
</tr>
</tbody>
</table>
&nbsp;

<div style="color:#a6a4a2;font-family:'Roboto Slab', Arial, 'Helvetica Neue', Helvetica, sans-serif;line-height:1.5;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
<div class="txtTinyMce-wrapper" style="line-height: 1.5; font-size: 12px; font-family: 'Roboto Slab', Arial, 'Helvetica Neue', Helvetica, sans-serif; color: #a6a4a2; mso-line-height-alt: 18px;">
<p style="margin: 0px; font-size: 12px; line-height: 1.5; word-break: break-word; text-align: center;">&nbsp;</p>
</div>
</div>

<div style="text-align: center;">
<!--[if mso]></td></tr></table><![endif]-->
<!--[if (!mso)&(!IE)]></div>
</div>

<div style="text-align: center;"><!--<![endif]--></div>
</div>
</div>

<div style="text-align: center;">
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]--></div>
</div>
</div>
</div>

<div style="text-align: center;">
<!--[if (mso)|(IE)]></td></tr></table><![endif]--></div>

<div id="gtx-trans" style="position: absolute; left: 85px; top: 288px;">
<div class="gtx-trans-icon">&nbsp;</div>
</div>
</div>
</div>
</div>
</td>
</tr>
</tbody>
</table>

<!--[if (IE)]></div><![endif]-->
</body>

</html>
"""

EMAIL2_TEMPLATE = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
<!--[if gte mso 9]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width">
<!--[if !mso]><!-->
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<!--<![endif]-->
<title></title>
<!--[if !mso]><!-->
<!--<![endif]-->
<style type="text/css">
body {
margin: 0;
padding: 0;
}

table,
td,
tr {
vertical-align: top;
border-collapse: collapse;
}

* {
line-height: inherit;
}

a[x-apple-data-detectors=true] {
color: inherit !important;
text-decoration: none !important;
}
</style>
<style type="text/css" id="media-query">
 @media (max-width: 660px) {

.block-grid,
.col {
min-width: 320px !important;
max-width: 100% !important;
display: block !important;
}

.block-grid {
width: 100% !important;
}

.col {
width: 100% !important;
}

.col_cont {
margin: 0 auto;
}

img.fullwidth,
img.fullwidthOnMobile {
width: 100% !important;
}

.no-stack .col {
min-width: 0 !important;
display: table-cell !important;
}

.no-stack.two-up .col {
width: 50% !important;
}

.no-stack .col.num2 {
width: 16.6% !important;
}

.no-stack .col.num3 {
width: 25% !important;
}

.no-stack .col.num4 {
width: 33% !important;
}

.no-stack .col.num5 {
width: 41.6% !important;
}

.no-stack .col.num6 {
width: 50% !important;
}

.no-stack .col.num7 {
width: 58.3% !important;
}

.no-stack .col.num8 {
width: 66.6% !important;
}

.no-stack .col.num9 {
width: 75% !important;
}

.no-stack .col.num10 {
width: 83.3% !important;
}

.video-block {
max-width: none !important;
}

.mobile_hide {
min-height: 0px;
max-height: 0px;
max-width: 0px;
display: none;
overflow: hidden;
font-size: 0px;
}

.desktop_hide {
display: block !important;
max-height: none !important;
}
}
</style>
<style type="text/css" id="menu-media-query">
 @media (max-width: 660px) {
.menu-checkbox[type="checkbox"]~.menu-links {
display: none !important;
padding: 5px 0;
}

.menu-checkbox[type="checkbox"]~.menu-links span.sep {
display: none;
}

.menu-checkbox[type="checkbox"]:checked~.menu-links,
.menu-checkbox[type="checkbox"]~.menu-trigger {
display: block !important;
max-width: none !important;
max-height: none !important;
font-size: inherit !important;
}

.menu-checkbox[type="checkbox"]~.menu-links>a,
.menu-checkbox[type="checkbox"]~.menu-links>span.label {
display: block !important;
text-align: center;
}

.menu-checkbox[type="checkbox"]:checked~.menu-trigger .menu-close {
display: block !important;
}

.menu-checkbox[type="checkbox"]:checked~.menu-trigger .menu-open {
display: none !important;
}

#menuw19hjn~div label {
border-radius: 50% !important;
}

#menuw19hjn:checked~.menu-links {
background-color: #3fb9bc !important;
}

#menuw19hjn:checked~.menu-links a {
color: #ffffff !important;
}

#menuw19hjn:checked~.menu-links span {
color: #ffffff !important;
}
}
</style>
</head>

<body class="clean-body" style="margin: 0; padding: 0; -webkit-text-size-adjust: 100%; background-color: #f6f8f8;">
<!--[if IE]><div class="ie-browser"><![endif]-->
<table bgcolor="#f6f8f8" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="table-layout: fixed; vertical-align: top; min-width: 320px; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f6f8f8; width: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top;" valign="top" class="">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color:#f6f8f8"><![endif]-->
<div style="background-color:transparent;">
<div class="block-grid two-up no-stack" style="min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="320" style="background-color:transparent;width:320px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:5px;"><![endif]-->
<div class="col num6" style="display: table-cell; vertical-align: top; max-width: 320px; min-width: 318px; width: 320px;">
<div class="col_cont" style="width:100% !important;">
<!--[if (!mso)&(!IE)]>
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;"><!--<![endif]-->
<div align="left" class="img-container left fixedwidth" style="padding-right: 0px;padding-left: 0px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="left"><![endif]-->
<div style="font-size:1px;line-height:25px"><br>
<br>
<a href="http://www.pasona.com/" style="background-color: transparent; outline: none;" tabindex="-1" target="_blank"><img alt="Pasona" border="0" class="left fixedwidth" height="34" src="https://www2.pasona.com/l/519571/2021-11-15/gbqhvn/519571/1637023162DnRtOeCf/PNA_logo_clear_back.png" style="text-decoration-line: none; width: 187px; max-width: 100%; display: block; height: 34px; border-width: 0px;" title="Pasona" width="187"></a></div>

<div style="font-size:1px;line-height:15px">&nbsp;</div>

<!--[if mso]></td></tr></table><![endif]--></div>

<!--[if (!mso)&(!IE)]></div>
<!--<![endif]--></div>
</div>

<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td><td align="center" width="320" style="background-color:transparent;width:320px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:5px;"><![endif]-->

<div class="col num6" style="display: table-cell; vertical-align: top; max-width: 320px; min-width: 318px; width: 320px;">
<div class="col_cont" style="width:100% !important;">
<!--[if (!mso)&(!IE)]>
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;"><!--<![endif]-->
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td align="right" style="word-break: break-word; vertical-align: top; padding-top: 15px; padding-bottom: 5px; padding-left: 0px; padding-right: 0px; text-align: right; font-size: 0px;" valign="top" class=""><!--[if !mso><input class="menu-checkbox" id="menuw19hjn" style="display:none !important;max-height:0;visibility:hidden;" type="checkbox"> <!--<![endif]-->
<div class="menu-trigger" style="display:none;max-height:0px;max-width:0px;font-size:0px;overflow:hidden;"><label class="menu-label" for="menuw19hjn" style="height:36px;width:36px;display:inline-block;cursor:pointer;mso-hide:all;user-select:none;align:right;text-align:center;color:#ffffff;text-decoration:none;background-color:#3fb9bc;"><span class="menu-open" style="mso-hide:all;font-size:26px;line-height:36px;">☰</span><span class="menu-close" style="display:none;mso-hide:all;font-size:26px;line-height:36px;">✕</span></label></div>

<div class="menu-links">
<!--[if mso]>
<table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center">
<tr>
<td style="padding-top:20px;padding-right:20px;padding-bottom:15px;padding-left:20px">
<![endif]--><br>
<a href="https://form.run/ @pnaweb--UcEAWPHvAFBxyTpxf61l?utm_source=mail&amp;utm_medium=PNAnewsletter"><img align="right" alt="" border="0" height="75" src="https://www2.pasona.com/l/519571/2024-04-02/kb7phy/519571/1712093663Hbkuu8JI/CTA_Button.jpg" style="width: 300px; float: right; height: 75px; border-width: 0px; border-style: solid;" width="300"></a>
 <!--[if mso]></td></tr></table><![endif]--></div>
</td>
</tr>
</tbody>
</table>
<br>

<!--[if (!mso)&(!IE)]></div>
<!--<![endif]--></div>
</div>

<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]--></div>
</div>
</div>

<div style="background-color:#fff;">
<div class="block-grid " style="min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#fff;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="640" style="background-color:transparent;width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
<div class="col_cont" style="width:100% !important;">
<!--[if (!mso)&(!IE)]>
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;"><!--<![endif]-->
<div align="center" class="img-container center autowidth" style="padding-right: 16px;padding-left: 16px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 16px;padding-left: 16px;" align="center"><![endif]-->
<div align="center" class="img-container center autowidth" style="padding-right:16px; padding-left:16px">
<div align="center" class="img-container center autowidth" style="text-align:-webkit-center; padding-right:16px; padding-left:16px">
<p><span style="font-size:11px;"><span style="color:#aa2128;"><strong>締め切りが間近になりましたので再度のご案内をさせていただきます。<br>
既に本ウェビナーのお申し込みを頂いた方には重複のご案内になることをご容赦くださいませ。</strong></span></span><span style="font-size:medium"><span style="line-height:inherit"><span style="color:#000000"><span style="font-family:&quot;Times New Roman&quot;"><span style="font-style:normal"><span style="font-variant-ligatures:normal"><span style="font-weight:400"><span style="white-space:normal"><span style="background-color:#ffffff"><span style="text-decoration-thickness:initial"><span style="text-decoration-style:initial"><span style="text-decoration-color:initial"><span style="line-height:inherit"><span style="font-size:20px"><span style="line-height:inherit"><strong style="line-height:inherit"><span style="line-height:inherit"><span style="font-family:Arial, Helvetica, sans-serif"><span lang="JA" style="line-height:inherit"><span style="line-height:21.4px">​​​​</span></span></span></span></strong></span></span><br style="line-height:inherit">
<a href="https://www.pasona.com/seminar/visa_111925/"><img alt="" border="0" height="315" src="https://www2.pasona.com/l/519571/2025-10-23/kcr1tr/519571/1761263724GrYzWrJK/B_For_November_2025.png" style="width: 600px; height: 315px; border-width: 0px; border-style: solid;" width="600"></a><br>
<br>
<span style="font-size:14px"><span style="line-height:inherit"><span style="line-height:inherit"><span style="font-family:Arial, Helvetica, sans-serif"><span style="line-height:14.98px"><span lang="JA" style="line-height:inherit"><span style="line-height:14.98px">​​​​​</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span><a href="https://www.pasona.com/seminar/visa_111925/"><span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><img alt="" border="0" height="50" src="https://www2.pasona.com/l/519571/2024-02-27/kb617z/519571/1709085445ZEUWJECB/output_onlinepngtools__1_.png" style="width: 200px; height: 50px; border-width: 0px; border-style: solid;" width="200"></span></span></a></p>

<p style="text-align:justify; margin-bottom:11px"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:medium"><span style="line-height:inherit"><span style="color:#000000"><span style="font-style:normal"><span style="font-variant-ligatures:normal"><span style="font-weight:400"><span style="white-space:normal"><span style="background-color:#ffffff"><span style="text-decoration-thickness:initial"><span style="text-decoration-style:initial"><span style="text-decoration-color:initial"><span style="line-height:inherit"><span style="font-size:14px"><span style="line-height:inherit">第二次トランプ政権の発足以降、移民受入れ制限の公約のもと、さまざまな大統領令が打ち出され、米国移民法のあらゆる側面で厳格化が加速しています。その影響は、日系企業が活用する各種ビザにも及び、採用や駐在員派遣に関するルールが次々と変更されるなど、米国で事業を行うすべての企業において、これまで以上に柔軟かつ迅速な対応と、的確なリスクマネジメントが求められています。<br>
&nbsp;<br>
本ウェビナーでは、移民法専門弁護士をお招きし、実際に企業から寄せられる「よくある質問 Top 5」をもとに、最新の政策動向とその実務的な対応策を解説します。</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></p>

<hr>
<p align="center"><span style="font-size:20px;"><strong><span style="font-family:Arial,Helvetica,sans-serif;">【概要】<br>
<span style="color:#000000;">第二次トランプ政権下で加速する<br>
移民政策の厳格化・在米日系企業への影響</span><br>
<span style="color:#aa2128;">～よくある質問Top 5から考える、<br>
厳格化を乗り切るための実践的ヒント～</span></span></strong></span></p>
</div>

<div style="padding-top:10px; padding-right:16px; padding-bottom:15px; padding-left:16px">
<div class="txtTinyMce-wrapper">
<table border="1" cellpadding="1" cellspacing="1" class="pd-table" style="width: 564px;">
<tbody>
<tr>
<td style="width: 103px; text-align: center;">
<p><br>
<br>
​​​​​<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><strong>日　時</strong></span></span><br>
&nbsp;</p>
</td>
<td style="width: 447px;">
<p><br>
<br>
<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">&nbsp; &nbsp;日程： 2025年11月19日（水）<br>
&nbsp; &nbsp;時間：13:00-14:00 PT/ 15:00-16:00 CT/16:00-17:00 ET</span></span><br>
&nbsp;</p>
</td>
</tr>
<tr>
<td style="width: 103px; text-align: center;">
<p><br>
<br>
<br>
<br>
​​​​​​<br>
<span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;"><strong>場　所</strong></span></span></p>
</td>
<td style="width: 447px;">
<p style="margin-bottom: 11px;"><span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="color:#000000;"><span style="line-height:107%"><span lang="JA"><span style="line-height:107%">​​</span></span></span></span><br>
<br>
&nbsp;</span></span>&nbsp; &nbsp;<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">オンラインウェビナー（ツール：ZOOM）</span></span><span style="background-color: transparent;">​​​​​</span></p>

<ul>
<li><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;">イベントご参加用のURLは、ご登録いただいた方に、<br>
開催日1営業日前にお送りいたします。</span></span></li>
<li><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;">Zoomのアプリをインストール（無料）のうえ、ご参加<br>
されることを推奨しておりますが必須ではございません。</span></span></li>
</ul>

<div style="margin-bottom: 11px;"><span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="color:#000000;"><span style="line-height:107%"><span lang="JA"><span style="line-height:107%">​​​​</span></span></span></span></span></span></div>
</td>
</tr>
<tr>
<td style="width: 103px; text-align: center;">
<p><br>
<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;"><strong>​​​</strong></span></span><br>
<span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;"><strong>登 壇 者</strong></span></span></p>
</td>
<td style="width: 447px;"><br>
<br>
<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">&nbsp; &nbsp;<strong>岸波　宏和氏 / Hirokazu Kishinami</strong><br>
&nbsp; &nbsp;増田・舟井・アイファート・ミッチェル法律事務所 / 弁護士</span></span><br>
<br>
&nbsp;</td>
</tr>
<tr>
<td style="width: 103px;">
<p>​​​​​<br>
<br>
<br>
<span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;"><span style="background-color: transparent; text-align: center;">&nbsp; &nbsp; &nbsp; &nbsp;</span><strong style="background-color: transparent; font-size: 14px; font-family: Arial, Helvetica, sans-serif; text-align: center;">詳</strong><strong>　</strong><strong style="background-color: transparent; font-size: 14px; font-family: Arial, Helvetica, sans-serif; text-align: center;">細<br>
&nbsp; &nbsp;&nbsp;お申し込み</strong></span></span></p>
</td>
<td style="width: 447px;">
<p style="text-align: center;"><br>
<a href="https://www.pasona.com/seminar/visa_111925/"><span style="color:#e74c3c;"><span style="font-size:22px;"><strong>詳細・お申し込みページ</strong></span></span></a><br>
<br>
<span style="font-size:16px;">​​​​​​<strong>【ウェビナー登録締切日】<br>
米国時間11月17日（月）18:00　PST<br>
&nbsp;</strong><span style="font-family:Arial,Helvetica,sans-serif;"><span style="margin-left:8px;"><span style="background-color:transparent;"><a href="mailto:infonews @pasona.com" style="color:blue;text-decoration:underline;">​​​​​</a></span></span></span></span></p>
</td>
</tr>
</tbody>
</table>
&nbsp;

<div style="text-align:-webkit-center; padding:10px 16px 15px">
<div class="txtTinyMce-wrapper">
<div style="margin-bottom:11px; text-align:center"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;"><span style="margin-left:8px;"><span style="background-color:transparent;"><strong>お問い合わせ<br>
Pasona N A, Inc.&nbsp;<a href="mailto:infonews @pasona.com?subject=%E3%80%90%E3%82%A6%E3%82%A7%E3%83%93%E3%83%8A%E3%83%BC%E3%80%91%E3%81%8A%E5%95%8F%E3%81%84%E5%90%88%E3%82%8F%E3%81%9B">infonews @pasona.com</a></strong></span></span></span></span></div>
</div>
</div>
</div>
</div>

<div style="color:#555555;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;line-height:1.8;padding-top:10px;padding-right:16px;padding-bottom:15px;padding-left:16px;">
<div class="txtTinyMce-wrapper" style="font-size: 12px; line-height: 1.8; color: #555555; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; mso-line-height-alt: 22px;">
<p style="margin: 0px; line-height: 1.8; word-break: break-word; font-size: 13px; text-align: center;">
<!--[if mso]></center></v:textbox></v:roundrect></td></tr></table><![endif]--></p>
</div>
</div>

<div style="text-align: center;">
<!--[if (!mso)&(!IE)]></div>
</div>

<div style="text-align: center;"><!--<![endif]--></div>
</div>
</div>

<div style="text-align: center;">
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]--></div>
</div>
</div>
</div>

<div style="background-color:transparent;">
<div class="block-grid " style="min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
<div class="col_cont" style="width:100% !important;">
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" height="5" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid transparent; height: 5px; width: 100%;" valign="top" width="100%">
<tbody style="text-align: center;">
</tbody>
</table>
</td>
</tr>
</tbody>
</table>

<div class="img-container center autowidth" style="padding-right: 0px; padding-left: 0px; text-align: center;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="center"><![endif]--><a href="https://form.run/ @pnaweb--UcEAWPHvAFBxyTpxf61l?utm_source=mail&amp;utm_medium=PNAnewsletter"><img alt="" border="0" height="160" src="https://storage.pardot.com/519571/1709082473KSrkeukw/_____________________.png" style="height: 160px; width: 640px; border-width: 0px; border-style: solid;" width="640"></a></div>
&nbsp;

<div class="img-container center autowidth" style="padding-right: 0px; padding-left: 0px; text-align: center;">
<!--[if mso]></td></tr></table><![endif]--></div>

<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" height="5" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid transparent; height: 5px; width: 100%;" valign="top" width="100%">
<tbody style="text-align: center;">
</tbody>
</table>
</td>
</tr>
</tbody>
</table>

<div style="text-align: center;">
<!--[if (!mso)&(!IE)]></div>
</div>

<div style="text-align: center;"><!--<![endif]--></div>
</div>
</div>

<div style="text-align: center;">
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]--></div>
</div>
</div>
</div>

<div style="background-color:transparent;">
<div class="block-grid " style="min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<div style="text-align: center;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="640" style="background-color:transparent;width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:30px;"><![endif]--></div>

<div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
<div class="col_cont" style="width:100% !important;">
<div style="text-align: center;">
<!--[if (!mso)&(!IE)]></div>

<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:30px; padding-right: 0px; padding-left: 0px;">
<div style="text-align: center;"><!--<![endif]--></div>

<table cellpadding="0" cellspacing="0" class="social_icons" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top" class="">
<div style="text-align: center;">
<div style="text-align: left;">
<table align="center" class="Table" style="width:6.25in; border-collapse:collapse" width="600">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top">
<table class="Table" style="border-collapse:collapse; border:none">
<tbody>
<tr>
<td style="border-bottom:1px solid #b6bbbe; padding:30px 30px 30px 30px; border-top:1px solid #b6bbbe; border-right:1px solid #b6bbbe; border-left:1px solid #b6bbbe" valign="top">
<table align="center" class="Table" style="width:100.0%; border-collapse:collapse" width="100%">
<tbody>
<tr>
<td style="width:122px; padding:0in 0in 0in 0in" valign="top">
<table class="Table" style="width:122px; border-collapse:collapse" width="122">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top" class="">
<p><span style="font-size:12pt"><span style="font-family:Aptos,sans-serif"><span style="font-family:&quot;Helvetica&quot;,sans-serif"><span style="color:#4b525d"><span style="text-decoration:none"><span style="text-underline:none"><img alt="Litmus" class="light-img" height="38" id="_x0000_i1025" src="https://www2.pasona.com/l/519571/2022-05-09/j7b7v8/519571/1652138760j4CezAKY/Logo_2_nobk.png" style="width: 150px; height: 38px;" width="150"></span></span></span></span></span></span><br>
&nbsp;</p>
</td>
</tr>
</tbody>
</table>
</td>
<td style="width:30px; padding:0in 0in 0in 0in" valign="top" class="">&nbsp;</td>
<td style="width:416px; padding:0in 0in 0in 0in" valign="top">
<table class="Table" role="presentation" style="width:416px; border-collapse:collapse" width="416">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top" class="">
<p align="right" style="margin-bottom:5px; text-align:right"><span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-family:Aptos,sans-serif"><span style="font-size:10.5pt"><span style="font-family:&quot;Helvetica&quot;,sans-serif"><span style="color:#4b525d">&nbsp;340 Madison Avenue, Suite 12-B, New York, NY 10173&nbsp;&nbsp;</span></span></span></span></span></span><br>
<span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-family:Aptos,sans-serif"><span style="font-size:10.5pt"><span style="font-family:&quot;Helvetica&quot;,sans-serif"><span style="color:#4b525d">&nbsp;<a href="{{Unsubscribe}}"><span style="color:#4b525d">Unsubscribe</span></a>&nbsp; &nbsp;|&nbsp; &nbsp;<a href="{{View_Online}}"><span style="color:#4b525d">View&nbsp;online</span></a>&nbsp; &nbsp;|&nbsp; &nbsp;<a href="https://www.pasona.com/en/privacy/"><span style="color:#4b525d">Privacy Policy</span></a>&nbsp;&nbsp;</span></span></span></span></span></span></p>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr>
<td style="width:122px; padding:0in 0in 0in 0in" valign="top">
<table class="Table" style="width:122px; border-collapse:collapse" width="122">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top">
<table class="Table" style="width:122px; border-collapse:collapse" width="122">
<tbody>
<tr>
<td style="word-break: break-word; vertical-align: top; padding-bottom: 0; padding-right: 7.5px; padding-left: 7.5px;" valign="top" class=""><br>
<a href="https://www.facebook.com/pasona.usa" target="_blank"><img alt="Facebook" height="32" src="https://d2fi4ri5dhpqd1.cloudfront.net/public/resources/social-networks-icon-sets/circle-color/facebook @2x.png" style="text-decoration-line: none; height: auto; border: 0px; display: block;" title="Facebook" width="32"></a></td>
<td style="word-break: break-word; vertical-align: top; padding-bottom: 0; padding-right: 7.5px; padding-left: 7.5px;" valign="top" class="">
<div>&nbsp;</div>
<a href="https://www.linkedin.com/company/pasona-na-inc/" target="_blank"><img alt="LinkedIn" height="32" src="https://d2fi4ri5dhpqd1.cloudfront.net/public/resources/social-networks-icon-sets/circle-color/linkedin @2x.png" style="text-decoration-line: none; height: auto; border: 0px; display: block;" title="LinkedIn" width="32"></a></td>
<td style="word-break: break-word; vertical-align: top; padding-bottom: 0; padding-right: 7.5px; padding-left: 7.5px;" valign="top" class="">
<div>&nbsp;</div>
<a href="https://youtu.be/a0ezUQFQyTk" target="_blank"><img alt="YouTube" height="32" src="https://d2fi4ri5dhpqd1.cloudfront.net/public/resources/social-networks-icon-sets/circle-color/youtube @2x.png" style="text-decoration-line: none; height: auto; border: 0px; display: block;" title="YouTube" width="32"></a></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
<td style="width:30px; padding:0in 0in 0in 0in" valign="top" class="">&nbsp;</td>
<td style="width:416px; padding:0in 0in 0in 0in" valign="top">
<table class="Table" role="presentation" style="width:416px; border-collapse:collapse" width="416">
<tbody>
<tr>
<td style="padding:0in 0in 0in 0in" valign="top" class="">
<p align="right" style="margin-bottom:5px; text-align:right"><br>
<span style="font-family:Trebuchet MS,Helvetica,sans-serif;"><strong><span style="color:#aa2128;"><span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-size:10.5pt">© 2025&nbsp;Pasona N A, Inc. </span></span></span></span><span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-size:10.5pt">All rights&nbsp;reserved.</span></span></span><span style="color:#aa2128;"><span style="font-size:12pt"><span style="line-height:18.0pt"><span style="font-size:10.5pt">&nbsp;</span></span></span></span></strong></span></p>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
​​​​​​</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</div>

<div style="text-align: right;">&nbsp;</div>

<div><span style="font-size:10px;"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="color:#bdc3c7;">【免責事項】<br>
​本メールに記載されている情報の正確性については万全を期しておりますが、ご利用者が当情報を用いて行う一切の行為について、何らの責任を負うものではありません。本情報に起因してご利用者に生じた損害については、責任を負いかねますのでご了承ください。</span></span></span><br>
<span style="font-size:11px;"><span style="font-family:Arial,Helvetica,sans-serif;"><span style="color:#bdc3c7;">This message may contain information that is legally privileged or confidential. If you received this transmission in error, regardless of whether you are a named recipient, please kindly notify the sender by reply e-mail and delete the message and any attachments. &nbsp;Any opinions expressed in this message may not reflect views of the company.</span></span></span></div>
</div>
</td>
</tr>
</tbody>
</table>
&nbsp;

<div style="color:#a6a4a2;font-family:'Roboto Slab', Arial, 'Helvetica Neue', Helvetica, sans-serif;line-height:1.5;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
<div class="txtTinyMce-wrapper" style="line-height: 1.5; font-size: 12px; font-family: 'Roboto Slab', Arial, 'Helvetica Neue', Helvetica, sans-serif; color: #a6a4a2; mso-line-height-alt: 18px;">
<p style="margin: 0px; font-size: 12px; line-height: 1.5; word-break: break-word; text-align: center;">&nbsp;</p>
</div>
</div>

<div style="text-align: center;">
<!--[if mso]></td></tr></table><![endif]-->
<!--[if (!mso)&(!IE)]></div>
</div>

<div style="text-align: center;"><!--<![endif]--></div>
</div>
</div>

<div style="text-align: center;">
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]--></div>
</div>
</div>
</div>

<div style="text-align: center;">
<!--[if (mso)|(IE)]></td></tr></table><![endif]--></div>

<div id="gtx-trans" style="position: absolute; left: 85px; top: 288px;">
<div class="gtx-trans-icon">&nbsp;</div>
</div>
</div>
</div>
</div>
</td>
</tr>
</tbody>
</table>

<!--[if (IE)]></div><![endif]-->
</body>

</html>
"""

# --- HTML RENDERING HELPERS ---

def to_br(text: str) -> str:
    """Converts newlines to <br> tags and escapes HTML."""
    if not text:
        return ""
    # Basic escape
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return text.replace('\n', '<br>\n')

def render_final_email(template_html: str, data: Dict[str, Any]) -> str:
    """
    Renders the final HTML by replacing placeholders in the rich template.
    """
    html = template_html
    overview = data.get('overview', {})

    # --- Replace simple text fields ---
    html = html.replace(
        '第二次トランプ政権の発足以降、移民受入れ制限の公約のもと、さまざまな大統領令が打ち出され、米国移民法のあらゆる側面で厳格化が加速しています。その影響は、日系企業が活用する各種ビザにも及び、採用や駐在員派遣に関するルールが次々と変更されるなど、米国で事業を行うすべての企業において、これまで以上に柔軟かつ迅速な対応と、的確なリスクマネジメントが求められています。<br>\n&nbsp;<br>\n本ウェビナーでは、移民法専門弁護士をお招きし、実際に企業から寄せられる「よくある質問 Top 5」をもとに、最新の政策動向とその実務的な対応策を解説します。',
        to_br(data.get('intro', ''))
    )
    html = html.replace(
        '第二次トランプ政権下で加速する<br>\n移民政策の厳格化・在米日系企業への影響',
        to_br(data.get('title', ''))
    )
    html = html.replace(
        '～よくある質問Top 5から考える、<br>\n厳格化を乗り切るための実践的ヒント～',
        to_br(data.get('subtitle', ''))
    )
    html = html.replace(
        'オンラインウェビナー（ツール：ZOOM）',
        overview.get('place', '')
    )
    html = html.replace(
        '米国時間11月17日（月）18:00　PST',
        overview.get('registration_deadline', '')
    )

    # --- Replace links ---
    if overview.get('link'):
        html = html.replace('https://www.pasona.com/seminar/visa_111925/', overview['link'])

    # --- Replace date/time block ---
    datetime_parts = [
        f"&nbsp; &nbsp;日程： {overview.get('datetime_jp', '')}",
        f"&nbsp; &nbsp;時間：{overview.get('datetime_pt', '')}",
        overview.get('datetime_ct', ''),
        overview.get('datetime_et', '')
    ]
    datetime_str = '<br>\n'.join(filter(None, datetime_parts))
    html = html.replace(
        '<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">&nbsp; &nbsp;日程： 2025年11月19日（水）<br>\n&nbsp; &nbsp;時間：13:00-14:00 PT/ 15:00-16:00 CT/16:00-17:00 ET</span></span>',
        f'<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">{datetime_str}</span></span>'
    )

    # --- Replace speaker block ---
    speakers = data.get('speakers', [])
    if speakers:
        speaker_blocks = []
        for speaker in speakers:
            name = speaker.get('name', '')
            role = speaker.get('role', '')
            speaker_blocks.append(f"&nbsp; &nbsp;<strong>{to_br(name)}</strong><br>\n&nbsp; &nbsp;{to_br(role)}")
        speaker_html = '<br>\n<br>\n'.join(speaker_blocks)
        html = html.replace(
            '<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">&nbsp; &nbsp;<strong>岸波　宏和氏 / Hirokazu Kishinami</strong><br>\n&nbsp; &nbsp;増田・舟井・アイファート・ミッチェル法律事務所 / 弁護士</span></span>',
            f'<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">{speaker_html}</span></span>'
        )

    # --- Replace notices block ---
    notices = overview.get('notices', [])
    if notices:
        notice_html = '\n'.join([f'<li><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;">{to_br(item)}</span></span></li>' for item in notices])
        html = html.replace(
            '<ul>\n<li><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;">イベントご参加用のURLは、ご登録いただいた方に、<br>\n開催日1営業日前にお送りいたします。</span></span></li>\n<li><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;">Zoomのアプリをインストール（無料）のうえ、ご参加<br>\nされることを推奨しておりますが必須ではございません。</span></span></li>\n</ul>',
            f'<ul>\n{notice_html}\n</ul>'
        )
    
    return html

def create_download_button(html_content: str, filename: str, label: str):
    """Generates a download button for the given HTML content."""
    b64 = base64.b64encode(html_content.encode()).decode()
    return st.download_button(
        label=label,
        data=html_content,
        file_name=filename,
        mime='text/html',
    )

# --- CORE FUNCTIONS ---

def cheap_prune(raw_text: str) -> str:
    """
    Normalizes and prunes the raw text to reduce token count while preserving key info.
    """
    # 1. Normalize whitespace and bullets
    text = re.sub(r'[\u200b\u200c\u200d\ufeff\xa0]', ' ', raw_text)
    text = re.sub(r'[・◦●■]', '•', text)
    text = re.sub(r'[\t ]+', ' ', text)
    lines = text.split('\n')
    
    # 2. Filter for lines containing likely event-related keywords
    keywords = [
        '開催', '日時', '日本時間', 'PT', 'CT', 'ET', 'タイトル', '対象', 
        '注意事項', '紹介文', '概要', '登壇者', '経歴', 'Zoom', '締切', 
        '申し込み', 'URL', 'メール', 'agenda', 'speaker', 'topic', 'date', 'time'
    ]
    keyword_regex = re.compile('|'.join(keywords), re.IGNORECASE)
    
    # Regex for simple date/time/url patterns
    pattern_regex = re.compile(
        r'(\d{1,4}[-/年]\d{1,2}[-/月]\d{1,2}日?)|'  # Date like 2023/10/26
        r'(\d{1,2}:\d{2})|'                        # Time like 10:00
        r'(https?://\S+)|'                       # URL
        r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})' # Email
    )

    pruned_lines = [
        line.strip() for line in lines 
        if keyword_regex.search(line) or pattern_regex.search(line) or len(line.strip()) < 10 # Keep very short lines (often headings)
    ]
    
    # Collapse multiple blank lines
    collapsed_text = re.sub(r'\n{3,}', '\n\n', "\n".join(pruned_lines))
    
    # 3. Fallback: If speaker info seems to be lost, use original text
    speaker_keywords_present = any(kw in raw_text for kw in ['登壇者', '経歴', 'speaker'])
    if speaker_keywords_present and not any(kw in collapsed_text for kw in ['登壇者', '経歴', 'speaker']):
        return raw_text # Fallback to original if pruning was too aggressive
        
    return collapsed_text

def extract_with_openai(cleaned_text: str, api_key: str, model: str, temperature: float) -> Dict[str, Any]:

# --- MAIN APP ---

st.set_page_config(page_title="Webinar Email Generator", page_icon="📧", layout="wide")

# Initialize session state
if 'run_count' not in st.session_state:
    st.session_state.run_count = 0
    st.session_state.time_saved = 0
    st.session_state.money_saved = 0.0
    st.session_state.last_run_seconds = 0.0
    st.session_state.email1_html = ""
    st.session_state.email2_html = ""
    st.session_state.parsed_json = None
    st.session_state.api_key = os.getenv("OPENAI_API_KEY") or ""

# --- SIDEBAR ---
with st.sidebar:
    st.header("📊 Metrics")
    with st.container(border=True):
        st.metric("Count", f"{st.session_state.run_count} runs")
    with st.container(border=True):
        st.metric("Time Saved", f"{st.session_state.time_saved} min")
    with st.container(border=True):
        st.metric("Money Saved", f"${st.session_state.money_saved:,.2f}")

    if st.session_state.last_run_seconds > 0:
        st.info(f"Last run: {st.session_state.last_run_seconds:.2f}s")

    st.header("⚙️ Settings")
    
    st.session_state.api_key = st.text_input(
        "OpenAI API Key", 
        type="password", 
        value=st.session_state.api_key,
        help="Your API key is used only for this session and not stored."
    )
    
    model = st.selectbox(
        "Model",
        ("gpt-4o-mini", "gpt-4o", "gpt-4-turbo"),
        index=0,
        help="Cheaper models like gpt-4o-mini are recommended."
    )
    
    temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.2, 0.05,
        help="Lower values make the output more deterministic and focused."
    )

# --- MAIN UI ---
st.title("📧 Webinar → Two Emails (LP-style)")
st.caption("Paste a messy webinar brief from Word/Outlook to generate two clean HTML emails.")

raw_text_input = st.text_area(
    "Paste your webinar brief here (JP or EN)",
    height=300,
    placeholder="""
例：
【ウェビナータイトル】生成AI時代の新しい働き方
【紹介文】本ウェビナーでは、生成AIを活用して業務効率を...
【開催日時】2024年10月28日(月) 10:00～11:00 (日本時間)
【登壇者】山田 太郎 (株式会社サンプル 代表取締役)
...
"""
)

if st.button("Generate Emails", type="primary"):
    if not st.session_state.api_key:
        st.error("Please enter your OpenAI API Key in the sidebar.")
    elif not raw_text_input.strip():
        st.warning("Please paste some text into the brief area.")
    else:
        start_time = time.time()
        
        with st.spinner("Analyzing and generating emails..."):
            try:
                # 1. Prune text
                cleaned_text = cheap_prune(raw_text_input)
                prune_msg = f"Pruned {len(raw_text_input)}→{len(cleaned_text)} chars."
                
                # 2. Extract with OpenAI
                data = extract_with_openai(cleaned_text, st.session_state.api_key, model, temperature)
                st.session_state.parsed_json = data
                
                # 3. Render Emails
                email1_html = render_final_email(EMAIL1_TEMPLATE, data)
                st.session_state.email1_html = email1_html

                email2_html = render_final_email(EMAIL2_TEMPLATE, data)
                st.session_state.email2_html = email2_html

                # 5. Update metrics
                end_time = time.time()
                st.session_state.last_run_seconds = end_time - start_time
                st.session_state.run_count += 1
                st.session_state.time_saved += 30
                st.session_state.money_saved += (30 / 60) * 40 # Assume $40/hr

                st.success(f"✓ Success! Generated in {st.session_state.last_run_seconds:.2f}s. ({prune_msg})")
                st.rerun()

            except openai.APIError as e:
                st.error(f"An OpenAI API error occurred: {e.message}")
            except Exception as e:
                st.exception(e)

# Display generated content if available
if st.session_state.email1_html:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Email #1 (Announcement)")
        st.code(st.session_state.email1_html, language="html")
        create_download_button(st.session_state.email1_html, "email_announcement.html", "Download HTML #1")

    with col2:
        st.subheader("Email #2 (Reminder)")
        st.code(st.session_state.email2_html, language="html")
        create_download_button(st.session_state.email2_html, "email_reminder.html", "Download HTML #2")

    if st.checkbox("Show parsed JSON data"):
        st.json(st.session_state.parsed_json)

st.markdown("---")
st.caption("Powered by Streamlit. Uses OpenAI Structured Outputs for schema-locked JSON.")
