<?xml version="1.0" encoding="UTF-8" ?>
<!--
    fix-committees
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
    
    <xsl:template match="@*|node()">
        <xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy>
    </xsl:template>
    
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>
    
    <xsl:template match="/congressional-committees">
        <entities type="committee"
            version="congress-113"
            updated="{date:date-time()}">
            <xsl:apply-templates select="*"/>
        </entities>
    </xsl:template>
    
    <xsl:template match="committee-entity">
        <entity><xsl:apply-templates select="@*|node()"/></entity>
    </xsl:template>
</xsl:stylesheet>
