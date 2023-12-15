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
  
  <xsl:param name="paramCheckNextLink">yes</xsl:param>
  <xsl:param name="paramExtHTML"></xsl:param>
  <xsl:variable name="varTestCaseID" select="/TestCase/@TestCaseID"/>
  <xsl:variable name="varLastTestCaseID" select="document('LastTestCaseID.xml')/LastTestCaseID[string(.)]"/>  
<!--Variables for help messages -->
  <xsl:variable name="criterionHelp">Items to be covered by the set of test cases</xsl:variable>  
  <xsl:variable name="pathHelp">Complete execution path covered, see help page for notation</xsl:variable> 
  <xsl:variable name="labelsHelp">IDs of all "pathcrawler_label" instructions covered by this path</xsl:variable> 
  <xsl:variable name="pathPredicateHelp">The logical predicate over input variables satisfied by this test-case and all other cases which would cover this path</xsl:variable> 
  <xsl:variable name="verdictHelp">Was the result satisfactory according to the oracle used?</xsl:variable> 
  <xsl:variable name="pathPrefixIDHelp">The execution path or partial path whose treatment generated this test-case</xsl:variable> 
  <xsl:variable name="outputsHelp">Concrete output values (an output name starting with res__ denotes the value returned by the tested function)</xsl:variable> 
  <xsl:variable name="symOutputsHelp">Outputs expressed as a function of inputs, unless constant (an output name starting with res__ denotes the value returned by the tested function)</xsl:variable> 
<!--END Variables for help messages -->


  <xsl:template match="/">
    <html>
      <head>
	<link rel="stylesheet" href="style.css" type="text/css"/>
	<title>Test-case <xsl:value-of select="/TestCase/@TestCaseID"/></title>
      </head>
      <body>
	<h2 class="page_title">Test-case <xsl:value-of select="/TestCase/@TestCaseID"/></h2>
	<div class="centered">
	  <table border="0" width="100%" cellpadding="2">
	    <tr>
	      <td align="left" width="25%">
		<xsl:if test="TestCase/@PrevTestCaseID">
		  <xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="/TestCase/@PrevTestCaseID"/>.xml<xsl:value-of select="$paramExtHTML"/></xsl:attribute>Previous TC</xsl:element>
		</xsl:if>&nbsp;
	      </td>
	      <td align="center" width="50%">
<!--		<xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="TestCase/SessionData/TestSessionFile"/><xsl:value-of select="$paramExtHTML"/>#<xsl:value-of select="/TestCase/@PrefixID"/></xsl:attribute>View path prefixes explored</xsl:element>-->&nbsp;
	      </td>
	      <td align="right" width="25%">
		<xsl:if test="$paramCheckNextLink = 'yes' and $varLastTestCaseID != $varTestCaseID">
		  <xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="TestCase/@NextTestCaseID"/>.xml<xsl:value-of select="$paramExtHTML"/></xsl:attribute>Next TC</xsl:element>	  
		</xsl:if>&nbsp;
	      </td>
	    </tr>      
	  </table>
	</div>
	<xsl:apply-templates  select="TestCase"/>
	<div class="centered">
	  <table border="0" width="100%" cellpadding="2">
	    <tr>
	      <td align="left" width="25%">
		<xsl:if test="TestCase/@PrevTestCaseID">
		  <xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="/TestCase/@PrevTestCaseID"/>.xml<xsl:value-of select="$paramExtHTML"/></xsl:attribute>Previous TC</xsl:element>
		</xsl:if>&nbsp;
	      </td>
	      <td align="center" width="50%">
