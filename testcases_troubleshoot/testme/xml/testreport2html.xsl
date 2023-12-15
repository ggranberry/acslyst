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
  <xsl:variable name="statusHelp">Did test-case generation for this function end normally?</xsl:variable>  
  <xsl:variable name="criterionHelp">Items to be covered by the set of test cases</xsl:variable>  
  <xsl:variable name="successHelp">Number of test-cases whose result was satisfactory according to the oracle which was used</xsl:variable>  
  <xsl:variable name="failureHelp">Number of test-cases whose result was unsatisfactory according to the oracle which was used</xsl:variable>  
  <xsl:variable name="unknownHelp">Number of test-cases whose result could not be qualified by the oracle which was used</xsl:variable>  
  <xsl:variable name="assertHelp">Number of test-cases whose result violated an assertion in the source code</xsl:variable>  
  <xsl:variable name="crashedHelp">Number of test-cases on which the function under test crashed</xsl:variable>  
  <xsl:variable name="hungHelp">Number of test-cases on which the function under test hung</xsl:variable>  
  <xsl:variable name="oracleWarningHelp">Number of test-cases whose verdict is uncertain due to oracle warning</xsl:variable>  
  <xsl:variable name="rteHelp">Number of tests-cases which resulted in a run-time error</xsl:variable>  
  <xsl:variable name="PCBugHelp">Number of path prefixes which resulted in a PathCrawler error</xsl:variable>  
  <xsl:variable name="untreatedHelp">Number of path prefixes which cannot be treated by the current version of PathCrawler</xsl:variable>  
  <xsl:variable name="uninitVarHelp">Number of path prefixes with an uninitialised variable</xsl:variable>  
  <xsl:variable name="pathsHelp">The execution paths and partial paths explored during test-case generation</xsl:variable>  
  <xsl:variable name="labelsHelp">Are any "pathcrawler_label" instructions not covered by any test-case</xsl:variable> 
  <xsl:variable name="unreachBranchesHelp">Are any branches syntactically unreachable</xsl:variable> 
  <xsl:variable name="uncovBranchesHelp">Are any branches not covered by any test-case (ie. unreachabe if no timeouts)</xsl:variable> 
  <xsl:variable name="coveredHelp">Number of feasible execution paths covered by a test-case</xsl:variable>  
  <xsl:variable name="infeasibleHelp">Number of execution paths or partial paths found to be infeasible</xsl:variable>    
  <xsl:variable name="iterlimitHelp">Number of test-cases rejected because unnecessary for respect of the coverage criterion</xsl:variable>  
  <xsl:variable name="timeoutHelp">Number of execution paths or partial paths assumed to be infeasible because constraint solving timed out</xsl:variable>
  <xsl:variable name="assumeHelp">Number of exection paths or partial paths explored but not covered because they violated an "assume" in the source code</xsl:variable>  
<!--END Variables for help messages -->

  <xsl:template match="/">
    <html>
      <head>
	<link rel="stylesheet" href="style.css" type="text/css"/>
	<meta http-equiv="CACHE-CONTROL" content="NO-CACHE"/>
	<xsl:if test="$paramRefresh != 'no'">
	  <xsl:element name="meta">
	    <xsl:attribute name="http-equiv">refresh</xsl:attribute>
	    <xsl:attribute name="content"><xsl:value-of select="$paramRefresh"/></xsl:attribute>
	  </xsl:element>
	</xsl:if>
	<title>Test session report</title>
      </head>
      <body>
	<h2 class="page_title">Test session summary<xsl:if test="$paramRefresh != 'no'"> (so far...) </xsl:if></h2>
	<xsl:apply-templates  select="TestReport"/>
      </body>
    </html>
  </xsl:template>
  <xsl:template match="TestReport">
<!--
    <div class="centered">
      <table border="0" width="100%" cellpadding="2">
	<tr><td align="center" width="100%">
	  <xsl:if test="$paramRefresh = 'no'">
	    <xsl:element name="a"><xsl:attribute name="href"><xsl:value-of select="SessionData/TestSessionFile"/><xsl:value-of select="$paramExtHTML"/></xsl:attribute>View path prefixes explored</xsl:element>
	  </xsl:if>
	  <xsl:if test="$paramRefresh != 'no'">Path prefixes explored not yet available...</xsl:if>
	</td></tr>      
      </table>
    </div>
