// Component 290: common post-victory cleanup. Numeric state and transition
// indices are supplied when absent by lib/comp290_seed.tpa.

// Keep de Lancie's public victory chain (77-83); retire only the private
// Waterdeep pitch and its repeat-click coda.
REPLACE_STATE_TRIGGER ~BDDELANC~ 95  ~False()~
REPLACE_STATE_TRIGGER ~BDDELANC~ 104 ~False()~

// Bence's public states 64-65 stay. State 65 now performs state 66's harmless
// ambience/exit work directly, without mentioning Skie or entering state 66.
ALTER_TRANS ~BDBENCE~ BEGIN 65 END BEGIN 0 END BEGIN
  ACTION ~SoundActivate("SS_Soldier",TRUE)
EscapeArea()~
  EPILOGUE ~EXIT~
END

// Murder/arrest roots are dead even if another dialogue jumps into them.
REPLACE_STATE_TRIGGER ~BDBENCE~ 6  ~False()~
REPLACE_STATE_TRIGGER ~BDBENCE~ 9  ~False()~
REPLACE_STATE_TRIGGER ~BDBENCE~ 10 ~False()~
REPLACE_STATE_TRIGGER ~BDBENCE~ 67 ~False()~
REPLACE_STATE_TRIGGER ~BDBENCE~ 68 ~False()~
REPLACE_STATE_TRIGGER ~BDBENCE~ 70 ~False()~
REPLACE_STATE_TRIGGER ~BDBENCE~ 71 ~False()~
REPLACE_STATE_TRIGGER ~BDBENCE~ 73 ~False()~

// Direct transition entry must also be harmless: state triggers do not guard
// GOTO/EXTERN routes.
ALTER_TRANS ~BDBENCE~ BEGIN 9 10 END BEGIN 0 END BEGIN
  ACTION ~~
  EPILOGUE ~EXIT~
END
ALTER_TRANS ~BDBENCE~ BEGIN 70 71 73 END BEGIN 0 1 END BEGIN
  ACTION ~~
  EPILOGUE ~EXIT~
END

// Corwin's optional arrest interjection is another direct-entry terminal.
REPLACE_STATE_TRIGGER ~BDCORWIJ~ 203 ~False()~
ALTER_TRANS ~BDCORWIJ~ BEGIN 203 END BEGIN 0 END BEGIN
  ACTION ~~
  EPILOGUE ~EXIT~
END

// Dazzo becomes the single explicit ending trigger after the public victory
// exchange has advanced bd_plot to 590. The platform files replace states
// 2/3's terminal action.
REPLACE_STATE_TRIGGER ~BDDAZZO~ 0 ~Global("bd_plot","GLOBAL",590)
Global("CSR_ENDING_USED","GLOBAL",0)~

// Retire the three Hooded-Man rumor entries and the debug dialogue's four
// dream plus four prison shortcuts. Portal and unrelated debug tools stay.
REPLACE_STATE_TRIGGER ~BDRUMOR3~ 7  ~False()~
REPLACE_STATE_TRIGGER ~BDRUMOR3~ 20 ~False()~
REPLACE_STATE_TRIGGER ~BDRUMOR3~ 37 ~False()~

ALTER_TRANS ~BDDEBUG~ BEGIN 10 END BEGIN 1 END BEGIN TRIGGER ~False()~ END
ALTER_TRANS ~BDDEBUG~ BEGIN 10 END BEGIN 2 END BEGIN TRIGGER ~False()~ END
ALTER_TRANS ~BDDEBUG~ BEGIN 10 END BEGIN 3 END BEGIN TRIGGER ~False()~ END
ALTER_TRANS ~BDDEBUG~ BEGIN 10 END BEGIN 4 END BEGIN TRIGGER ~False()~ END
ALTER_TRANS ~BDDEBUG~ BEGIN 10 END BEGIN 5 END BEGIN TRIGGER ~False()~ END
ALTER_TRANS ~BDDEBUG~ BEGIN 10 END BEGIN 6 END BEGIN TRIGGER ~False()~ END
ALTER_TRANS ~BDDEBUG~ BEGIN 10 END BEGIN 7 END BEGIN TRIGGER ~False()~ END
ALTER_TRANS ~BDDEBUG~ BEGIN 10 END BEGIN 8 END BEGIN TRIGGER ~False()~ END