<!--		<xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="TestCase/SessionData/TestSessionFile"/><xsl:value-of select="$paramExtHTML"/>#<xsl:value-of select="/TestCase/@PrefixID"/></xsl:attribute>View path prefixes explored</xsl:element>-->&nbsp;
	      </td>
	      <td align="right" width="25%">
		<xsl:if test="$paramCheckNextLink = 'yes' and $varLastTestCaseID != $varTestCaseID">
		  <xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="TestCase/@NextTestCaseID"/>.xml<xsl:value-of select="$paramExtHTML"/></xsl:attribute>Next TC</xsl:element>	  
		</xsl:if>&nbsp;
	      </td>
	    </tr>      
	  </table>
	</div>
      </body>
    </html>
  </xsl:template>
  <xsl:template match="TestCase">

    
    <h3 class="section_title">Test-case data</h3>
    
    <div class="centered">
      <p><b>Input array sizes:</b></p>
      <table class="input_data">
	<tr class="input_data_caption">
	  <th>Array (or pointer)</th>
	  <th>Number of elements</th>
	</tr>
	<xsl:if test="not(Inputs/ArDim)"><tr><td colspan="2"><i>(empty)</i></td></tr></xsl:if>
	<xsl:for-each  select="Inputs/ArDim">
	  <tr>
	    <td><xsl:value-of select="VName"/></td>	
	    <td><xsl:value-of select="Val"/></td>
	  </tr>      
	</xsl:for-each>
      </table>
      
      <p><b>Input values:</b></p>
      <table class="input_data">
	<tr class="input_data_caption">
	  <th>Variable</th>
	  <th>Value</th>
	</tr>
	<xsl:if test="not(Inputs/VVal)"><tr><td colspan="2"><i>(empty)</i></td></tr></xsl:if>
	<xsl:for-each  select="Inputs/VVal">
	  <tr>
	    <td><xsl:value-of select="VName"/></td>
	    <td><xsl:value-of select="Val"/></td>
	  </tr>      
	</xsl:for-each>
      </table>

      <p><b>Verdict:</b>&nbsp;<img src="help.gif" border="0" alt="{$verdictHelp}" title="{$verdictHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;<xsl:apply-templates  select="Verdict"/></p>
 
      <p><b>Path:</b>&nbsp;<img src="help.gif" border="0" alt="{$pathHelp}" title="{$pathHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;
	<xsl:choose>
		<xsl:when test="not(Prefix/*) and not(Suffix/*)">
			<i>empty</i>
		</xsl:when>
		<xsl:otherwise>
			<xsl:if test="Prefix/*">
				<xsl:apply-templates select="Prefix"/>
			</xsl:if>
			<xsl:if test="Suffix/*">
				<xsl:apply-templates select="Suffix"/>
			</xsl:if>
		</xsl:otherwise>
	</xsl:choose>
      </p>

      <xsl:if test="CoveredLabels">
	<p><b>Covered labels:</b>&nbsp;<img src="help.gif" border="0" alt="{$labelsHelp}" title="{$labelsHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;
	<xsl:choose>
	  <xsl:when test="not(CoveredLabels/*)">
	    <i>none</i>
	  </xsl:when>
	  <xsl:otherwise>
	    <xsl:apply-templates select="CoveredLabels"/>
	  </xsl:otherwise>
	</xsl:choose>
	</p>
      </xsl:if>

      <p><b>Outputs:</b>&nbsp;<img src="help.gif" border="0" alt="{$outputsHelp}" title="{$outputsHelp}" style="cursor: help;" align="bottom"/></p>
      <table class="input_data">
	<tr class="input_data_caption">
	  <th>Expression</th>
	  <th>Value</th>
	</tr>
	<xsl:if test="not(Outputs/Output)"><tr><td colspan="2"><i>(empty)</i></td></tr></xsl:if>
	<xsl:for-each  select="Outputs/Output">
	  <tr>
	    <td><xsl:value-of select="VName"/></td>	
	    <td><xsl:value-of select="Val"/></td>
	  </tr>      
	</xsl:for-each>
      </table>
      
      <p><b>Symbolic outputs:</b>&nbsp;<img src="help.gif" border="0" alt="{$symOutputsHelp}" title="{$symOutputsHelp}" style="cursor: help;" align="bottom"/></p>
      <table class="input_data">
	<tr class="input_data_caption">
	  <th>Expression</th>
	  <th>Value</th>
	</tr>
	<xsl:if test="not(SymOutputs/SymOutput)"><tr><td colspan="2"><i>(empty)</i></td></tr></xsl:if>
	<xsl:for-each  select="SymOutputs/SymOutput">
	  <tr>
	    <td><xsl:value-of select="VName"/></td>
	    <td><xsl:value-of select="Val"/></td>
	  </tr>      
	</xsl:for-each>
      </table>

      <p><b>Path predicate:</b>&nbsp;<img src="help.gif" border="0" alt="{$pathPredicateHelp}" title="{$pathPredicateHelp}" style="cursor: help;" align="bottom"/></p>	
      <xsl:if test="not(PathPredicate/Ctr)"><i>(empty)</i></xsl:if>
      <xsl:for-each select="PathPredicate/Ctr">
	<p>	
	  <span class="marge">	
	    <xsl:value-of select="."/><xsl:if test="not(position()=last())"><b> AND </b></xsl:if>
	  </span>
	</p>
      </xsl:for-each>
      

      <p><xsl:element name="a"><xsl:attribute name="href">../testdrivers/<xsl:value-of select="@TestCaseID"/>.c</xsl:attribute><xsl:attribute name="target">_blank</xsl:attribute>View test driver</xsl:element></p>

      <p><b>Path prefix ID:</b>&nbsp;<img src="help.gif" border="0" alt="{$pathPrefixIDHelp}" title="{$pathPrefixIDHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;<xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="SessionData/TestSessionFile"/><xsl:value-of select="$paramExtHTML"/>#<xsl:value-of select="@PrefixID"/></xsl:attribute><xsl:value-of select="@PrefixID"/></xsl:element></p>

    </div>

    <h3 class="section_title">General information</h3>
    <div class="centered">

      <xsl:comment><p><b>Session started: </b><xsl:value-of select="SessionData/When"/></p></xsl:comment><xsl:text>
