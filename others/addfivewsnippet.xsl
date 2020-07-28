<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  
<xsl:template match="ent[@type='location']">
  <xsl:variable name="sw">
    <xsl:value-of select="parts/part/@sw"/>
  </xsl:variable>
  <xsl:variable name="ew">
    <xsl:value-of select="parts/part/@ew"/>
  </xsl:variable>
  <xsl:copy>
    <xsl:attribute name="snippet">
      <xsl:value-of select="/document//w[@id=$sw]/preceding-sibling::w[5]"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="/document//w[@id=$sw]/preceding-sibling::w[4]"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="/document//w[@id=$sw]/preceding-sibling::w[3]"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="/document//w[@id=$sw]/preceding-sibling::w[2]"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="/document//w[@id=$sw]/preceding-sibling::w[1]"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="parts/part"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="/document//w[@id=$ew]/following-sibling::w[1]"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="/document//w[@id=$ew]/following-sibling::w[2]"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="/document//w[@id=$ew]/following-sibling::w[3]"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="/document//w[@id=$ew]/following-sibling::w[4]"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="/document//w[@id=$ew]/following-sibling::w[5]"/>
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
