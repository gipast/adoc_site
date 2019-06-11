1000 REM ******************************************************************
1010 REM *                 GPSS/PC(tm) COMMENT STRIPPER
1020 REM *                            BY
1030 REM *                    BRAD A. HEDRICK-GPSS/PC(tm) USER
1040 REM *                     AT HIRAM WALKER & SONS
1050 REM *            
1060 REM *      To save a considerable amount of memory when running a GPSS/PC(tm)
1070 REM * program, lines with comment fields can be deleted.
1080 REM *      This program will delete from the GPSS/PC(tm) code, all comments 
1090 REM * which begin with a semicolon (;), plus the blank spaces that lead
1100 REM * up to the comment field.  Comments with asterisks (*) are left alone
1110 REM * and are considered a "permanent" part of the GPSS/PC(tm) executable 
1120 REM * program.
1130 REM *
1140 REM * WARNING: Lines consisting of a line number followed by blank(s) and
1150 REM * a semicolon, will be deleted - use an asterisk instead of a semi-
1160 REM * colon to save the numbered line(s).
1170 REM *
1180 REM *********************************************************************
1190 REM * Initialize constants
1200   DATA 0,1,2,3,4,5,6,7,8,9
1210   FOR K = 1 TO 10 : READ NC$(K) : NEXT K
1220 REM * Get file specs from user and open
1230   INPUT "ENTER THE INPUT FILE.EXT " ,I$
1240   INPUT "ENTER THE OUTPUT FILE.EXT " ,O$
1250   OPEN I$ FOR INPUT AS #1
1260   OPEN O$ FOR OUTPUT AS #2
1270 REM * Processing loop
1280   N = 1
1290   IF EOF(1) THEN 1420
1300     LINE INPUT #1, IN$
1310     PS=INSTR(IN$,";")
1320     IF PS = 0 THEN GOTO 1400
1330       IF N>=PS THEN 1270      :REM SPECIAL CASE FOR COMMENTS W/NO LINE #'S
1340         CH$ = MID$(IN$,PS-N,1)
1350         IF CH$ <> " " THEN GOTO 1380
1360         N = N + 1
1370       GOTO 1330
1380       IN$ = MID$(IN$,1,PS-N)
1390       GOSUB 1450
1400     PRINT #2,IN$
1410   GOTO 1270
1420 CLOSE
1430 SYSTEM
1440 END
1450 REM * Subroutine to test for and handle the situation when line number *
1460 REM * is the only data left in the record
1470   L = LEN(IN$)
1480   FOR I = 1 TO L
1490     X$ = MID$(IN$,I,1)
1500     FOR J = 1 TO 10
1510       IF X$ = NC$(J) THEN 1540
1520     NEXT J
1530     GOTO 1560 : REM we have found more than just a line number
1540   NEXT I
1550   TOTO 1270 : REM return point after finding only a line number remaining
1560   RETURN
