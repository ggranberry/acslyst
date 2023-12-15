<?xml version="1.0" encoding="UTF-8"?>

<!--                                                                        -->
<!--                                                                        -->
<!--  This file is part of the Frama-C plug-in 'PathCrawler' (pc).          -->
<!--                                                                        -->
<!--  Copyright (C) 2007-2023                                               -->
<!--    CEA (Commissariat à l'énergie atomique et aux énergies              -->
<!--         alternatives)                                                  -->
<!--                                                                        -->
<!--  All rights reserved.                                                  -->
<!--  Contact CEA LIST for licensing.                                       -->
<!--                                                                        -->
<!--                                                                        -->

<!DOCTYPE xsl:stylesheet [<!ENTITY nbsp "&#160;">]>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output
      method="html"
      encoding="ISO-8859-1"
      doctype-public="-//W3C//DTD HTML 4.01//EN"
      doctype-system="http://www.w3.org/TR/html4/strict.dtd"
      indent="yes"
      />

  <xsl:param name="paramExtHTML"></xsl:param>
  <xsl:param name="paramRefresh">no</xsl:param>
<!--Variables for help messages -->
  <xsl:variable name="criterionHelp">Items to be covered by the set of test-cases</xsl:variable>  
  <xsl:variable name="pathPrefixIDHelp">The execution path or partial path whose treatment generated this test-case</xsl:variable> 
  <xsl:variable name="pathHelp">Complete execution path covered, see help page for notation</xsl:variable> 
  <xsl:variable name="verdictHelp">Was the result satisfactory according to the oracle used ?</xsl:variable> 
  <xsl:variable name="timeHelp">Time elapsed since the start of test-case generation</xsl:variable>

<!--END Variables for help messages -->
  
  <xsl:template match="/">
    <html>
      <head>
	<link rel="stylesheet" href="style.css" type="text/css"/>
	<xsl:if test="$paramRefresh != 'no'"><xsl:element name="meta"><xsl:attribute name="http-equiv">refresh</xsl:attribute><xsl:attribute name="content"><xsl:value-of select="$paramRefresh"/></xsl:attribute></xsl:element></xsl:if>
	<title>Test cases</title>
      </head>
      <body>
	<h2 class="page_title">Test-cases generated</h2>
	<xsl:apply-templates  select="TestSession"/>
      </body>
    </html>
  </xsl:template>
  <xsl:template match="TestSession">
<!--
    <div class="centered">
      <table border="0" width="100%" cellpadding="2">
	<tr><td align="center" width="100%">
	  <xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="SessionData/TestReportFile"/><xsl:value-of select="$paramExtHTML"/></xsl:attribute>View test session summary</xsl:element>
	</td></tr>      
      </table>
    </div>
-->
    <h3 class="section_title">General test session information</h3>
    <div class="centered">
      <xsl:comment><p><b>Session started: </b><xsl:value-of select="SessionData/When"/></p></xsl:comment><xsl:text>
</xsl:text>
 <xsl:comment><p><b>PathCrawler version: </b><xsl:value-of select="SessionData/Version"/></p></xsl:comment><xsl:text>
</xsl:text> 
      <p><b>Function under test: </b> <xsl:value-of select="SessionData/FunName"/></p>
      <p><b>Coverage criterion:&nbsp;<img src="help.gif" border="0" 
	   alt="{$criterionHelp}" title="{$criterionHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;</b> 
      <xsl:if test="SessionData/Strategy/@IterNum = 'all'">all feasible paths</xsl:if> <!-- OLD, DELETE all WHEN UNSELESS -->
      <xsl:if test="SessionData/Strategy/@IterNum = 'allpath'">all feasible paths</xsl:if> 
      <xsl:if test="SessionData/Strategy/@IterNum = 'allcond'">all feasible conditions</xsl:if> 
      <xsl:if test="SessionData/Strategy/@IterNum != 'all' and SessionData/Strategy/@IterNum != 'allpath' and SessionData/Strategy/@IterNum != 'allcond'">limit loop iterations to <xsl:value-of select="SessionData/Strategy/@IterNum"/></xsl:if> 
      </p>      
    </div>
    
    <h3 class="section_title">Test-cases generated</h3>
