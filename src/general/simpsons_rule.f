! *****************************COPYRIGHT*******************************
! (C) Crown copyright Met Office. All rights reserved.
! For further details please refer to the file COPYRIGHT.txt
! which you should have received as part of this distribution.
! *****************************COPYRIGHT*******************************
!
!+ Subroutine to integrate an array of equally spaced values.
!
! Method:
!   Perform integration using Simpsons Rule. This needs an even
!   number of intervals, so if N is odd the last three intervals
!   are integrated using Simpson's 3/8 rule. A single interval is
!   integrated using the trapezoidal rule.
!
!- ---------------------------------------------------------------------
      SUBROUTINE SIMPSONS_RULE(N,DELTA,INPUT_ARRAY,RESULT)


      IMPLICIT NONE

      INTEGER, INTENT(IN) ::
     &     N
!             Number of intervals (INPUT_ARRAY holds N+1 points)

      REAL(KIND=KIND(1.0D0)) , INTENT(IN) ::
     &     DELTA
!             Size of Interval
     &  ,  INPUT_ARRAY(0:N)
!             Array being summed over

      REAL(KIND=KIND(1.0D0)) , INTENT(OUT) ::
     &     Result
!             The final sum of all array entries

!
! Local Variables
!
      INTEGER
     &   I
!            Looping variable
     &  , N_SIMP
!            Number of intervals integrated using Simpsons Rule

      REAL (KIND=KIND(1.0D0)) ::
     &    SUM
!            The sum of the array entries


      IF (N.EQ.1) THEN
        RESULT=0.5D0*DELTA*(INPUT_ARRAY(0)+INPUT_ARRAY(1))
        RETURN
      ELSE IF (MOD(N,2).EQ.1) THEN
        N_SIMP=N-3
      ELSE
        N_SIMP=N
      ENDIF

      SUM=0.0
      IF (N_SIMP.GT.0) THEN
        DO I=0,N_SIMP
           IF ((I.EQ.0).OR.(I.EQ.N_SIMP)) THEN
              SUM=SUM+INPUT_ARRAY(I)
           ELSE IF (MOD(I,2).EQ.0) THEN
              SUM=SUM+2.0*INPUT_ARRAY(I)
           ELSE IF (MOD(I,2).EQ.1) THEN
              SUM=SUM+4.0*INPUT_ARRAY(I)
           ENDIF
        ENDDO
      ENDIF

      RESULT=SUM*DELTA/3.0

!     Simpson's 3/8 rule over the last three intervals
      IF (N_SIMP.LT.N) THEN
        RESULT=RESULT+0.375D0*DELTA*(INPUT_ARRAY(N-3)
     &    +3.0D0*(INPUT_ARRAY(N-2)+INPUT_ARRAY(N-1))+INPUT_ARRAY(N))
      ENDIF

      RETURN
      END
