// Component 290: common post-victory cleanup. Numeric state and transition
// indices are guarded against the installed resources in lib/comp290.tpa.

// Keep de Lancie's public victory chain (77-83); retire only the private
// Waterdeep pitch and its repeat-click coda.
ADD_STATE_TRIGGER ~BDDELANC~ 95  ~False()~
ADD_STATE_TRIGGER ~BDDELANC~ 104 ~False()~

// Bence's public states 64-65 stay. State 65 now performs state 66's harmless
// ambience/exit work directly, without mentioning Skie or entering state 66.
ALTER_TRANS ~BDBENCE~ BEGIN 65 END BEGIN 0 END BEGIN
  ACTION ~SoundActivate("SS_Soldier",TRUE)
EscapeArea()~
  EPILOGUE ~EXIT~
END

// Murder/arrest roots are dead even if another dialogue jumps into them.
ADD_STATE_TRIGGER ~BDBENCE~ 6  ~False()~
ADD_STATE_TRIGGER ~BDBENCE~ 9  ~False()~
ADD_STATE_TRIGGER ~BDBENCE~ 10 ~False()~
ADD_STATE_TRIGGER ~BDBENCE~ 67 ~False()~
ADD_STATE_TRIGGER ~BDBENCE~ 68 ~False()~
ADD_STATE_TRIGGER ~BDBENCE~ 70 ~False()~
ADD_STATE_TRIGGER ~BDBENCE~ 71 ~False()~
ADD_STATE_TRIGGER ~BDBENCE~ 73 ~False()~

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
ADD_STATE_TRIGGER ~BDCORWIJ~ 203 ~False()~
ALTER_TRANS ~BDCORWIJ~ BEGIN 203 END BEGIN 0 END BEGIN
  ACTION ~~
  EPILOGUE ~EXIT~
END

// Dazzo becomes the single explicit ending trigger after the public victory
// exchange has advanced bd_plot to 590. The platform files replace states
// 2/3's terminal action.
ADD_STATE_TRIGGER ~BDDAZZO~ 0 ~Global("bd_plot","GLOBAL",590)
Global("CSR_ENDING_USED","GLOBAL",0)~

// Retire the three Hooded-Man rumor entries and the debug dialogue's four
// dream plus four prison shortcuts. Portal and unrelated debug tools stay.
ADD_STATE_TRIGGER ~BDRUMOR3~ 7  ~False()~
ADD_STATE_TRIGGER ~BDRUMOR3~ 20 ~False()~
ADD_STATE_TRIGGER ~BDRUMOR3~ 37 ~False()~

ADD_TRANS_TRIGGER ~BDDEBUG~ 10 ~False()~ DO 1
ADD_TRANS_TRIGGER ~BDDEBUG~ 10 ~False()~ DO 2
ADD_TRANS_TRIGGER ~BDDEBUG~ 10 ~False()~ DO 3
ADD_TRANS_TRIGGER ~BDDEBUG~ 10 ~False()~ DO 4
ADD_TRANS_TRIGGER ~BDDEBUG~ 10 ~False()~ DO 5
ADD_TRANS_TRIGGER ~BDDEBUG~ 10 ~False()~ DO 6
ADD_TRANS_TRIGGER ~BDDEBUG~ 10 ~False()~ DO 7
ADD_TRANS_TRIGGER ~BDDEBUG~ 10 ~False()~ DO 8