<!--    
    <div class="centered">
      <p align="justify">For each test-case, the columns show the test-case ID, oracle's verdict, time elapsed since the test session was started, path prefix ID and the complete program path as a sequence of decisions. </p>
    </div> 
-->
      <table align="center" width="100%" border="1" cellpadding="2">
	<tr class="input_data_caption">
	  <td align="center"><b>Test case ID</b></td>
	  <td align="center"><b>Verdict</b>&nbsp;<img src="help.gif" border="0" alt="{$verdictHelp}" title="{$verdictHelp}" style="cursor: help;" align="bottom"/></td>
	  <td align="center"><b>Time, sec.</b>&nbsp;<img src="help.gif" border="0" alt="{$timeHelp}" title="{$timeHelp}" style="cursor: help;" align="bottom"/></td>
	  <td align="center"><b>Prefix ID&nbsp;<img src="help.gif" border="0" 
	   alt="{$pathPrefixIDHelp}" title="{$pathPrefixIDHelp}" style="cursor: help;" align="bottom"/></b></td>
<!--	  <td align="left"><b>&nbsp;&nbsp;Path prefix</b></td> -->
	  <td align="left"><b>&nbsp;&nbsp;Path prefix/<font color='grey'>suffix</font></b>&nbsp;<img src="help.gif" border="0" alt="{$pathHelp}" title="{$pathHelp}" style="cursor: help;" align="bottom"/></td> 
	</tr>
	<xsl:for-each select="PrefixData">
	  <xsl:if test="TestCaseFile">
	  <tr>
	    <td align="left">
	      <xsl:if test="TestCaseFile"><xsl:element name="a">
		    <xsl:attribute name="href"><xsl:value-of select="TestCaseFile"/><xsl:value-of select="$paramExtHTML"/></xsl:attribute>
		    <xsl:value-of select="@TestCaseID"/>
	      </xsl:element></xsl:if>
	    </td>	    
	    <xsl:if test="Verdict"><xsl:apply-templates select="Verdict"/></xsl:if>    
	    <xsl:if test="not(Verdict)"><td>&nbsp;</td></xsl:if> 
	    <td align="center">
	      <xsl:value-of select="Dur"/>
	    </td>
	    <td align="left">
	      <xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="../SessionData/TestSessionFile"/><xsl:value-of select="$paramExtHTML"/>#<xsl:value-of select="@PrefixID"/></xsl:attribute><xsl:value-of select="@PrefixID"/></xsl:element>
<!--
	      <xsl:value-of select="@PrefixID"/> 
	      <xsl:element name="a">
		<xsl:attribute name="name"><xsl:value-of select="@TestCaseID"/></xsl:attribute>
		<xsl:text>&nbsp;</xsl:text>
	      </xsl:element>
-->
	    </td>
	    <td align="left" nowrap="true">
	      <xsl:choose>
		<xsl:when test="not(Prefix/*) and not(Suffix/*)">
		  <i>empty</i>
		</xsl:when>
		<xsl:otherwise>
		  <xsl:if test="Prefix/*">
		    <xsl:apply-templates select="Prefix"/>
		  </xsl:if>
		  <xsl:if test="Suffix/*">
		    <font color='grey'><xsl:apply-templates select="Suffix"/></font>
		  </xsl:if>
		</xsl:otherwise>
	      </xsl:choose>
	      &nbsp;
