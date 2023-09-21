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
  
  <xsl:template match="/">
    <html>
      <head>
	<link rel="stylesheet" href="style.css" type="text/css"/>
	<xsl:if test="$paramRefresh != 'no'"><xsl:element name="meta"><xsl:attribute name="http-equiv">refresh</xsl:attribute><xsl:attribute name="content"><xsl:value-of select="$paramRefresh"/></xsl:attribute></xsl:element></xsl:if>
	<title>Test session results</title>
      </head>
      <body>
	<h2 class="page_title">Path prefixes explored</h2>
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
      <p><b>Session started: </b><xsl:value-of select="SessionData/When"/></p>
      <p><b>PathCrawler version: </b><xsl:value-of select="SessionData/Version"/></p>
      <p><b>Function under test: </b> <xsl:value-of select="SessionData/FunName"/></p>
      <p><b>Coverage criterion: </b> 
      <xsl:if test="SessionData/Strategy/@Coverage = 'all-paths'">all feasible paths</xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'all-branches'">all reachable branches</xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'all-mcdc'">mcdc of all decisions</xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'paths-func'">all feasible paths in function <xsl:value-of select="SessionData/Strategy"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'branches-func'">all reachable branches in function <xsl:value-of select="SessionData/Strategy"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'mcdc-func'">mcdc of all decisions in function <xsl:value-of select="SessionData/Strategy"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@IterLimit != 'none'">, limit loop unrolling to <xsl:value-of select="SessionData/Strategy/@IterLimit"/></xsl:if>      
      <xsl:if test="SessionData/Strategy/@RecurLimit != 'none'">, limit recursion unfolding to <xsl:value-of select="SessionData/Strategy/@RecurLimit"/></xsl:if>      
      <xsl:if test="SessionData/Strategy/@SuffixLengthLimit != 'none'">, limit number of conditions treated in path suffix to <xsl:value-of select="SessionData/Strategy/@SuffixLengthLimit"/></xsl:if>      

      </p>      
    </div>
    
    <h3 class="section_title">Path prefixes treated</h3>
    <xsl:for-each  select="PrefixData">
      <div class="centered">
	<hr class="path_separator"/>
	<p><xsl:element name="a">
	  <xsl:attribute name="name"><xsl:value-of select="@TestCaseID"/></xsl:attribute>
	  <b>Path prefix ID: </b> <xsl:value-of select="@PrefixID"/>
	</xsl:element></p>
	<p><b>Path prefix/<font color='grey'>suffix</font>: </b>
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
	</p>
	<p><b>Treated: </b><xsl:value-of select="Time"/></p>
	<p><b>Time elapsed since test session started: </b><xsl:value-of select="Dur"/> sec.</p>
	<p><b>Status: </b><xsl:apply-templates  select="PrefixStatus"/></p>
	<xsl:if test="TestCaseFile">
	  <p><b>Test case ID: </b> <xsl:value-of select="@TestCaseID"/></p>
	  <p><b>Verdict: </b><xsl:apply-templates  select="Verdict"/></p>
	  <p><xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="TestCaseFile"/><xsl:value-of select="$paramExtHTML"/></xsl:attribute>
	    View test case details
	  </xsl:element>
	  </p>
	</xsl:if>
      </div>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="Prefix|Suffix">
    <xsl:if test="child::*"><xsl:apply-templates select="child::*"/></xsl:if>
    <xsl:if test="not(child::*)"><i>empty</i></xsl:if>
  </xsl:template>
  
  <xsl:template match="N"><xsl:if test="@SrcFile"><xsl:value-of select="@SrcFile"/> : </xsl:if>-<xsl:value-of select="."/>;</xsl:template>
  
  <xsl:template match="P"><xsl:if test="@SrcFile"><xsl:value-of select="@SrcFile"/> : </xsl:if>+<xsl:value-of select="."/>;</xsl:template>

  <!-- ATTN: consistency with io.pl -->
  <xsl:template match="Verdict">
    <xsl:if test="@Type = 'success'">success <xsl:value-of select="."/></xsl:if>
    <xsl:if test="@Type = 'unknown'">unknown <xsl:value-of select="."/></xsl:if>
    <xsl:if test="@Type = 'failure'"><font class="attn">failure: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'assert_violated'"><font class="attn">user assertion violated: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'assert_violated_in_oracle'"><font class="attn">user assertion violated in oracle: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'crashed'"><font class="attn">program crashed before 1st branch: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'hung'"><font class="attn">program did not terminate: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'interrupt'"><font class="attn">abnormal program termination: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'bug_oracle'"><font class="attn">bug in oracle: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'maybe_success'"><font class="attn">oracle crashed after success verdict: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'maybe_unknown'"><font class="attn">oracle crashed after unknown verdict: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'maybe_failure'"><font class="attn">oracle crashed after fail verdict: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'invalid_memory_access'"><font class="attn">PathCrawler detected invalid memory access: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'deref_null_pointer'"><font class="attn">null pointer dereference: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'use_after_free'"><font class="attn">use after free: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'div_by_0'"><font class="attn">PathCrawler detected division by 0: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'uninit_var'"><font class="attn">PathCrawler detected uninitialised variable: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'invalid_arg'"><font class="attn">PathCrawler detected invalid argument: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'error'"><font class="attn">error: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'no_extra_coverage'"><font class="attn">this case did not increase coverage: <xsl:value-of select="."/></font></xsl:if>
    <xsl:if test="@Type = 'none"><font class="attn">none</font></xsl:if>
  </xsl:template>


  <!-- ATTN: consistency with io.pl -->
  <xsl:template match="PrefixStatus">
    <xsl:if test="@Status = 'covered'">a test case was generated</xsl:if>
    <xsl:if test="@Status = 'timeout'">test generation for this path was stopped by timeout</xsl:if>
    <xsl:if test="@Status = 'infeasible'">infeasible partial path</xsl:if>
    <xsl:if test="@Status = 'assume_violated'">a test case violating a user assume statement was generated</xsl:if>
    <xsl:if test="@Status = 'iteration_limit_violated'">violates loop iteration or recursion depth limits</xsl:if>
    <xsl:if test="@Status = 'no_extra_coverage'">this path provides no extra coverage</xsl:if>
    <xsl:if test="@Status = 'PC_bug'">this path revealed a possible bug in PathCrawler: please report</xsl:if>
    <xsl:if test="@Status = 'untreated'">this path contains untreated C language constructs</xsl:if>
    <xsl:if test="@Status = 'subsumed'">this is a prefix of another path</xsl:if>
    <xsl:if test=". != ''"> (<xsl:value-of select="."/>)</xsl:if>
  </xsl:template>

</xsl:stylesheet>
