
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  
<xsl:template match="ent[@type='location']">
  <xsl:variable name="sw">
    <xsl:value-of select="parts/part/@sw"/>
  </xsl:variable>
  <xsl:variable name="snip">
    <xsl:value-of select="/document//s[w[@id=$sw]]"/>
  </xsl:variable>
  <xsl:copy>
    <xsl:attribute name="snippet">
      <xsl:value-of select="normalize-space(/document//s[w[@id=$sw]])"/>
    </xsl:attribute>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