<!-- 	      <xsl:apply-templates select="document(TestCaseFile)/TestCase/Path"/> -->
	    </td>
 	  </tr>
	  </xsl:if>
	</xsl:for-each>
      </table>
  </xsl:template>

  <xsl:template match="Prefix|Suffix">
    <xsl:if test="child::*"><xsl:apply-templates select="child::*"/></xsl:if>
    <xsl:if test="not(child::*)"><i>(empty)</i></xsl:if>
  </xsl:template>

  <xsl:template match="Path">
    <xsl:if test="child::*"><xsl:apply-templates select="child::*"/></xsl:if>
    <xsl:if test="not(child::*)"><i>empty</i></xsl:if>
  </xsl:template>
  
  <xsl:template match="N"><xsl:if test="@SrcFile"><xsl:value-of select="@SrcFile"/>&nbsp;:&nbsp;</xsl:if>-<xsl:value-of select="."/>;</xsl:template>
  
  <xsl:template match="P"><xsl:if test="@SrcFile"><xsl:value-of select="@SrcFile"/>&nbsp;:&nbsp;</xsl:if>+<xsl:value-of select="."/>;</xsl:template>

  <!-- ATTN: consistency with io.pl -->
  <xsl:template match="Verdict">	    
    <xsl:element name="td">	    	   
      <xsl:if test="../TestCaseFile">
	<xsl:attribute name="align">center</xsl:attribute>
	<xsl:attribute name="title">
	  <xsl:value-of select="./@Type"/>
	  <xsl:if test=". != ''">
	    <xsl:text> - </xsl:text>
	    <xsl:value-of select="."/>
	  </xsl:if>    
	</xsl:attribute>
	<xsl:if test="@Type = 'success'">success</xsl:if>
	<xsl:if test="@Type = 'unknown'">unknown</xsl:if>
	<xsl:if test="@Type = 'failure'"><font class="attn">failure</font></xsl:if>
	<xsl:if test="@Type = 'assert_violated'"><font class="attn">user&nbsp;assert&nbsp;KO</font></xsl:if>
	<xsl:if test="@Type = 'assert_violated_in_oracle'"><font class="attn">user&nbsp;assert&nbsp;in&nbsp;oracle&nbsp;KO</font></xsl:if>
	<xsl:if test="@Type = 'crashed'"><font class="attn">crashed</font></xsl:if>
	<xsl:if test="@Type = 'hung'"><font class="attn">hung</font></xsl:if>
	<xsl:if test="@Type = 'interrupt'"><font class="attn">interrupt</font></xsl:if>
	<xsl:if test="@Type = 'bug_oracle'"><font class="warn">oracle&nbsp;bug</font></xsl:if>
	<xsl:if test="@Type = 'maybe_success'"><font class="warn">maybe&nbsp;success</font></xsl:if>
	<xsl:if test="@Type = 'maybe_unknown'"><font class="warn">maybe&nbsp;unknown</font></xsl:if>
	<xsl:if test="@Type = 'maybe_failure'"><font class="warn">maybe&nbsp;failure</font></xsl:if>
	<xsl:if test="@Type = 'uninit_var'"><font class="warn">uninit.&nbsp;variable</font></xsl:if>
	<xsl:if test="@Type = 'invalid_memory_access'"><font class="warn">invalid&nbsp;mem.&nbsp;access</font></xsl:if>
	<xsl:if test="@Type = 'deref_null_pointer'"><font class="warn">deref.&nbsp;null&nbsp;ptr.</font></xsl:if>
	<xsl:if test="@Type = 'use_after_free'"><font class="warn">use&nbsp;after&nbsp;free</font></xsl:if>
	<xsl:if test="@Type = 'div_by_0'"><font class="warn">division&nbsp;by&nbsp;0</font></xsl:if>
	<xsl:if test="@Type = 'invalid_arg'"><font class="warn">invalid&nbsp;argument</font></xsl:if>
	<xsl:if test="@Type = 'error'"><font class="warn">error</font></xsl:if>
	<xsl:if test="@Type = 'no_extra_coverage'"><font class="warn">no&nbsp;extra&nbsp;cov.</font></xsl:if>
	<xsl:if test="@Type = 'none'"><font class="warn">error</font></xsl:if>
      </xsl:if>	    
    </xsl:element>
  </xsl:template>

</xsl:stylesheet>
