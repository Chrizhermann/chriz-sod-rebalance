// Reuse the installed state's localized text and transitions verbatim.
// The original crypt routes and native JoinParty endpoint remain intact.
APPEND ~BDSHARTE~
IF ~%csr110_field_condition%~ THEN BEGIN csr110_sharteel_field
  SAY #%csr110_sharteel_say%
  COPY_TRANS ~BDSHARTE~ 4
END
END