-->
    <h3 class="section_title">General test session information</h3>
    <div class="centered">
      <xsl:comment><p><b>Session started: </b><xsl:value-of select="SessionData/When"/></p></xsl:comment><xsl:text>
</xsl:text><xsl:comment><p><b>PathCrawler version: </b><xsl:value-of select="SessionData/Version"/></p></xsl:comment><xsl:text>
</xsl:text>      
      <p><b>Function under test: </b> <xsl:value-of select="SessionData/FunName"/></p>
      <p>
	<b>Coverage criterion:&nbsp;
	<img src="help.gif" border="0" alt="{$criterionHelp}" title="{$criterionHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;
	</b> 
      <xsl:if test="SessionData/Strategy/@Coverage = 'all-paths'">all feasible paths</xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'all-branches'">all reachable branches</xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'all-mcdc'">mcdc of all decisions</xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'paths-func'">all feasible paths in function <xsl:value-of select="SessionData/Strategy"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'branches-func'">all reachable branches in function <xsl:value-of select="SessionData/Strategy"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@Coverage = 'mcdc-func'">mcdc of all decisions in function <xsl:value-of select="SessionData/Strategy"/></xsl:if>
      <xsl:if test="SessionData/Strategy/@IterLimit != 'none'">, limit loop iterations to <xsl:value-of select="SessionData/Strategy/@IterLimit"/></xsl:if>      
      <xsl:if test="SessionData/Strategy/@RecurLimit != 'none'">, limit recursion unfolding to <xsl:value-of select="SessionData/Strategy/@RecurLimit"/></xsl:if>      
      <xsl:if test="SessionData/Strategy/@SuffixLengthLimit != 'none'">, limit number of conditions treated in path suffix to <xsl:value-of select="SessionData/Strategy/@SuffixLengthLimit"/></xsl:if>
      </p>
      <xsl:if test="$paramRefresh = 'no'">
	<p>
	  <b>Termination status:&nbsp;
	  <img src="help.gif" border="0" alt="{$statusHelp}" title="{$statusHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;
	  </b>
	  <xsl:if test="TermStatus/@Type != 'normally' or UntreatedNum != '0' or UninitVarNum != '0' or PCBugNum != '0' or TimeoutNum != '0'">
	    <font class="warn">
	      <xsl:value-of select="TermStatus/@Type"/>
	      <xsl:if test="TermStatus != ''"> (<xsl:value-of select="TermStatus"/>)</xsl:if>
	      <xsl:if test="UntreatedNum != '0' or UninitVarNum != '0' or PCBugNum != '0'">, with warnings</xsl:if>
	      <xsl:if test="TimeoutNum != '0'">, with timeouts</xsl:if>
	    </font>
	  </xsl:if>
	  <xsl:if test="TermStatus/@Type = 'normally' and UntreatedNum = '0' and UninitVarNum = '0' and PCBugNum = '0' and TimeoutNum = '0'">
	    <xsl:value-of select="TermStatus/@Type"/>
	    <xsl:if test="TermStatus != ''"> (<xsl:value-of select="TermStatus"/>)</xsl:if>
	  </xsl:if>
	</p>
      </xsl:if>
    </div>    
    <h3 class="section_title">Test session statistics</h3>
    <div class="centered">     
      <table class="input_data">
	<tr class="input_data_caption">
	  <td><b>Total test session duration:</b></td> 
	  <td class="middle"><xsl:value-of select="Dur"/> sec.</td>
	</tr> 
	<xsl:if test="UnreachableBranches">
	  <tr class="input_data_caption">
	    <td><b>Unreachable branches:&nbsp;<img src="help.gif" border="0" 
	   alt="{$unreachBranchesHelp}" title="{$unreachBranchesHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;</b></td> 
	    <td class="middle">
	      <xsl:choose>
		<xsl:when test="not(UnreachableBranches/*)">
		  none
		</xsl:when>
		<xsl:otherwise>
		  <xsl:apply-templates select="UnreachableBranches"/>
		</xsl:otherwise>
	      </xsl:choose>
	    </td>
	  </tr>
	</xsl:if>
	<xsl:if test="UncoveredBranches">
	  <tr class="input_data_caption">
	    <td><b>Uncovered branches:&nbsp;<img src="help.gif" border="0" 
	   alt="{$uncovBranchesHelp}" title="{$uncovBranchesHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;</b></td> 
	    <td class="middle">
	      <xsl:choose>
		<xsl:when test="not(UncoveredBranches/*)">
		  none
		</xsl:when>
		<xsl:otherwise>
		  <xsl:apply-templates select="UncoveredBranches"/>
		</xsl:otherwise>
	      </xsl:choose>
	    </td>
	  </tr>
	</xsl:if>
	<xsl:if test="UncoveredLabels">
	  <tr class="input_data_caption">
	    <td><b>Uncovered labels:&nbsp;<img src="help.gif" border="0" 
	   alt="{$labelsHelp}" title="{$labelsHelp}" style="cursor: help;" align="bottom"/>&nbsp;&nbsp;</b></td> 
	    <td class="middle">
	      <xsl:choose>
		<xsl:when test="not(UncoveredLabels/*)">
		  none
		</xsl:when>
		<xsl:otherwise>
		  <xsl:apply-templates select="UncoveredLabels"/>
		</xsl:otherwise>
	      </xsl:choose>
	    </td>
	  </tr>
	</xsl:if>
	<tr class="input_data_caption">
	  <td><b>Number of test-cases:</b></td> 
	  <td class="middle"><xsl:value-of select="CoveredNum"/></td>
	</tr>
	<tr>
	  <td>
	    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with verdict "success":&nbsp;
	    <img src="help.gif" border="0" alt="{$successHelp}" title="{$successHelp}" style="cursor: help;" align="bottom"/>
	    </b>
	  </td> 
	  <td class="middle"><xsl:value-of select="SuccessNum"/></td>
	</tr>
	<tr>
	  <td>
	    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	    <xsl:if test="FailureNum != '0'"><font class="attn">with verdict "failure":</font></xsl:if>
	    <xsl:if test="FailureNum = '0'">with verdict "failure":</xsl:if>&nbsp;
	    <img src="help.gif" border="0" alt="{$failureHelp}" title="{$failureHelp}" style="cursor: help;" align="bottom"/>
	    </b>
	  </td> 
	  <td class="middle">
	    <xsl:if test="FailureNum != '0'"><font class="attn"><xsl:value-of select="FailureNum"/></font></xsl:if>
	    <xsl:if test="FailureNum = '0'"><xsl:value-of select="FailureNum"/></xsl:if>
	  </td>
	</tr>
	<tr>
	  <td>
	    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with verdict "unknown":&nbsp;
	    <img src="help.gif" border="0" alt="{$unknownHelp}" title="{$unknownHelp}" style="cursor: help;" align="bottom"/>
	    </b>
	  </td> 
	  <td class="middle"><xsl:value-of select="UnknownNum"/></td>
	</tr>
	<tr>
	  <td>
	    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	    <xsl:if test="AssertViolatedNum != '0'"><font class="attn">violating user assertion:</font></xsl:if>
	    <xsl:if test="AssertViolatedNum = '0'">violating user assertion:</xsl:if>&nbsp;
	    <img src="help.gif" border="0" alt="{$assertHelp}" title="{$assertHelp}" style="cursor: help;" align="bottom"/>
	    </b>
	  </td> 
	  <td class="middle">
	    <xsl:if test="AssertViolatedNum != '0'">
	      <font class="attn"><xsl:value-of select="AssertViolatedNum"/></font>
	    </xsl:if>
	    <xsl:if test="AssertViolatedNum = '0'"><xsl:value-of select="AssertViolatedNum"/></xsl:if>
	  </td>
	</tr>
	<xsl:if test="CrashedNum != '0'">
	<tr>
	  <td>
	    <font class="attn">
	      <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;function under test crashed:&nbsp;
	      <img src="help.gif" border="0" alt="{$crashedHelp}" title="{$crashedHelp}" style="cursor: help;" align="bottom"/>
	      </b>
	    </font>
	  </td> 
	  <td class="middle"><font class="attn"><xsl:value-of select="CrashedNum"/></font></td>
	</tr>
	</xsl:if>
	<xsl:if test="HungNum != '0'">
	<tr>
	  <td>
	    <font class="attn">
	      <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;function under test hung:&nbsp;
	      <img src="help.gif" border="0" alt="{$hungHelp}" title="{$hungHelp}" style="cursor: help;" align="bottom"/>
	      </b>
	    </font>
	  </td> 
	  <td class="middle"><font class="attn"><xsl:value-of select="HungNum"/></font></td>
	</tr>
	</xsl:if>
	<xsl:if test="SegFaultNum != '0'">
        <tr>
	  <td>
	    <font class="attn">
	      <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with run-time error:&nbsp;<img src="help.gif" border="0" alt="{$rteHelp}" title="{$rteHelp}" style="cursor: help;" align="bottom"/>
	      </b>
	    </font>
	  </td> 
	  <td class="middle"><font class="attn"><xsl:value-of select="SegFaultNum"/></font></td>
	</tr>
	</xsl:if>
	<xsl:if test="BugOracleNum != '0' or MaybeSuccessNum != '0' or MaybeUnknownNum != '0' or MaybeFailureNum != '0'  ">
        <tr>
	  <td>
	    <font class="warn">
	      <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with oracle warnings:&nbsp;
	      <img src="help.gif" border="0" alt="{$oracleWarningHelp}" title="{$oracleWarningHelp}" style="cursor: help;" align="bottom"/>
	      </b>
	    </font>
	  </td> 
	  <td class="middle">
	    <font class="warn">
	      <xsl:value-of select="BugOracleNum + MaybeSuccessNum + MaybeUnknownNum + MaybeFailureNum"/>
	    </font>
	  </td>
	</tr>
	</xsl:if>
	<xsl:text>
	  </xsl:text><xsl:comment>BugOracleNum: <xsl:value-of select="BugOracleNum"/></xsl:comment><xsl:text>
	  </xsl:text><xsl:comment>MaybeSuccessNum: <xsl:value-of select="MaybeSuccessNum"/></xsl:comment><xsl:text>
	  </xsl:text><xsl:comment>MaybeUnknownNum: <xsl:value-of select="MaybeUnknownNum"/></xsl:comment><xsl:text>
	  </xsl:text><xsl:comment>MaybeFailureNum: <xsl:value-of select="MaybeFailureNum"/></xsl:comment><xsl:text>
	</xsl:text>
	<tr class="input_data_caption">
	  <td>
	    <b>Number of treated partial paths:&nbsp;
	    <img src="help.gif" border="0" alt="{$pathsHelp}" title="{$pathsHelp}" style="cursor: help;" align="bottom"/>
	    </b>
	  </td> 
	  <td class="middle"><xsl:value-of select="TotalPrefixNum"/></td>
	</tr>
	<tr>
	  <td>
	    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;covered:&nbsp;
	    <img src="help.gif" border="0" alt="{$coveredHelp}" title="{$coveredHelp}" style="cursor: help;" align="bottom"/>
	    </b>
	  </td> 
	  <td class="middle"><xsl:value-of select="CoveredNum"/></td>
	</tr>
        <xsl:if test="InfeasibleNum != '0'">
	  <tr>
	    <td>
	      <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;infeasible:&nbsp;
	      <img src="help.gif" border="0" alt="{$infeasibleHelp}" title="{$infeasibleHelp}" style="cursor: help;" align="bottom"/>
	      </b>
	    </td> 
	    <td class="middle"><xsl:value-of select="InfeasibleNum"/></td>
	  </tr>
	</xsl:if>
        <xsl:if test="TimeoutNum != '0'">
	  <tr>
	    <td>
	      <font class="warn">
		<b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;interrupted by timeout:&nbsp;
		<img src="help.gif" border="0" alt="{$timeoutHelp}" title="{$timeoutHelp}" style="cursor: help;" align="bottom"/>
		</b>
	      </font>
	    </td> 
	    <td class="middle"><font class="warn"><xsl:value-of select="TimeoutNum"/></font></td>
	  </tr>
	</xsl:if>
        <xsl:if test="IterLimitViolatedNum != '0'">
	  <tr>
	    <td>
	      <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;unnecessary for coverage:&nbsp;
	      <img src="help.gif" border="0" alt="{$iterlimitHelp}" title="{$iterlimitHelp}" style="cursor: help;" align="bottom"/>
	      </b>
	    </td> 
	  <td class="middle"><xsl:value-of select="IterLimitViolatedNum"/></td>
	  </tr>
	</xsl:if>
        <xsl:if test="AssumeViolatedNum != '0'">
	  <tr>
	    <td>
	      <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;violating an assume:&nbsp;
	      <img src="help.gif" border="0" alt="{$assumeHelp}" title="{$assumeHelp}" style="cursor: help;" align="bottom"/>
	      </b>
	    </td> 
	  <td class="middle"><xsl:value-of select="AssumeViolatedNum"/></td>
	  </tr>
	</xsl:if>
	<xsl:if test="UninitVarNum != '0'">
          <tr>
	    <td>
	      <font class="warn">
		<b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uninitialised variables:&nbsp;
		<img src="help.gif" border="0" alt="{$uninitVarHelp}" title="{$uninitVarHelp}" style="cursor: help;" align="bottom"/>
		</b>
	      </font>
	    </td> 
	    <td class="middle"><font class="warn"><xsl:value-of select="UninitVarNum"/></font></td>
	  </tr>
	</xsl:if>
	<xsl:if test="UntreatedNum != '0'">
          <tr>
	    <td>
	      <font class="warn">
		<b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;untreated in PathCrawler:&nbsp;
		<img src="help.gif" border="0" alt="{$untreatedHelp}" title="{$untreatedHelp}" style="cursor: help;" align="bottom"/>
		</b>
	      </font>
	    </td> 
	    <td class="middle"><font class="warn"><xsl:value-of select="UntreatedNum"/></font></td>
	  </tr>
	</xsl:if>
	<xsl:if test="PCBugNum != '0'">
          <tr>
	    <td>
	      <font class="warn">
		<b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with PathCrawler error:&nbsp;
		<img src="help.gif" border="0" alt="{$PCBugHelp}" title="{$PCBugHelp}" style="cursor: help;" align="bottom"/>
		</b>
	      </font>
	    </td> 
	    <td class="middle"><font class="warn"><xsl:value-of select="PCBugNum"/></font></td>
	  </tr>
	</xsl:if>
      </table>
    </div>
  </xsl:template>

  <xsl:template match="N"><xsl:if test="@SrcFile"><xsl:value-of select="@SrcFile"/>&nbsp;:&nbsp;</xsl:if>-<xsl:value-of select="."/><xsl:if test="@LID">(label <xsl:value-of select="@LID"/>)&nbsp;</xsl:if>; </xsl:template>
  
  <xsl:template match="P"><xsl:if test="@SrcFile"><xsl:value-of select="@SrcFile"/>&nbsp;:&nbsp;</xsl:if>+<xsl:value-of select="."/><xsl:if test="@LID">(label <xsl:value-of select="@LID"/>)&nbsp;</xsl:if>; </xsl:template>

  <xsl:template match="UncoveredLabels|UncoveredBranches|UnreachableBranches">
    <xsl:if test="child::*"><xsl:apply-templates select="child::*"/></xsl:if>
    <xsl:if test="not(child::*)"><i>none</i></xsl:if>
  </xsl:template>
  
  <xsl:template match="LID"><xsl:value-of select="."/>; </xsl:template>

</xsl:stylesheet>