</xsl:text>
 <xsl:comment><p><b>PathCrawler version: </b><xsl:value-of select="SessionData/Version"/></p></xsl:comment><xsl:text>
</xsl:text>

      <p><b>Function under test: </b> <xsl:value-of select="SessionData/FunName"/></p>

      <p><b>Coverage criterion:</b>&nbsp;<img src="help.gif" border="0" alt="{$criterionHelp}" title="{$criterionHelp}" style="cursor: help;" align="bottom"/> &nbsp;&nbsp;<xsl:if test="SessionData/Strategy/@Coverage = 'all-paths'">all feasible paths</xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'all-branches'">all reachable branches</xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'all-mcdc'">mcdc of all decisions</xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'paths-func'">all feasible paths in function <xsl:value-of select="SessionData/Strategy"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'branches-func'">all reachable branches in function <xsl:value-of select="SessionData/Strategy"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'mcdc-func'">mcdc of all decisions in function <xsl:value-of select="SessionData/Strategy"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@IterLimit != 'none'">, limit loop iterations to <xsl:value-of select="SessionData/Strategy/@IterLimit"/></xsl:if>      
      <xsl:if test="SessionData/Strategy/@RecurLimit != 'none'">, limit recursion unfolding to <xsl:value-of select="SessionData/Strategy/@RecurLimit"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@SuffixLengthLimit != 'none'">, limit number of conditions treated in path suffix to <xsl:value-of select="SessionData/Strategy/@SuffixLengthLimit"/></xsl:if>
      </p>

      <p><b>Generated: </b><xsl:value-of select="Time"/></p>

      <p><b>Time elapsed since test session started: </b><xsl:value-of select="Dur"/> sec.</p>

    </div>

  </xsl:template>

  <xsl:template match="Prefix|Suffix">
    <xsl:if test="child::*"><xsl:apply-templates select="child::*"/></xsl:if>
    <xsl:if test="not(child::*)"><i>empty</i></xsl:if>
  </xsl:template>
  
  <xsl:template match="N"><xsl:if test="@SrcFile"><xsl:value-of select="@SrcFile"/>&nbsp;:&nbsp;</xsl:if>-<xsl:value-of select="."/><xsl:if test="@LID">(label <xsl:value-of select="@LID"/>)&nbsp;</xsl:if>; </xsl:template>
  
  <xsl:template match="P"><xsl:if test="@SrcFile"><xsl:value-of select="@SrcFile"/>&nbsp;:&nbsp;</xsl:if>+<xsl:value-of select="."/><xsl:if test="@LID">(label <xsl:value-of select="@LID"/>)&nbsp;</xsl:if>; </xsl:template>

  <xsl:template match="CoveredLabels">
    <xsl:if test="child::*"><xsl:apply-templates select="child::*"/></xsl:if>
    <xsl:if test="not(child::*)"><i>none</i></xsl:if>
  </xsl:template>
  
  <xsl:template match="LID"><xsl:value-of select="."/>; </xsl:template>

  <!-- ATTN: consistency with io.pl -->
  <xsl:template match="Verdict">
    <xsl:if test="@Type = 'success'">success<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></xsl:if>
    <xsl:if test="@Type = 'unknown'">unknown<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></xsl:if>
    <xsl:if test="@Type = 'failure'"><font class="attn">failure<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'assert_violated'"><font class="attn">user assert KO<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'assert_violated_in_oracle'"><font class="attn">user assert KO in oracle<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'crashed'"><font class="attn">crashed<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'hung'"><font class="attn">hung<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'interrupt'"><font class="attn">interrupt<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'bug_oracle'"><font class="warn">oracle bug<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'maybe_success'"><font class="warn">maybe success<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'maybe_unknown'"><font class="warn">maybe unknown<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'maybe_failure'"><font class="warn">maybe failure<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'invalid_memory_access'"><font class="warn">invalid memory access<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'div_by_0'"><font class="warn">division by 0<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'uninit_var'"><font class="warn">uninitialized variable<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'deref_null_pointer'"><font class="warn">null pointer dereference<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'use_after_free'"><font class="warn">use after free<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'invalid_arg'"><font class="warn">invalid argument<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'error'"><font class="warn">error<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></font></xsl:if>
    <xsl:if test="@Type = 'no_extra_coverage'">no_extra_coverage<xsl:if test=". != ''"><xsl:text> - </xsl:text><xsl:value-of select="."/></xsl:if></xsl:if>
    <xsl:if test="@Type = 'error'"><font class="warn">none</font></xsl:if>
  </xsl:template>

</xsl:stylesheet>
