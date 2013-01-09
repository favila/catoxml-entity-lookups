<?xml version="1.0" encoding="UTF-8" ?>
<!--
	govtrack2cato
	transform govtrack's people.xml into a simplified cato entity lookup table
	Created by Francis Avila on 2013-01-09.
	Copyright (c) 2013 Dancing Mammoth, Inc. All rights reserved.
-->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:date="http://exslt.org/dates-and-times" 
    extension-element-prefixes="date"
    exclude-result-prefixes="date">
    <xsl:strip-space elements="*"/>
    <xsl:output indent="yes" encoding="UTF-8" method="xml" />
    
    <xsl:param name="source" value=""/>
    <xsl:template match="@*|node()">
        <xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy>
    </xsl:template>
    
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>

    <xsl:template match="/people">
        <entities type="person" 
            version="congress-{@session}"
            updated="{date:date-time()}">
            <xsl:if test="normalize-space($source)">
                <xsl:attribute name="source"><xsl:value-of select="normalize-space($source)"/></xsl:attribute>
            </xsl:if>
            <xsl:apply-templates select="person"/>
        </entities>
    </xsl:template>
    
    <xsl:template match="person">
        <entity id="{@bioguideid}" govtrackid="{@id}">
            <xsl:copy-of select="@title | @state | @class | @district | @party"/>
            <name>
                <xsl:copy-of select="@lastname | @firstname"/>
                <xsl:value-of select="translate(@name, '[]', '()')"/>
            </name>
        </entity>
    </xsl:template>

</xsl:stylesheet>
